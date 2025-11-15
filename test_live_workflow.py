#!/usr/bin/env python3
"""
Live Workflow Test
Demonstrates real-time UI modification workflow with Live Editor
"""

import sys
import time
from pathlib import Path
from editor_client import EditorClient
from mcp_server import (
    create_ui_file,
    add_widget_to_ui,
    modify_widget_property,
    get_ui_structure
)


def wait_for_editor(port: int = 7010):
    """Wait for Live Editor to be ready."""
    client = EditorClient(port=port)
    print("Waiting for Live Editor...")

    for i in range(30):
        if client.ping():
            print("✓ Live Editor is ready")
            return client
        time.sleep(1)

    print("✗ Live Editor not found")
    return None


def demonstrate_workflow(client: EditorClient):
    """Demonstrate live UI modification workflow."""
    print("\n" + "=" * 60)
    print("Live UI Modification Workflow Demo")
    print("=" * 60)

    ui_file = "workflow_demo.ui"

    # Step 1: Create new UI
    print("\n[Step 1] Creating new UI file...")
    result = create_ui_file(ui_file, template="dialog", width=500, height=400)
    print(f"  {result}")

    # Reload in editor
    client.reload_ui()
    time.sleep(0.5)

    # Step 2: Add title label
    print("\n[Step 2] Adding title label...")
    result = add_widget_to_ui(
        ui_file,
        widget_type="QLabel",
        object_name="titleLabel",
        properties={"text": "실시간 UI 데모", "geometry": {"x": 150, "y": 20, "width": 200, "height": 40}}
    )
    print(f"  {result}")

    # Reload and screenshot
    client.reload_ui()
    time.sleep(0.5)
    screenshot1 = client.take_screenshot("screenshots/workflow_step2.png")
    print(f"  Screenshot: {screenshot1.get('path')}")

    # Step 3: Add input fields
    print("\n[Step 3] Adding input fields...")
    add_widget_to_ui(
        ui_file,
        widget_type="QLabel",
        object_name="nameLabel",
        properties={"text": "이름:", "geometry": {"x": 50, "y": 100, "width": 80, "height": 25}}
    )
    add_widget_to_ui(
        ui_file,
        widget_type="QLineEdit",
        object_name="nameInput",
        properties={"geometry": {"x": 140, "y": 100, "width": 300, "height": 25}}
    )

    client.reload_ui()
    time.sleep(0.5)
    screenshot2 = client.take_screenshot("screenshots/workflow_step3.png")
    print(f"  Screenshot: {screenshot2.get('path')}")

    # Step 4: Add buttons
    print("\n[Step 4] Adding buttons...")
    add_widget_to_ui(
        ui_file,
        widget_type="QPushButton",
        object_name="submitButton",
        properties={"text": "제출", "geometry": {"x": 200, "y": 300, "width": 100, "height": 40}}
    )
    add_widget_to_ui(
        ui_file,
        widget_type="QPushButton",
        object_name="cancelButton",
        properties={"text": "취소", "geometry": {"x": 310, "y": 300, "width": 100, "height": 40}}
    )

    client.reload_ui()
    time.sleep(0.5)
    screenshot3 = client.take_screenshot("screenshots/workflow_step4.png")
    print(f"  Screenshot: {screenshot3.get('path')}")

    # Step 5: Modify title
    print("\n[Step 5] Modifying title text...")
    result = modify_widget_property(ui_file, "titleLabel", "text", "완성된 UI 💡")
    print(f"  {result}")

    client.reload_ui()
    time.sleep(0.5)
    screenshot4 = client.take_screenshot("screenshots/workflow_final.png")
    print(f"  Screenshot: {screenshot4.get('path')}")

    # Step 6: Show final structure
    print("\n[Step 6] Final UI structure:")
    structure = get_ui_structure(ui_file)
    widget_tree = structure.get("widget_tree", {})
    print(f"  Dialog: {widget_tree.get('name')} ({widget_tree.get('type')})")
    print(f"  Widgets:")
    for child in widget_tree.get("children", []):
        name = child.get("name")
        wtype = child.get("type")
        text = child.get("properties", {}).get("text", "")
        if text:
            print(f"    - {name} ({wtype}): '{text}'")
        else:
            print(f"    - {name} ({wtype})")

    print("\n" + "=" * 60)
    print("✓ Workflow demo completed")
    print("  Check screenshots/ directory for step-by-step images")
    print("=" * 60)


def main():
    """Main entry point."""
    print("QtLiveDevTools Live Workflow Demo")
    print("\nPrerequisite: Live Editor must be running")
    print("Start with: ./start_live_editor.sh workflow_demo.ui 7010\n")

    # Wait for editor
    client = wait_for_editor(port=7010)
    if not client:
        print("\n✗ Cannot proceed without Live Editor")
        return 1

    # Create screenshots directory
    Path("screenshots").mkdir(exist_ok=True)

    # Run workflow demo
    demonstrate_workflow(client)

    return 0


if __name__ == "__main__":
    sys.exit(main())
