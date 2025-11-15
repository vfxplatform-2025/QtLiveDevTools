#!/usr/bin/env python3
"""
Test loading the created .ui files
Run with: rez-env pyside6 -- python test_load_ui.py
"""

import sys
from pathlib import Path
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


def load_ui(ui_file: str):
    """Load and display a .ui file."""
    ui_path = Path(ui_file)

    if not ui_path.exists():
        print(f"Error: UI file not found: {ui_file}")
        return None

    # Create UI loader
    loader = QUiLoader()

    # Load .ui file
    file = QFile(str(ui_path))
    file.open(QFile.ReadOnly)
    widget = loader.load(file)
    file.close()

    print(f"✓ Loaded: {ui_file}")
    print(f"  Widget type: {widget.__class__.__name__}")
    print(f"  Size: {widget.width()} x {widget.height()}")

    return widget


def main():
    """Main entry point."""
    app = QApplication(sys.argv)

    # Test loading different UI files
    ui_files = [
        "my_first_test.ui",
        "login_dialog.ui",
        "settings_dialog.ui"
    ]

    widgets = []
    for ui_file in ui_files:
        if Path(ui_file).exists():
            widget = load_ui(ui_file)
            if widget:
                widgets.append(widget)
                widget.show()
        else:
            print(f"✗ File not found: {ui_file}")

    if widgets:
        print(f"\n✓ Displaying {len(widgets)} UI windows")
        print("Close windows to exit...")
        sys.exit(app.exec_())
    else:
        print("\n✗ No UI files loaded")
        return 1


if __name__ == "__main__":
    main()
