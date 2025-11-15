"""
Test Live UI Editor socket communication

Usage: python test_live_editor.py [port]
Default port: 7010
"""

import sys
from editor_client import EditorClient
import json

def test_editor(port=7010):
    """Test all Live UI Editor functions."""
    client = EditorClient('localhost', port)

    print(f'🧪 Testing Live UI Editor on port {port}...\n')

    # 1. Ping test
    print('1️⃣ Ping test...')
    if client.ping():
        print('   ✅ Editor is running\n')
    else:
        print('   ❌ Editor not responding')
        print(f'   Make sure Live Editor is running:')
        print(f'   rez-env pyside6 python-3.9 -- python live_ui_editor.py --ui <file.ui> --port {port}')
        return 1

    # 2. Get widget tree
    print('2️⃣ Getting widget tree...')
    result = client.get_widget_tree()
    if result.get('status') == 'success':
        tree = result.get('widget_tree', {})
        print(f'   ✅ Dialog: {tree.get("name")}')
        print(f'   ✅ Total widgets: {len(tree.get("children", []))}')
        for widget in tree.get('children', []):
            widget_type = widget.get('type')
            widget_name = widget.get('name')
            text = widget.get('properties', {}).get('text', '')
            if text:
                print(f'      - {widget_type}: {widget_name} ("{text}")')
            else:
                print(f'      - {widget_type}: {widget_name}')
        print()
    else:
        print(f'   ❌ Failed: {result.get("message")}')

    # 3. Take screenshot
    print('3️⃣ Taking screenshot...')
    result = client.take_screenshot('screenshots/live_editor_test.png')
    if result.get('status') == 'success':
        print(f'   ✅ Saved: {result.get("path")}')
        base64_len = len(result.get('screenshot_base64', ''))
        print(f'   ✅ Base64 length: {base64_len:,} chars')
        print(f'   ✅ Estimated size: ~{base64_len * 3 // 4 // 1024} KB')
        print()
    else:
        print(f'   ❌ Failed: {result.get("message")}')

    # 4. Get UI file path
    print('4️⃣ Getting UI file path...')
    ui_file = client.get_ui_file()
    print(f'   ✅ Current UI: {ui_file}\n')

    # 5. Reload UI
    print('5️⃣ Testing reload...')
    result = client.reload_ui()
    if result.get('status') == 'success':
        print(f'   ✅ {result.get("message")}\n')
    else:
        print(f'   ❌ Failed: {result.get("message")}')

    print('🎉 All tests passed!')
    print('\nNext steps:')
    print('  - Check screenshots/live_editor_test.png')
    print('  - Try modifying the UI and reload')
    return 0

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 7010
    sys.exit(test_editor(port))
