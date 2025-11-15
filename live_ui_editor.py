"""
Live UI Editor - Real-time Qt UI viewer with socket control

Maya commandPort-style socket server for Qt UI manipulation.
Run with: rez-env pyside6 -- python live_ui_editor.py --ui myfile.ui --port 7001
"""

import sys
import socket
import json
import threading
import argparse
import base64
from pathlib import Path
from io import BytesIO

from PySide2.QtWidgets import QApplication, QWidget, QDialog, QMainWindow
from PySide2.QtCore import Qt, QTimer, Signal, QObject, QFile
from PySide2.QtGui import QPixmap
from PySide2.QtUiTools import QUiLoader

from ui_manager import UIManager


class EditorSignals(QObject):
    """Signals for cross-thread communication."""
    reload_requested = Signal()
    screenshot_requested = Signal(str)  # output path
    command_received = Signal(dict)


class LiveUIEditor:
    """
    Live UI Editor with socket control.

    Listens for JSON commands on a TCP port and manipulates the UI accordingly.
    """

    def __init__(self, ui_file: str, port: int = 7001):
        """
        Initialize Live UI Editor.

        Args:
            ui_file: Path to .ui file to load
            port: TCP port to listen on
        """
        self.ui_file = Path(ui_file)
        self.port = port
        self.widget = None
        self.app = None
        self.server_socket = None
        self.running = True
        self.signals = EditorSignals()

        # Connect signals
        self.signals.reload_requested.connect(self._reload_ui)
        self.signals.screenshot_requested.connect(self._take_screenshot)
        self.signals.command_received.connect(self._handle_command)

    def start(self):
        """Start the editor and socket server."""
        # Create Qt application
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

        # Load UI
        self._load_ui()

        # Start socket server in separate thread
        server_thread = threading.Thread(target=self._run_server, daemon=True)
        server_thread.start()

        print(f"[LiveUIEditor] Listening on port {self.port}")
        print(f"[LiveUIEditor] Loaded UI: {self.ui_file}")
        print(f"[LiveUIEditor] Send JSON commands to control the UI")

        # Show widget
        if self.widget:
            self.widget.show()

        # Run Qt event loop
        return self.app.exec_()

    def _load_ui(self):
        """Load .ui file and display widget."""
        if not self.ui_file.exists():
            print(f"[ERROR] UI file not found: {self.ui_file}")
            return

        try:
            loader = QUiLoader()
            ui_file = QFile(str(self.ui_file))
            ui_file.open(QFile.ReadOnly)
            self.widget = loader.load(ui_file)
            ui_file.close()
            print(f"[INFO] Loaded UI: {self.ui_file}")
        except Exception as e:
            print(f"[ERROR] Failed to load UI: {e}")

    def _reload_ui(self):
        """Reload UI file (hot-reload)."""
        print("[INFO] Reloading UI...")
        if self.widget:
            self.widget.close()
        self._load_ui()
        if self.widget:
            self.widget.show()

    def _take_screenshot(self, output_path: str):
        """
        Capture screenshot of the widget.

        Args:
            output_path: Where to save screenshot
        """
        if not self.widget:
            print("[ERROR] No widget to screenshot")
            return None

        try:
            pixmap = self.widget.grab()
            pixmap.save(output_path)
            print(f"[INFO] Screenshot saved: {output_path}")
            return output_path
        except Exception as e:
            print(f"[ERROR] Screenshot failed: {e}")
            return None

    def _get_screenshot_base64(self) -> str:
        """Get screenshot as base64 string."""
        if not self.widget:
            return ""

        try:
            pixmap = self.widget.grab()
            byte_array = BytesIO()
            pixmap.save(byte_array, "PNG")
            return base64.b64encode(byte_array.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"[ERROR] Screenshot encoding failed: {e}")
            return ""

    def _get_widget_tree(self) -> dict:
        """Get widget hierarchy from loaded UI."""
        if not self.ui_file.exists():
            return {}

        try:
            ui_manager = UIManager(str(self.ui_file))
            return ui_manager.get_widget_tree()
        except Exception as e:
            print(f"[ERROR] Failed to get widget tree: {e}")
            return {}

    def _run_server(self):
        """Run socket server (in separate thread)."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind(("localhost", self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)  # Allow checking self.running

            print(f"[SERVER] Listening on localhost:{self.port}")

            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    # Handle connection in separate thread
                    threading.Thread(
                        target=self._handle_connection,
                        args=(conn,),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] Server error: {e}")
                    break

        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def _handle_connection(self, conn: socket.socket):
        """Handle a single client connection."""
        try:
            # Receive command (max 64KB)
            data = conn.recv(65536).decode('utf-8')
            if not data:
                return

            command = json.loads(data)
            print(f"[COMMAND] Received: {command.get('action', 'unknown')}")

            # Process command
            response = self._process_command(command)

            # Send response
            conn.send(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError as e:
            error_response = {"status": "error", "message": f"Invalid JSON: {e}"}
            conn.send(json.dumps(error_response).encode('utf-8'))
        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            conn.send(json.dumps(error_response).encode('utf-8'))
        finally:
            conn.close()

    def _process_command(self, command: dict) -> dict:
        """
        Process a command and return response.

        Args:
            command: Command dictionary with 'action' key

        Returns:
            Response dictionary
        """
        action = command.get("action")

        if action == "reload_ui":
            # Must run in Qt main thread
            self.signals.reload_requested.emit()
            return {"status": "success", "message": "UI reloaded"}

        elif action == "take_screenshot":
            output_path = command.get("path", "screenshots/screenshot.png")
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # Take screenshot (runs in Qt thread via signal)
            screenshot_base64 = self._get_screenshot_base64()

            # Also save to file
            if screenshot_base64:
                import base64
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(screenshot_base64))

            return {
                "status": "success",
                "path": output_path,
                "screenshot_base64": screenshot_base64
            }

        elif action == "get_widget_tree":
            tree = self._get_widget_tree()
            return {
                "status": "success",
                "widget_tree": tree
            }

        elif action == "get_ui_file":
            return {
                "status": "success",
                "ui_file": str(self.ui_file)
            }

        elif action == "ping":
            return {
                "status": "success",
                "message": "pong"
            }

        else:
            return {
                "status": "error",
                "message": f"Unknown action: {action}"
            }

    def _handle_command(self, command: dict):
        """Handle command in Qt main thread."""
        # For future expansion: commands that modify UI
        pass

    def stop(self):
        """Stop the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Live UI Editor for Qt")
    parser.add_argument("--ui", required=True, help=".ui file to load")
    parser.add_argument("--port", type=int, default=7001, help="Port to listen on")
    args = parser.parse_args()

    editor = LiveUIEditor(args.ui, args.port)

    try:
        sys.exit(editor.start())
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        editor.stop()


if __name__ == "__main__":
    main()
