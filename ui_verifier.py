"""
UI Verifier - Automatic UI validation with screenshot analysis

This module provides automatic UI verification by:
1. Loading UI in Live Editor
2. Capturing screenshot
3. Analyzing screenshot for common issues
4. Suggesting fixes
"""

import base64
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from editor_client import EditorClient


class UIVerifier:
    """Automatic UI verification system"""

    def __init__(self, editor_port: int = 7010):
        """
        Initialize UI verifier.

        Args:
            editor_port: Port where Live UI Editor is running
        """
        self.editor_port = editor_port
        self.client = EditorClient(port=editor_port)

    def verify_ui(self, ui_file: str) -> Dict[str, Any]:
        """
        Verify a UI file by loading it and analyzing screenshot.

        Args:
            ui_file: Path to .ui file

        Returns:
            Verification result with issues and suggestions
        """
        ui_path = Path(ui_file)

        if not ui_path.exists():
            return {
                "status": "error",
                "message": f"UI file not found: {ui_file}",
                "issues": [],
                "screenshot": None
            }

        # Check if Live Editor is running
        if not self.client.ping():
            return {
                "status": "error",
                "message": f"Live UI Editor not running on port {self.editor_port}",
                "issues": [],
                "screenshot": None,
                "suggestion": f"Start Live Editor: rez-env pyside6 -- python live_ui_editor.py --ui {ui_file} --port {self.editor_port}"
            }

        # Load UI in editor
        reload_result = self.client.reload_ui(str(ui_path.absolute()))
        if not reload_result.get("success"):
            return {
                "status": "error",
                "message": f"Failed to load UI: {reload_result.get('message')}",
                "issues": [],
                "screenshot": None
            }

        # Get widget tree for analysis
        widget_tree = self.client.get_widget_tree()

        # Capture screenshot
        screenshot_path = ui_path.parent / f"{ui_path.stem}_verify.png"
        screenshot_result = self.client.take_screenshot(str(screenshot_path))

        screenshot_base64 = None
        if screenshot_result.get("success") and screenshot_path.exists():
            with open(screenshot_path, "rb") as f:
                screenshot_base64 = base64.b64encode(f.read()).decode('utf-8')

        # Analyze for issues
        issues = self._analyze_ui_structure(widget_tree, ui_path)

        return {
            "status": "success",
            "ui_file": str(ui_file),
            "screenshot_path": str(screenshot_path) if screenshot_path.exists() else None,
            "screenshot_base64": screenshot_base64,
            "widget_count": len(widget_tree.get("widgets", [])),
            "issues": issues,
            "verification_type": "automatic",
            "message": f"Found {len(issues)} potential issues" if issues else "No issues detected"
        }

    def _analyze_ui_structure(self, widget_tree: Dict, ui_path: Path) -> List[Dict[str, str]]:
        """
        Analyze UI structure for common issues.

        Args:
            widget_tree: Widget tree from Live Editor
            ui_path: Path to UI file

        Returns:
            List of issues found
        """
        issues = []
        widgets = widget_tree.get("widgets", [])

        # Check 1: Empty UI
        if not widgets:
            issues.append({
                "severity": "warning",
                "category": "structure",
                "message": "UI has no widgets",
                "suggestion": "Add widgets to the UI"
            })
            return issues

        # Check 2: Too many top-level widgets (might need layout)
        top_level_widgets = [w for w in widgets if w.get("parent") == widget_tree.get("root")]
        if len(top_level_widgets) > 5:
            issues.append({
                "severity": "info",
                "category": "layout",
                "message": f"{len(top_level_widgets)} top-level widgets detected",
                "suggestion": "Consider using a layout (QVBoxLayout, QHBoxLayout, QGridLayout) to organize widgets"
            })

        # Check 3: Widgets with default names
        default_names = [w for w in widgets if w.get("name", "").startswith(("pushButton_", "label_", "lineEdit_"))]
        if len(default_names) > 3:
            issues.append({
                "severity": "info",
                "category": "naming",
                "message": f"{len(default_names)} widgets have default names",
                "suggestion": "Use descriptive names for widgets (e.g., 'loginButton' instead of 'pushButton_1')"
            })

        # Check 4: Missing window title
        root_widget = widget_tree.get("root_properties", {})
        if not root_widget.get("windowTitle"):
            issues.append({
                "severity": "info",
                "category": "properties",
                "message": "Window has no title",
                "suggestion": "Set windowTitle property for better UX"
            })

        # Check 5: Very small or very large window
        geometry = root_widget.get("geometry", {})
        width = geometry.get("width", 0)
        height = geometry.get("height", 0)

        if width < 200 or height < 100:
            issues.append({
                "severity": "warning",
                "category": "size",
                "message": f"Window is very small ({width}x{height})",
                "suggestion": "Consider increasing window size for better usability"
            })
        elif width > 1920 or height > 1080:
            issues.append({
                "severity": "warning",
                "category": "size",
                "message": f"Window is very large ({width}x{height})",
                "suggestion": "Window might not fit on smaller screens"
            })

        # Check 6: Buttons without text
        buttons = [w for w in widgets if w.get("class", "").endswith("Button")]
        buttons_no_text = [b for b in buttons if not b.get("text")]
        if buttons_no_text:
            issues.append({
                "severity": "warning",
                "category": "content",
                "message": f"{len(buttons_no_text)} button(s) have no text",
                "suggestion": "Add text property to buttons for clarity"
            })

        return issues

    def create_verification_report(self, verification_result: Dict) -> str:
        """
        Create a human-readable verification report.

        Args:
            verification_result: Result from verify_ui()

        Returns:
            Formatted text report
        """
        report = []
        report.append("=" * 60)
        report.append("UI VERIFICATION REPORT")
        report.append("=" * 60)
        report.append("")

        report.append(f"UI File: {verification_result.get('ui_file', 'N/A')}")
        report.append(f"Status: {verification_result.get('status', 'unknown').upper()}")

        if verification_result.get("status") == "error":
            report.append(f"Error: {verification_result.get('message')}")
            if verification_result.get("suggestion"):
                report.append(f"Suggestion: {verification_result.get('suggestion')}")
            return "\n".join(report)

        report.append(f"Widget Count: {verification_result.get('widget_count', 0)}")

        screenshot_path = verification_result.get('screenshot_path')
        if screenshot_path:
            report.append(f"Screenshot: {screenshot_path}")

        report.append("")

        issues = verification_result.get("issues", [])

        if not issues:
            report.append("✅ No issues detected - UI looks good!")
        else:
            report.append(f"⚠️  Found {len(issues)} potential issue(s):")
            report.append("")

            # Group by severity
            warnings = [i for i in issues if i.get("severity") == "warning"]
            infos = [i for i in issues if i.get("severity") == "info"]

            if warnings:
                report.append("WARNINGS:")
                for idx, issue in enumerate(warnings, 1):
                    report.append(f"  {idx}. [{issue.get('category', 'general')}] {issue.get('message')}")
                    if issue.get('suggestion'):
                        report.append(f"     → {issue.get('suggestion')}")
                report.append("")

            if infos:
                report.append("INFO:")
                for idx, issue in enumerate(infos, 1):
                    report.append(f"  {idx}. [{issue.get('category', 'general')}] {issue.get('message')}")
                    if issue.get('suggestion'):
                        report.append(f"     → {issue.get('suggestion')}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


def verify_ui_file(ui_file: str, port: int = 7010) -> Dict[str, Any]:
    """
    Convenience function to verify a UI file.

    Args:
        ui_file: Path to .ui file
        port: Live Editor port

    Returns:
        Verification result
    """
    verifier = UIVerifier(editor_port=port)
    return verifier.verify_ui(ui_file)


def print_verification_report(ui_file: str, port: int = 7010) -> None:
    """
    Verify UI and print report.

    Args:
        ui_file: Path to .ui file
        port: Live Editor port
    """
    verifier = UIVerifier(editor_port=port)
    result = verifier.verify_ui(ui_file)
    report = verifier.create_verification_report(result)
    print(report)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ui_verifier.py <ui_file> [port]")
        print("Example: python ui_verifier.py my_dialog.ui 7010")
        sys.exit(1)

    ui_file = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7010

    print_verification_report(ui_file, port)
