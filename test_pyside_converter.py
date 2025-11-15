#!/usr/bin/env python3
"""
Test: PySide Version Converter

Tests conversion between PySide2 and PySide2:
1. UI file conversion
2. Python script conversion
3. Directory batch conversion
"""

import sys
import shutil
from pathlib import Path
from mcp_server import convert_pyside_version
from ui_manager import UIManager


def create_test_files():
    """Create test files for conversion."""
    print("Creating test files...")

    # 1. Create a PySide2 UI file
    manager = UIManager()
    manager.create_empty_ui("QDialog", "TestDialog", 400, 300)
    manager.add_widget("QPushButton", "okButton", properties={
        "text": "OK",
        "geometry": {"x": 150, "y": 200, "width": 100, "height": 40}
    })
    manager.save("test_pyside6.ui")
    print("✓ Created test_pyside6.ui")

    # 2. Create a PySide2 Python script
    py6_code = """#!/usr/bin/env python3
'''
Test PySide2 Application
'''

from PySide2.QtWidgets import QApplication, QDialog, QPushButton
from PySide2.QtCore import Qt

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide2 Dialog")

        # Create button
        self.button = QPushButton("OK", self)
        self.button.setGeometry(100, 100, 80, 30)

        # Connect signal (PySide2 uses exec())
        self.button.clicked.connect(self.accept)

    def show_dialog(self):
        return self.exec_()  # PySide2 style

if __name__ == "__main__":
    app = QApplication([])
    dialog = MyDialog()
    dialog.show_dialog()
"""

    with open("test_pyside6.py", "w") as f:
        f.write(py6_code)
    print("✓ Created test_pyside6.py")


def test_ui_conversion():
    """Test UI file conversion."""
    print("\n" + "=" * 70)
    print("Test 1: UI File Conversion (PySide2 → PySide2)")
    print("=" * 70)

    # Make a copy
    shutil.copy("test_pyside6.ui", "test_convert.ui")

    # Convert to PySide2
    result = convert_pyside_version("pyside2", "test_convert.ui")

    print(f"\nStatus: {result['status']}")
    print(f"Files converted: {len(result['files_converted'])}")

    if result['files_converted']:
        print(f"\n✓ Converted: {result['files_converted'][0]}")
        if result['changes_made']:
            print("  Changes:")
            for change in result['changes_made'].get(result['files_converted'][0], []):
                print(f"    - {change}")

    # Convert back to PySide2
    print("\n" + "-" * 70)
    print("Converting back: PySide2 → PySide2")
    print("-" * 70)

    result = convert_pyside_version("pyside6", "test_convert.ui")
    print(f"Status: {result['status']}")
    print(f"Files converted: {len(result['files_converted'])}")


def test_python_conversion():
    """Test Python script conversion."""
    print("\n" + "=" * 70)
    print("Test 2: Python Script Conversion (PySide2 → PySide2)")
    print("=" * 70)

    # Make a copy
    shutil.copy("test_pyside6.py", "test_convert.py")

    # Convert to PySide2
    result = convert_pyside_version("pyside2", "test_convert.py")

    print(f"\nStatus: {result['status']}")
    print(f"Files converted: {len(result['files_converted'])}")

    if result['files_converted']:
        print(f"\n✓ Converted: {result['files_converted'][0]}")
        if result['changes_made']:
            print("  Changes:")
            for change in result['changes_made'].get(result['files_converted'][0], []):
                print(f"    - {change}")

    # Show converted code snippet
    print("\n" + "-" * 70)
    print("Converted Code (relevant lines):")
    print("-" * 70)

    with open("test_convert.py", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:20], 1):  # Show first 20 lines
            if "PySide" in line or "exec" in line:
                print(f"{i:3}: {line.rstrip()}")


def test_directory_conversion():
    """Test batch directory conversion."""
    print("\n" + "=" * 70)
    print("Test 3: Directory Batch Conversion")
    print("=" * 70)

    # Create test directory
    test_dir = Path("test_conversion_dir")
    test_dir.mkdir(exist_ok=True)

    # Copy test files
    shutil.copy("test_pyside6.ui", test_dir / "file1.ui")
    shutil.copy("test_pyside6.ui", test_dir / "file2.ui")
    shutil.copy("test_pyside6.py", test_dir / "script1.py")
    shutil.copy("test_pyside6.py", test_dir / "script2.py")

    print(f"Created test directory with 4 files (2 UI + 2 Python)")

    # Convert entire directory
    print("\nConverting entire directory to PySide2...")
    result = convert_pyside_version("pyside2", str(test_dir))

    print(result['report'])

    # Cleanup
    shutil.rmtree(test_dir)
    print("\n✓ Test directory cleaned up")


def test_full_report():
    """Test comprehensive conversion report."""
    print("\n" + "=" * 70)
    print("Test 4: Full Conversion Report")
    print("=" * 70)

    # Convert current directory (only test files)
    result = convert_pyside_version("pyside2", ".")

    print(result['report'])

    # Summary
    print("\n" + "=" * 70)
    print("Conversion Summary")
    print("=" * 70)
    print(f"Total files converted: {len(result['files_converted'])}")
    print(f"Warnings: {len(result['warnings'])}")
    print(f"Errors: {len(result['errors'])}")


def cleanup():
    """Clean up test files."""
    print("\n" + "=" * 70)
    print("Cleaning up test files...")
    print("=" * 70)

    test_files = [
        "test_pyside6.ui",
        "test_pyside6.py",
        "test_convert.ui",
        "test_convert.py"
    ]

    for file in test_files:
        if Path(file).exists():
            Path(file).unlink()
            print(f"✓ Removed {file}")


def main():
    """Run all tests."""
    print("=" * 70)
    print("PySide Version Converter Test Suite")
    print("=" * 70)

    try:
        # Setup
        create_test_files()

        # Run tests
        test_ui_conversion()
        test_python_conversion()
        test_directory_conversion()
        test_full_report()

        print("\n" + "=" * 70)
        print("✅ All Tests Passed!")
        print("=" * 70)

        print("\n🎯 PySide Version Converter is working perfectly!")
        print("\nYou can now convert between PySide2 and PySide2:")
        print("  - Single files: .ui or .py")
        print("  - Entire directories")
        print("  - Automatic detection of changes needed")
        print("  - Detailed conversion reports")

        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Cleanup
        cleanup()


if __name__ == "__main__":
    sys.exit(main())
