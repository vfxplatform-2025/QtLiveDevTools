"""
Simple .ui file viewer for testing

Usage: rez-env pyside6 python-3.9 -- python test_ui_viewer.py <ui_file>
"""

import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

def view_ui(ui_file_path):
    """Load and display a .ui file."""
    app = QApplication(sys.argv)

    loader = QUiLoader()
    ui_file = QFile(ui_file_path)

    if not ui_file.open(QFile.ReadOnly):
        print(f"Error: Cannot open file {ui_file_path}")
        return 1

    widget = loader.load(ui_file)
    ui_file.close()

    if widget is None:
        print(f"Error: Failed to load UI from {ui_file_path}")
        return 1

    widget.show()
    print(f"Showing UI: {ui_file_path}")
    return app.exec_()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_ui_viewer.py <ui_file>")
        print("\nExample:")
        print("  rez-env pyside6 python-3.9 -- python test_ui_viewer.py login_example.ui")
        sys.exit(1)

    ui_file = sys.argv[1]
    sys.exit(view_ui(ui_file))
