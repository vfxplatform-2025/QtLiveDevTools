#!/usr/bin/env python3
"""
Advanced Features Test
Tests layouts, stylesheets, and complex UI structures
"""

import sys
from pathlib import Path
from mcp_server import (
    create_ui_file,
    add_widget_to_ui,
    add_layout_to_ui,
    modify_widget_property,
    get_ui_structure
)


def test_layouts():
    """Test different layout types."""
    print("\n" + "=" * 60)
    print("Testing Layouts")
    print("=" * 60)

    ui_file = "layout_test.ui"

    # Create UI with layouts
    print("\n[1] Creating UI with VBoxLayout...")
    create_ui_file(ui_file, template="dialog", width=400, height=500)

    # Add main vertical layout
    print("\n[2] Adding QVBoxLayout...")
    result = add_layout_to_ui(ui_file, layout_type="QVBoxLayout", object_name="mainLayout")
    print(f"  {result}")

    # Add horizontal layout for buttons
    print("\n[3] Adding QHBoxLayout for buttons...")
    result = add_layout_to_ui(ui_file, layout_type="QHBoxLayout", object_name="buttonLayout")
    print(f"  {result}")

    # Add grid layout
    print("\n[4] Adding QGridLayout for form...")
    result = add_layout_to_ui(ui_file, layout_type="QGridLayout", object_name="formLayout")
    print(f"  {result}")

    # Add some widgets
    print("\n[5] Adding widgets to test layouts...")
    add_widget_to_ui(
        ui_file,
        widget_type="QLabel",
        object_name="headerLabel",
        properties={"text": "레이아웃 테스트", "geometry": {"x": 100, "y": 20, "width": 200, "height": 30}}
    )

    add_widget_to_ui(
        ui_file,
        widget_type="QPushButton",
        object_name="button1",
        properties={"text": "버튼 1", "geometry": {"x": 50, "y": 100, "width": 100, "height": 40}}
    )

    add_widget_to_ui(
        ui_file,
        widget_type="QPushButton",
        object_name="button2",
        properties={"text": "버튼 2", "geometry": {"x": 160, "y": 100, "width": 100, "height": 40}}
    )

    add_widget_to_ui(
        ui_file,
        widget_type="QPushButton",
        object_name="button3",
        properties={"text": "버튼 3", "geometry": {"x": 270, "y": 100, "width": 100, "height": 40}}
    )

    # Show structure
    print("\n[6] Final structure:")
    structure = get_ui_structure(ui_file)
    widget_tree = structure.get("widget_tree", {})

    print(f"  Dialog: {widget_tree.get('name')}")
    print(f"  Children: {len(widget_tree.get('children', []))}")
    for child in widget_tree.get("children", []):
        name = child.get("name")
        wtype = child.get("type")
        print(f"    - {name} ({wtype})")

    print(f"\n  ✓ Layout test UI created: {ui_file}")


def test_complex_ui():
    """Test creating a complex UI with multiple widget types."""
    print("\n" + "=" * 60)
    print("Testing Complex UI")
    print("=" * 60)

    ui_file = "complex_ui.ui"

    print("\n[1] Creating complex UI...")
    create_ui_file(ui_file, template="mainwindow", width=800, height=600)

    # Add various widgets
    widgets = [
        ("QLabel", "titleLabel", {"text": "복잡한 UI 예제", "geometry": {"x": 300, "y": 20, "width": 200, "height": 40}}),
        ("QLineEdit", "searchInput", {"geometry": {"x": 50, "y": 80, "width": 300, "height": 30}}),
        ("QPushButton", "searchButton", {"text": "검색", "geometry": {"x": 360, "y": 80, "width": 80, "height": 30}}),
        ("QListWidget", "resultsList", {"geometry": {"x": 50, "y": 130, "width": 400, "height": 300}}),
        ("QTextEdit", "detailsText", {"geometry": {"x": 470, "y": 130, "width": 300, "height": 300}}),
        ("QProgressBar", "progressBar", {"geometry": {"x": 50, "y": 450, "width": 720, "height": 25}}),
        ("QCheckBox", "option1", {"text": "옵션 1", "geometry": {"x": 50, "y": 490, "width": 100, "height": 25}}),
        ("QCheckBox", "option2", {"text": "옵션 2", "geometry": {"x": 160, "y": 490, "width": 100, "height": 25}}),
        ("QRadioButton", "radio1", {"text": "라디오 1", "geometry": {"x": 270, "y": 490, "width": 100, "height": 25}}),
        ("QRadioButton", "radio2", {"text": "라디오 2", "geometry": {"x": 380, "y": 490, "width": 100, "height": 25}}),
        ("QPushButton", "okButton", {"text": "확인", "geometry": {"x": 580, "y": 540, "width": 90, "height": 40}}),
        ("QPushButton", "cancelButton", {"text": "취소", "geometry": {"x": 680, "y": 540, "width": 90, "height": 40}}),
    ]

    print(f"\n[2] Adding {len(widgets)} widgets...")
    for i, (widget_type, object_name, properties) in enumerate(widgets, 1):
        result = add_widget_to_ui(ui_file, widget_type, object_name, properties)
        status = "✓" if result.get("status") == "success" else "✗"
        print(f"  {status} {i:2d}. {object_name} ({widget_type})")

    # Show structure
    print("\n[3] Final structure:")
    structure = get_ui_structure(ui_file)
    widget_tree = structure.get("widget_tree", {})

    print(f"  MainWindow: {widget_tree.get('name')}")
    print(f"  Total widgets: {len(widget_tree.get('children', []))}")

    # Count by type
    widget_types = {}
    for child in widget_tree.get("children", []):
        wtype = child.get("type")
        widget_types[wtype] = widget_types.get(wtype, 0) + 1

    print(f"\n  Widget types:")
    for wtype, count in sorted(widget_types.items()):
        print(f"    - {wtype}: {count}")

    print(f"\n  ✓ Complex UI created: {ui_file}")


def test_widget_modifications():
    """Test modifying widget properties."""
    print("\n" + "=" * 60)
    print("Testing Widget Modifications")
    print("=" * 60)

    ui_file = "modification_test.ui"

    print("\n[1] Creating test UI...")
    create_ui_file(ui_file, template="dialog", width=400, height=300)

    print("\n[2] Adding test widgets...")
    add_widget_to_ui(
        ui_file,
        widget_type="QLabel",
        object_name="testLabel",
        properties={"text": "초기 텍스트", "geometry": {"x": 100, "y": 100, "width": 200, "height": 30}}
    )

    add_widget_to_ui(
        ui_file,
        widget_type="QPushButton",
        object_name="testButton",
        properties={"text": "버튼", "geometry": {"x": 150, "y": 150, "width": 100, "height": 40}}
    )

    print("\n[3] Modifying properties...")
    modifications = [
        ("testLabel", "text", "수정된 텍스트"),
        ("testButton", "text", "클릭하세요"),
    ]

    for widget_name, property_name, value in modifications:
        result = modify_widget_property(ui_file, widget_name, property_name, value)
        status = "✓" if result.get("status") == "success" else "✗"
        print(f"  {status} {widget_name}.{property_name} = '{value}'")

    print(f"\n  ✓ Modifications complete: {ui_file}")


def main():
    """Main entry point."""
    print("QtLiveDevTools Advanced Features Test")
    print()

    # Create test directory
    Path("screenshots").mkdir(exist_ok=True)

    # Run tests
    test_layouts()
    test_complex_ui()
    test_widget_modifications()

    print("\n" + "=" * 60)
    print("✓ All advanced feature tests completed")
    print("=" * 60)
    print("\nCreated files:")
    print("  - layout_test.ui")
    print("  - complex_ui.ui")
    print("  - modification_test.ui")
    print("\nYou can open these in Qt Designer or Live Editor")

    return 0


if __name__ == "__main__":
    sys.exit(main())
