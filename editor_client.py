"""
Editor Client - Socket communication with Live UI Editor

Provides Python API to send commands to the Live UI Editor.
"""

import socket
import json
from typing import Dict, Any, Optional


class EditorClient:
    """Client for communicating with Live UI Editor via socket."""

    def __init__(self, host: str = "localhost", port: int = 7001, timeout: float = 5.0):
        """
        Initialize editor client.

        Args:
            host: Editor host address
            port: Editor port
            timeout: Socket timeout in seconds
        """
        self.host = host
        self.port = port
        self.timeout = timeout

    def send_command(self, action: str, **params) -> Dict[str, Any]:
        """
        Send a command to the editor.

        Args:
            action: Command action name
            **params: Additional command parameters

        Returns:
            Response dictionary from editor

        Raises:
            ConnectionError: If cannot connect to editor
            TimeoutError: If command times out
        """
        command = {"action": action, **params}

        try:
            # Create socket connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.host, self.port))

                # Send command
                sock.send(json.dumps(command).encode('utf-8'))

                # Receive response (max 10MB for screenshots)
                response_data = b""
                while True:
                    chunk = sock.recv(65536)
                    if not chunk:
                        break
                    response_data += chunk

                    # Try to parse - if valid JSON, we're done
                    try:
                        response = json.loads(response_data.decode('utf-8'))
                        return response
                    except json.JSONDecodeError:
                        # Not complete yet, keep receiving
                        continue

                # If we get here, parse final data
                if response_data:
                    return json.loads(response_data.decode('utf-8'))
                else:
                    return {"status": "error", "message": "Empty response"}

        except socket.timeout:
            raise TimeoutError(f"Command '{action}' timed out after {self.timeout}s")
        except ConnectionRefusedError:
            raise ConnectionError(
                f"Cannot connect to editor at {self.host}:{self.port}. "
                "Is Live UI Editor running?"
            )
        except Exception as e:
            raise ConnectionError(f"Communication error: {e}")

    def ping(self) -> bool:
        """
        Check if editor is running.

        Returns:
            True if editor responds, False otherwise
        """
        try:
            response = self.send_command("ping")
            return response.get("status") == "success"
        except (ConnectionError, TimeoutError):
            return False

    def reload_ui(self) -> Dict:
        """Reload the .ui file in the editor."""
        return self.send_command("reload_ui")

    def take_screenshot(self, output_path: str = "screenshots/screenshot.png") -> Dict:
        """
        Take a screenshot of the UI.

        Args:
            output_path: Where to save screenshot

        Returns:
            Response with screenshot_base64 and path
        """
        return self.send_command("take_screenshot", path=output_path)

    def get_widget_tree(self) -> Dict:
        """
        Get the widget hierarchy.

        Returns:
            Response with widget_tree
        """
        return self.send_command("get_widget_tree")

    def get_ui_file(self) -> str:
        """
        Get the current .ui file path.

        Returns:
            Path to .ui file
        """
        response = self.send_command("get_ui_file")
        return response.get("ui_file", "")


def test_connection(host: str = "localhost", port: int = 7001):
    """
    Test connection to Live UI Editor.

    Args:
        host: Editor host
        port: Editor port

    Returns:
        True if connected, False otherwise
    """
    client = EditorClient(host, port)
    return client.ping()


if __name__ == "__main__":
    # Test client
    import sys

    print("Testing Editor Client...")
    client = EditorClient()

    # Test ping
    if client.ping():
        print("✓ Editor is running")

        # Test get widget tree
        result = client.get_widget_tree()
        if result.get("status") == "success":
            print("✓ Got widget tree:")
            import json
            print(json.dumps(result.get("widget_tree", {}), indent=2))

        # Test screenshot
        result = client.take_screenshot("screenshots/test_screenshot.png")
        if result.get("status") == "success":
            print(f"✓ Screenshot saved: {result.get('path')}")
            print(f"  Base64 length: {len(result.get('screenshot_base64', ''))}")

    else:
        print("✗ Editor is not running")
        print(f"  Start with: rez-env pyside6 -- python live_ui_editor.py --ui <file.ui> --port {client.port}")
        sys.exit(1)
