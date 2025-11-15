"""
MCP Server for QtLiveDevTools

Provides MCP tools for Claude CLI to create and manipulate Qt UIs.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from ui_manager import UIManager, create_template_ui
from editor_client import EditorClient
from ui_comparator import UIComparator
from pyside_converter import PySideConverter


# MCP Server configuration
EDITOR_PORT = 7001
EDITOR_HOST = "localhost"


def create_ui_file(name: str, template: str = "dialog",
                   width: int = 400, height: int = 300) -> Dict[str, Any]:
    """
    Create a new .ui file from template.

    Args:
        name: UI file name (without .ui extension)
        template: Template type (dialog, mainwindow, widget)
        width: Initial width
        height: Initial height

    Returns:
        Result dictionary with file path and status
    """
    try:
        # Remove .ui extension if already present to avoid .ui.ui
        name_without_ext = name.removesuffix('.ui')
        output_path = f"{name_without_ext}.ui"
        create_template_ui(template, output_path, name=name_without_ext, width=width, height=height)

        return {
            "status": "success",
            "message": f"Created {template} UI",
            "file_path": output_path,
            "template": template,
            "dimensions": {"width": width, "height": height}
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def add_widget_to_ui(ui_file: str, widget_type: str, object_name: str,
                      parent_name: Optional[str] = None,
                      properties: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Add a widget to existing .ui file.

    Args:
        ui_file: Path to .ui file
        widget_type: Widget class (QPushButton, QLabel, QLineEdit, etc.)
        object_name: Unique object name
        parent_name: Parent widget name (optional)
        properties: Widget properties (optional)

    Returns:
        Result dictionary
    """
    try:
        if not Path(ui_file).exists():
            return {
                "status": "error",
                "message": f"UI file not found: {ui_file}"
            }

        manager = UIManager(ui_file)
        manager.add_widget(widget_type, object_name, parent_name, properties or {})
        manager.save()

        return {
            "status": "success",
            "message": f"Added {widget_type} '{object_name}' to {ui_file}",
            "widget_type": widget_type,
            "object_name": object_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def add_layout_to_ui(ui_file: str, layout_type: str, object_name: str,
                      parent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a layout to existing .ui file.

    Args:
        ui_file: Path to .ui file
        layout_type: Layout class (QVBoxLayout, QHBoxLayout, QGridLayout)
        object_name: Unique object name
        parent_name: Parent widget name (optional)

    Returns:
        Result dictionary
    """
    try:
        if not Path(ui_file).exists():
            return {
                "status": "error",
                "message": f"UI file not found: {ui_file}"
            }

        manager = UIManager(ui_file)
        manager.add_layout(layout_type, object_name, parent_name)
        manager.save()

        return {
            "status": "success",
            "message": f"Added {layout_type} '{object_name}' to {ui_file}",
            "layout_type": layout_type,
            "object_name": object_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def modify_widget_property(ui_file: str, widget_name: str,
                           property_name: str, value: Any) -> Dict[str, Any]:
    """
    Modify widget property in .ui file.

    Args:
        ui_file: Path to .ui file
        widget_name: Widget object name
        property_name: Property to modify
        value: New value

    Returns:
        Result dictionary
    """
    try:
        if not Path(ui_file).exists():
            return {
                "status": "error",
                "message": f"UI file not found: {ui_file}"
            }

        manager = UIManager(ui_file)
        manager.modify_property(widget_name, property_name, value)
        manager.save()

        return {
            "status": "success",
            "message": f"Modified {widget_name}.{property_name} = {value}",
            "widget_name": widget_name,
            "property_name": property_name,
            "value": value
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def get_ui_structure(ui_file: str) -> Dict[str, Any]:
    """
    Get widget hierarchy from .ui file.

    Args:
        ui_file: Path to .ui file

    Returns:
        Result dictionary with widget tree
    """
    try:
        if not Path(ui_file).exists():
            return {
                "status": "error",
                "message": f"UI file not found: {ui_file}"
            }

        manager = UIManager(ui_file)
        tree = manager.get_widget_tree()

        return {
            "status": "success",
            "widget_tree": tree,
            "ui_file": ui_file
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def preview_ui(ui_file: str, port: int = EDITOR_PORT) -> Dict[str, Any]:
    """
    Preview UI in Live Editor and take screenshot.

    Args:
        ui_file: Path to .ui file
        port: Editor port

    Returns:
        Result dictionary with screenshot
    """
    try:
        client = EditorClient(EDITOR_HOST, port)

        # Check if editor is running
        if not client.ping():
            return {
                "status": "error",
                "message": f"Live UI Editor not running on port {port}. "
                          f"Start with: rez-env pyside6 -- python live_ui_editor.py --ui {ui_file} --port {port}"
            }

        # Get current UI file
        current_ui = client.get_ui_file()
        if current_ui != str(Path(ui_file).absolute()):
            return {
                "status": "error",
                "message": f"Editor is showing different file: {current_ui}. "
                          f"Expected: {ui_file}"
            }

        # Reload and screenshot
        client.reload_ui()
        screenshot_path = f"screenshots/{Path(ui_file).stem}_preview.png"
        result = client.take_screenshot(screenshot_path)

        if result.get("status") == "success":
            return {
                "status": "success",
                "screenshot_path": result.get("path"),
                "screenshot_base64": result.get("screenshot_base64"),
                "ui_file": ui_file
            }
        else:
            return result

    except (ConnectionError, TimeoutError) as e:
        return {
            "status": "error",
            "message": f"Cannot connect to editor: {e}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def analyze_ui(ui_file: str, port: int = EDITOR_PORT) -> Dict[str, Any]:
    """
    Complete UI analysis (multi-layer).

    Args:
        ui_file: Path to .ui file
        port: Editor port

    Returns:
        Complete analysis including XML structure, widget tree, and screenshot
    """
    try:
        # Layer 1: XML Structure
        structure_result = get_ui_structure(ui_file)
        if structure_result.get("status") != "success":
            return structure_result

        # Layer 2 & 3: Runtime tree and screenshot (if editor is running)
        client = EditorClient(EDITOR_HOST, port)
        runtime_info = {}

        if client.ping():
            try:
                # Get runtime widget tree
                tree_result = client.get_widget_tree()
                if tree_result.get("status") == "success":
                    runtime_info["runtime_tree"] = tree_result.get("widget_tree")

                # Get screenshot
                screenshot_path = f"screenshots/{Path(ui_file).stem}_analysis.png"
                screenshot_result = client.take_screenshot(screenshot_path)
                if screenshot_result.get("status") == "success":
                    runtime_info["screenshot_path"] = screenshot_result.get("path")
                    runtime_info["screenshot_base64"] = screenshot_result.get("screenshot_base64")
            except:
                pass  # Editor is running but couldn't get info

        return {
            "status": "success",
            "ui_file": ui_file,
            "xml_structure": structure_result.get("widget_tree"),
            **runtime_info
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def compare_with_reference(reference_ui: str, target_ui: str, detailed: bool = True) -> Dict[str, Any]:
    """
    Compare target UI with reference UI.

    Args:
        reference_ui: Reference .ui file path
        target_ui: Target .ui file path
        detailed: Show detailed differences

    Returns:
        Comparison result with similarity score and differences
    """
    try:
        if not Path(reference_ui).exists():
            return {
                "status": "error",
                "message": f"Reference UI file not found: {reference_ui}"
            }

        if not Path(target_ui).exists():
            return {
                "status": "error",
                "message": f"Target UI file not found: {target_ui}"
            }

        comparator = UIComparator()
        comparator.load_reference(reference_ui)
        comparator.load_target(target_ui)

        result = comparator.compare()
        report = comparator.generate_report(result)

        response = {
            "status": "success",
            "reference_ui": reference_ui,
            "target_ui": target_ui,
            "similarity_score": result.similarity_score,
            "report": report
        }

        if detailed:
            response.update({
                "matching_widgets": result.matching_widgets,
                "missing_widgets": result.missing_widgets,
                "extra_widgets": result.extra_widgets,
                "property_differences": result.property_differences,
                "missing_specs": comparator.get_missing_widget_specs()
            })

        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def clone_from_reference(reference_ui: str, target_ui: str, verify: bool = True) -> Dict[str, Any]:
    """
    Clone UI from reference file.

    Args:
        reference_ui: Reference .ui file path
        target_ui: New target .ui file path
        verify: Verify after cloning

    Returns:
        Result with cloning status and verification
    """
    try:
        if not Path(reference_ui).exists():
            return {
                "status": "error",
                "message": f"Reference UI file not found: {reference_ui}"
            }

        # Load reference
        import shutil
        shutil.copy(reference_ui, target_ui)

        result = {
            "status": "success",
            "message": f"Cloned {reference_ui} to {target_ui}",
            "reference_ui": reference_ui,
            "target_ui": target_ui
        }

        # Verify if requested
        if verify:
            comparator = UIComparator()
            comparator.load_reference(reference_ui)
            comparator.load_target(target_ui)
            comparison = comparator.compare()

            result["verification"] = {
                "similarity_score": comparison.similarity_score,
                "verified": comparison.similarity_score >= 0.99
            }

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def convert_pyside_version(target_version: str, file_path: Optional[str] = None,
                          ui_files: bool = True, py_files: bool = True) -> Dict[str, Any]:
    """
    Convert between PySide6 and PySide2.

    Args:
        target_version: "pyside6" or "pyside2"
        file_path: File or directory path (current directory if None)
        ui_files: Convert .ui files
        py_files: Convert .py files

    Returns:
        Conversion result with report
    """
    try:
        target_version = target_version.lower()
        if target_version not in ["pyside6", "pyside2"]:
            return {
                "status": "error",
                "message": f"Invalid target version: {target_version}. Use 'pyside6' or 'pyside2'"
            }

        converter = PySideConverter()

        # Default to current directory if no path specified
        if file_path is None:
            file_path = "."

        path = Path(file_path)

        # Single file conversion
        if path.is_file():
            if path.suffix == ".ui":
                converter.convert_ui_file(str(path), target_version)
            elif path.suffix == ".py":
                converter.convert_python_file(str(path), target_version)
            else:
                return {
                    "status": "error",
                    "message": f"Unsupported file type: {path.suffix}"
                }

        # Directory conversion
        elif path.is_dir():
            converter.convert_directory(str(path), target_version, ui_files, py_files)

        else:
            return {
                "status": "error",
                "message": f"Path not found: {file_path}"
            }

        # Generate report
        report = converter.generate_report()

        return {
            "status": "success" if not converter.results.errors else "partial",
            "target_version": target_version,
            "files_converted": converter.results.files_converted,
            "changes_made": converter.results.changes_made,
            "warnings": converter.results.warnings,
            "errors": converter.results.errors,
            "report": report
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def send_command_to_editor(command: str, port: int = EDITOR_PORT, **params) -> Dict[str, Any]:
    """
    Send custom command to Live Editor.

    Args:
        command: Command action
        port: Editor port
        **params: Additional parameters

    Returns:
        Editor response
    """
    try:
        client = EditorClient(EDITOR_HOST, port)
        return client.send_command(command, **params)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# MCP Tool Definitions
# These would be registered with MCP SDK

MCP_TOOLS = {
    "create_ui_file": {
        "function": create_ui_file,
        "description": "Create a new .ui file from template",
        "parameters": {
            "name": "UI file name (without .ui extension)",
            "template": "Template type (dialog, mainwindow, widget)",
            "width": "Initial width (default 400)",
            "height": "Initial height (default 300)"
        }
    },
    "add_widget_to_ui": {
        "function": add_widget_to_ui,
        "description": "Add a widget to .ui file",
        "parameters": {
            "ui_file": "Path to .ui file",
            "widget_type": "Widget class (QPushButton, QLabel, etc.)",
            "object_name": "Unique object name",
            "parent_name": "Parent widget name (optional)",
            "properties": "Widget properties dict (optional)"
        }
    },
    "add_layout_to_ui": {
        "function": add_layout_to_ui,
        "description": "Add a layout to .ui file",
        "parameters": {
            "ui_file": "Path to .ui file",
            "layout_type": "Layout class (QVBoxLayout, QHBoxLayout, etc.)",
            "object_name": "Unique object name",
            "parent_name": "Parent widget name (optional)"
        }
    },
    "modify_widget_property": {
        "function": modify_widget_property,
        "description": "Modify widget property in .ui file",
        "parameters": {
            "ui_file": "Path to .ui file",
            "widget_name": "Widget object name",
            "property_name": "Property to modify",
            "value": "New value"
        }
    },
    "get_ui_structure": {
        "function": get_ui_structure,
        "description": "Get widget hierarchy from .ui file",
        "parameters": {
            "ui_file": "Path to .ui file"
        }
    },
    "preview_ui": {
        "function": preview_ui,
        "description": "Preview UI and take screenshot (requires Live Editor running)",
        "parameters": {
            "ui_file": "Path to .ui file",
            "port": "Editor port (default 7001)"
        }
    },
    "analyze_ui": {
        "function": analyze_ui,
        "description": "Complete multi-layer UI analysis",
        "parameters": {
            "ui_file": "Path to .ui file",
            "port": "Editor port (default 7001)"
        }
    },
    "send_command_to_editor": {
        "function": send_command_to_editor,
        "description": "Send custom command to Live Editor",
        "parameters": {
            "command": "Command action",
            "port": "Editor port (default 7001)",
            "**params": "Additional parameters"
        }
    },
    "compare_with_reference": {
        "function": compare_with_reference,
        "description": "Compare target UI with reference UI",
        "parameters": {
            "reference_ui": "Reference .ui file path",
            "target_ui": "Target .ui file path",
            "detailed": "Show detailed differences (default: True)"
        }
    },
    "clone_from_reference": {
        "function": clone_from_reference,
        "description": "Clone UI from reference file",
        "parameters": {
            "reference_ui": "Reference .ui file path",
            "target_ui": "New target .ui file path",
            "verify": "Verify after cloning (default: True)"
        }
    },
    "convert_pyside_version": {
        "function": convert_pyside_version,
        "description": "Convert between PySide6 and PySide2",
        "parameters": {
            "target_version": "Target version (pyside6 or pyside2)",
            "file_path": "File or directory path (optional)",
            "ui_files": "Convert .ui files (default: True)",
            "py_files": "Convert .py files (default: True)"
        }
    }
}


def verify_ui(ui_file: str, port: int = EDITOR_PORT) -> Dict[str, Any]:
    """
    Verify a UI file by loading it in Live Editor and capturing screenshot.

    Args:
        ui_file: Path to .ui file to verify
        port: Editor port

    Returns:
        Verification result with screenshot and analysis
    """
    try:
        # Use analyze_ui which already does everything we need
        result = analyze_ui(ui_file, port)

        if result.get("status") == "success":
            return {
                "status": "success",
                "message": f"UI verified: {ui_file}",
                "ui_file": ui_file,
                "analysis": result
            }
        else:
            return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Verification failed: {e}",
            "ui_file": ui_file
        }


def create_and_verify_ui(
    name: str,
    template: str = "dialog",
    width: int = 400,
    height: int = 300,
    widgets: Optional[List[Dict]] = None,
    port: int = EDITOR_PORT
) -> Dict[str, Any]:
    """
    Create a new UI file with widgets and automatically verify it.

    Args:
        name: UI file name (without .ui extension)
        template: Template type (dialog, mainwindow, widget)
        width: Initial width in pixels
        height: Initial height in pixels
        widgets: Optional list of widgets to add
        port: Editor port for verification

    Returns:
        Result with creation status and verification
    """
    try:
        # Create UI file
        create_result = create_ui_file(name, template, width, height)

        if create_result.get("status") != "success":
            return create_result

        ui_file = create_result.get("file_path")

        # Add widgets if provided
        if widgets:
            for widget_spec in widgets:
                widget_type = widget_spec.get("type")
                widget_name = widget_spec.get("name")
                properties = widget_spec.get("properties", {})
                parent = widget_spec.get("parent")

                if widget_type and widget_name:
                    add_result = add_widget_to_ui(
                        ui_file, widget_type, widget_name, parent, properties
                    )
                    if add_result.get("status") != "success":
                        return {
                            "status": "error",
                            "message": f"Failed to add widget {widget_name}: {add_result.get('message')}",
                            "ui_file": ui_file
                        }

        # Verify the created UI
        verify_result = verify_ui(ui_file, port)

        return {
            "status": "success",
            "message": f"UI created and verified: {ui_file}",
            "ui_file": ui_file,
            "creation": create_result,
            "verification": verify_result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Create and verify failed: {e}"
        }


if __name__ == "__main__":
    # Test MCP tools
    print("Testing MCP Tools...\n")

    # Test 1: Create UI
    print("1. Creating new dialog...")
    result = create_ui_file("test_dialog", "dialog", 500, 400)
    print(json.dumps(result, indent=2))

    # Test 2: Add widget
    print("\n2. Adding button...")
    result = add_widget_to_ui("test_dialog.ui", "QPushButton", "myButton",
                               properties={"text": "Click Me", "geometry": {"x": 150, "y": 200, "width": 100, "height": 30}})
    print(json.dumps(result, indent=2))

    # Test 3: Get structure
    print("\n3. Getting structure...")
    result = get_ui_structure("test_dialog.ui")
    print(json.dumps(result, indent=2))

    # Test 4: Analyze
    print("\n4. Analyzing UI...")
    result = analyze_ui("test_dialog.ui")
    print(json.dumps(result, indent=2))

    print("\n✓ MCP tools are working!")
    print("\nTo use with Live Editor:")
    print("  Terminal 1: rez-env pyside6 -- python live_ui_editor.py --ui test_dialog.ui --port 7001")
    print("  Terminal 2: python mcp_server.py")
