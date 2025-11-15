#!/usr/bin/env python3
"""
Integration test for QtLiveDevTools
Tests the full workflow: Create UI -> Start Editor -> Communicate -> Screenshot
"""

import sys
import time
import subprocess
from pathlib import Path
from editor_client import EditorClient


def test_editor_connection(port: int = 7010, max_retries: int = 10):
    """Test if Live Editor is running and responsive."""
    print(f"Testing connection to Live Editor on port {port}...")

    client = EditorClient(port=port)

    for i in range(max_retries):
        if client.ping():
            print(f"✓ Editor is running and responsive")
            return client
        print(f"  Attempt {i+1}/{max_retries}: Editor not responding, waiting...")
        time.sleep(1)

    print(f"✗ Editor is not running on port {port}")
    print(f"  Start with: ./start_live_editor.sh <ui_file> {port}")
    return None


def test_editor_commands(client: EditorClient):
    """Test various editor commands."""
    print("\nTesting editor commands...")

    # Test 1: Get UI file
    print("\n1. Get UI file:")
    result = client.get_ui_file()
    print(f"   Current UI: {result}")

    # Test 2: Get widget tree
    print("\n2. Get widget tree:")
    result = client.get_widget_tree()
    if result.get("status") == "success":
        tree = result.get("widget_tree", {})
        print(f"   ✓ Widget count: {len(tree.get('children', []))}")
        print(f"   Widget names: {[w.get('name') for w in tree.get('children', [])]}")
    else:
        print(f"   ✗ Failed: {result.get('message')}")

    # Test 3: Take screenshot
    print("\n3. Take screenshot:")
    screenshot_dir = Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)

    screenshot_path = screenshot_dir / "integration_test.png"
    result = client.take_screenshot(str(screenshot_path))

    if result.get("status") == "success":
        print(f"   ✓ Screenshot saved: {screenshot_path}")
        print(f"   File size: {screenshot_path.stat().st_size} bytes")

        # Check if base64 data is included
        base64_data = result.get("screenshot_base64", "")
        print(f"   Base64 length: {len(base64_data)} chars")
    else:
        print(f"   ✗ Failed: {result.get('message')}")

    # Test 4: Reload UI
    print("\n4. Reload UI:")
    result = client.reload_ui()
    if result.get("status") == "success":
        print(f"   ✓ UI reloaded successfully")
    else:
        print(f"   ✗ Failed: {result.get('message')}")

    return True


def main():
    """Main integration test."""
    print("=" * 60)
    print("QtLiveDevTools Integration Test")
    print("=" * 60)

    # Check if UI files exist
    ui_files = ["my_first_test.ui", "login_dialog.ui", "settings_dialog.ui"]
    print("\nChecking UI files:")
    for ui_file in ui_files:
        exists = Path(ui_file).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {ui_file}")

    # Test editor connection
    print("\n" + "-" * 60)
    client = test_editor_connection(port=7010)

    if not client:
        print("\n⚠ Live Editor is not running.")
        print("\nTo run this test:")
        print("  1. In Terminal 1: ./start_live_editor.sh my_first_test.ui 7010")
        print("  2. In Terminal 2: python test_integration.py")
        return 1

    # Test commands
    print("\n" + "-" * 60)
    test_editor_commands(client)

    print("\n" + "=" * 60)
    print("✓ Integration test completed")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
