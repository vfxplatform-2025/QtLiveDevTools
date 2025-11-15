#!/usr/bin/env python3
"""
PySide Version Converter - Convert between PySide2 and PySide2

Converts:
- .ui files (XML modifications)
- Python scripts (import statements, API changes)
- MCP server configuration
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ConversionResult:
    """Result of version conversion."""
    files_converted: List[str]
    changes_made: Dict[str, List[str]]
    errors: List[str]
    warnings: List[str]


class PySideConverter:
    """Convert between PySide2 and PySide2."""

    # API differences between PySide2 and PySide2
    API_CHANGES_6_TO_2 = {
        # Qt 6 removed these, Qt 5 had them
        "Qt::AA_EnableHighDpiScaling": None,  # Not needed in Qt5
        "Qt::AA_UseHighDpiPixmaps": None,  # Not needed in Qt5

        # Enum changes
        "Qt.AlignmentFlag": "Qt",
        "Qt.WindowType": "Qt",
        "Qt.ItemFlag": "Qt",

        # Method name changes
        "exec()": "exec_()",  # PySide2 uses exec_()
    }

    API_CHANGES_2_TO_6 = {
        # Reverse mapping
        "exec_()": "exec()",
    }

    def __init__(self):
        self.results = ConversionResult(
            files_converted=[],
            changes_made={},
            errors=[],
            warnings=[]
        )

    def convert_ui_file(self, ui_file: str, target_version: str) -> bool:
        """
        Convert .ui file to target PySide version.

        Args:
            ui_file: Path to .ui file
            target_version: "pyside6" or "pyside2"

        Returns:
            True if successful
        """
        try:
            tree = ET.parse(ui_file)
            root = tree.getroot()
            changes = []

            # Check current version in comments
            for comment in root.iter(ET.Comment):
                if "PySide2" in comment.text or "PySide2" in comment.text:
                    old_version = "PySide2" if "PySide2" in comment.text else "PySide2"
                    if target_version.lower() == old_version.lower():
                        self.results.warnings.append(
                            f"{ui_file}: Already in {target_version} format"
                        )
                        return True

            # Add version comment at the top
            version_comment = f" Generated for {target_version.upper()} "
            root.insert(0, ET.Comment(version_comment))
            changes.append(f"Added version comment: {target_version}")

            # Convert Qt enum references
            if target_version.lower() == "pyside2":
                # PySide2 → PySide2
                self._convert_enums_6_to_2(root, changes)
            else:
                # PySide2 → PySide2
                self._convert_enums_2_to_6(root, changes)

            # Save modified file
            self._indent(root)
            tree.write(ui_file, encoding='utf-8', xml_declaration=True)

            self.results.files_converted.append(ui_file)
            self.results.changes_made[ui_file] = changes

            return True

        except Exception as e:
            self.results.errors.append(f"{ui_file}: {str(e)}")
            return False

    def _convert_enums_6_to_2(self, root: ET.Element, changes: List[str]):
        """Convert PySide2 enum syntax to PySide2."""
        # Qt6 uses Qt.AlignCenter
        # Qt5 uses Qt.AlignCenter

        for elem in root.iter():
            if elem.text and "Qt." in elem.text:
                original = elem.text
                # Remove intermediate enum class names
                elem.text = re.sub(r'Qt\.(\w+Flag|WindowType|ItemFlag)\.', 'Qt.', elem.text)
                if elem.text != original:
                    changes.append(f"Enum: {original} → {elem.text}")

            # Check attributes too
            for attr, value in elem.attrib.items():
                if "Qt." in value:
                    original = value
                    new_value = re.sub(r'Qt\.(\w+Flag|WindowType|ItemFlag)\.', 'Qt.', value)
                    if new_value != original:
                        elem.attrib[attr] = new_value
                        changes.append(f"Enum attr: {original} → {new_value}")

    def _convert_enums_2_to_6(self, root: ET.Element, changes: List[str]):
        """Convert PySide2 enum syntax to PySide2."""
        # This is harder - need to determine the correct enum class
        # For now, keep PySide2 style (it's backward compatible in most cases)
        changes.append("PySide2 enum style kept (backward compatible)")

    def convert_python_file(self, py_file: str, target_version: str) -> bool:
        """
        Convert Python script to target PySide version.

        Args:
            py_file: Path to .py file
            target_version: "pyside6" or "pyside2"

        Returns:
            True if successful
        """
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            changes = []

            if target_version.lower() == "pyside2":
                # PySide2 → PySide2
                content, file_changes = self._convert_python_6_to_2(content)
            else:
                # PySide2 → PySide2
                content, file_changes = self._convert_python_2_to_6(content)

            changes.extend(file_changes)

            # Only write if changes were made
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.results.files_converted.append(py_file)
                self.results.changes_made[py_file] = changes
                return True
            else:
                self.results.warnings.append(f"{py_file}: No changes needed")
                return True

        except Exception as e:
            self.results.errors.append(f"{py_file}: {str(e)}")
            return False

    def _convert_python_6_to_2(self, content: str) -> Tuple[str, List[str]]:
        """Convert PySide2 Python code to PySide2."""
        changes = []

        # Import statements
        if "from PySide2" in content or "import PySide2" in content:
            content = content.replace("PySide2", "PySide2")
            changes.append("Imports: PySide2 → PySide2")

        # exec() → exec_()
        # Only replace if it's a Qt method call (has a dot before it or is QDialog.exec_())
        if re.search(r'\.exec\(\)', content):
            content = re.sub(r'\.exec\(\)', '.exec_()', content)
            changes.append("Method: .exec_() → .exec_()")

        # Qt.AlignCenter → Qt.AlignCenter
        if "Qt.AlignmentFlag" in content or "Qt.WindowType" in content or "Qt.ItemFlag" in content:
            content = re.sub(r'Qt\.(AlignmentFlag|WindowType|ItemFlag)\.', 'Qt.', content)
            changes.append("Enums: Qt.SomeFlag.Value → Qt.Value")

        # Remove Qt 6 specific flags
        qt6_specific = [
            # "Qt.AA_EnableHighDpiScaling  # Not needed in PySide2",
            # "Qt.AA_UseHighDpiPixmaps  # Not needed in PySide2"
        ]
        for flag in qt6_specific:
            if flag in content:
                # Comment out the line
                content = re.sub(
                    rf'^(\s*)(.*)({re.escape(flag)})',
                    r'\1# \2\3  # Not needed in PySide2',
                    content,
                    flags=re.MULTILINE
                )
                changes.append(f"Commented out Qt6-specific: {flag}")

        return content, changes

    def _convert_python_2_to_6(self, content: str) -> Tuple[str, List[str]]:
        """Convert PySide2 Python code to PySide2."""
        changes = []

        # Import statements
        if "from PySide2" in content or "import PySide2" in content:
            content = content.replace("PySide2", "PySide2")
            changes.append("Imports: PySide2 → PySide2")

        # exec_() → exec()
        if re.search(r'\.exec_\(\)', content):
            content = re.sub(r'\.exec_\(\)', '.exec_()', content)
            changes.append("Method: .exec_() → .exec_()")

        return content, changes

    def convert_directory(self, directory: str, target_version: str,
                         ui_files: bool = True, py_files: bool = True) -> ConversionResult:
        """
        Convert all files in a directory.

        Args:
            directory: Directory path
            target_version: "pyside6" or "pyside2"
            ui_files: Convert .ui files
            py_files: Convert .py files

        Returns:
            ConversionResult
        """
        path = Path(directory)

        if not path.exists():
            self.results.errors.append(f"Directory not found: {directory}")
            return self.results

        # Convert .ui files
        if ui_files:
            for ui_file in path.glob("*.ui"):
                print(f"Converting UI: {ui_file.name}")
                self.convert_ui_file(str(ui_file), target_version)

        # Convert .py files
        if py_files:
            for py_file in path.glob("*.py"):
                print(f"Converting Python: {py_file.name}")
                self.convert_python_file(str(py_file), target_version)

        return self.results

    def generate_report(self) -> str:
        """Generate conversion report."""
        lines = []
        lines.append("=" * 70)
        lines.append("PySide Version Conversion Report")
        lines.append("=" * 70)

        # Summary
        lines.append(f"\n✅ Files Converted: {len(self.results.files_converted)}")
        lines.append(f"⚠️  Warnings: {len(self.results.warnings)}")
        lines.append(f"❌ Errors: {len(self.results.errors)}")

        # Files converted
        if self.results.files_converted:
            lines.append("\n📁 Converted Files:")
            for file in self.results.files_converted:
                lines.append(f"   ✓ {file}")
                if file in self.results.changes_made:
                    for change in self.results.changes_made[file]:
                        lines.append(f"      - {change}")

        # Warnings
        if self.results.warnings:
            lines.append("\n⚠️  Warnings:")
            for warning in self.results.warnings:
                lines.append(f"   - {warning}")

        # Errors
        if self.results.errors:
            lines.append("\n❌ Errors:")
            for error in self.results.errors:
                lines.append(f"   - {error}")

        lines.append("\n" + "=" * 70)

        return "\n".join(lines)

    def _indent(self, elem, level=0):
        """Pretty print XML."""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


def main():
    """Command-line interface."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Convert between PySide2 and PySide2")
    parser.add_argument("target", choices=["pyside6", "pyside2"],
                       help="Target PySide version")
    parser.add_argument("--file", help="Single file to convert")
    parser.add_argument("--dir", help="Directory to convert (all .ui and .py files)")
    parser.add_argument("--ui-only", action="store_true", help="Only convert .ui files")
    parser.add_argument("--py-only", action="store_true", help="Only convert .py files")

    args = parser.parse_args()

    converter = PySideConverter()

    if args.file:
        file_path = Path(args.file)
        if file_path.suffix == ".ui":
            converter.convert_ui_file(args.file, args.target)
        elif file_path.suffix == ".py":
            converter.convert_python_file(args.file, args.target)
        else:
            print(f"Unknown file type: {file_path.suffix}")
            sys.exit(1)

    elif args.dir:
        converter.convert_directory(
            args.dir,
            args.target,
            ui_files=not args.py_only,
            py_files=not args.ui_only
        )
    else:
        print("Please specify --file or --dir")
        sys.exit(1)

    # Print report
    print("\n" + converter.generate_report())

    # Exit with error code if there were errors
    sys.exit(1 if converter.results.errors else 0)


if __name__ == "__main__":
    main()
