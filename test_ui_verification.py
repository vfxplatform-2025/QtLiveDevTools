#!/usr/bin/env python
"""
Test UI Verification System

Tests the automatic UI verification feature.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ui_verifier import UIVerifier, verify_ui_file
from mcp_server import create_and_verify_ui


def test_verify_existing_ui():
    """Test verifying an existing UI file"""
    print("=" * 60)
    print("TEST 1: Verify Existing UI")
    print("=" * 60)

    ui_file = "my_first_test.ui"

    if not Path(ui_file).exists():
        print(f"❌ UI file not found: {ui_file}")
        print("   Run 'Create a UI dialog called my_first_test' in Claude CLI first")
        return False

    verifier = UIVerifier(editor_port=7010)
    result = verifier.verify_ui(ui_file)

    if result.get("status") == "error":
        print(f"\n⚠️  Error: {result.get('message')}")
        if result.get("suggestion"):
            print(f"   Suggestion: {result.get('suggestion')}")
        return False

    print(f"\n✅ Verification completed")
    print(f"   Widget count: {result.get('widget_count', 0)}")
    print(f"   Issues found: {len(result.get('issues', []))}")

    if result.get('screenshot_path'):
        print(f"   Screenshot: {result.get('screenshot_path')}")

    # Print report
    report = verifier.create_verification_report(result)
    print("\n" + report)

    return True


def test_create_and_verify():
    """Test creating UI with automatic verification"""
    print("\n" + "=" * 60)
    print("TEST 2: Create and Verify UI")
    print("=" * 60)

    # Create a test UI with some potential issues
    result = create_and_verify_ui(
        name="test_verification",
        template="dialog",
        width=300,  # Small width (potential issue)
        height=200,  # Small height (potential issue)
        widgets=[
            {
                "type": "QPushButton",
                "name": "pushButton_1",  # Default name (potential issue)
                "properties": {
                    "text": ""  # No text (potential issue)
                }
            },
            {
                "type": "QPushButton",
                "name": "pushButton_2",  # Default name (potential issue)
                "properties": {
                    "text": ""  # No text (potential issue)
                }
            },
            {
                "type": "QLabel",
                "name": "label_1",  # Default name (potential issue)
                "properties": {
                    "text": "Test Label"
                }
            }
        ],
        port=7010
    )

    if result.get("status") == "error":
        print(f"\n❌ Error: {result.get('message')}")
        return False

    print(f"\n✅ Created and verified: {result.get('ui_file')}")

    verification = result.get("verification", {})
    print(f"   Widget count: {verification.get('widget_count', 0)}")
    print(f"   Issues found: {len(result.get('issues', []))}")

    # Print issues
    if result.get('issues'):
        print("\n   Issues detected:")
        for idx, issue in enumerate(result['issues'], 1):
            severity = issue.get('severity', 'info').upper()
            category = issue.get('category', 'general')
            message = issue.get('message', '')
            print(f"     {idx}. [{severity}] [{category}] {message}")
            if issue.get('suggestion'):
                print(f"        → {issue.get('suggestion')}")

    # Print full report
    if result.get('report'):
        print("\n" + result['report'])

    return True


def test_create_good_ui():
    """Test creating a well-designed UI (should have no/few issues)"""
    print("\n" + "=" * 60)
    print("TEST 3: Create Good UI (Minimal Issues)")
    print("=" * 60)

    result = create_and_verify_ui(
        name="test_good_ui",
        template="dialog",
        width=500,  # Good size
        height=400,  # Good size
        widgets=[
            {
                "type": "QLabel",
                "name": "titleLabel",  # Descriptive name
                "properties": {
                    "text": "Login Dialog",
                    "font": {
                        "_type": "font",
                        "pointsize": "14",
                        "bold": "true"
                    }
                }
            },
            {
                "type": "QLineEdit",
                "name": "usernameEdit",  # Descriptive name
                "properties": {
                    "placeholderText": "Username"
                }
            },
            {
                "type": "QLineEdit",
                "name": "passwordEdit",  # Descriptive name
                "properties": {
                    "placeholderText": "Password",
                    "echoMode": "Password"
                }
            },
            {
                "type": "QPushButton",
                "name": "loginButton",  # Descriptive name
                "properties": {
                    "text": "Login"  # Has text
                }
            },
            {
                "type": "QPushButton",
                "name": "cancelButton",  # Descriptive name
                "properties": {
                    "text": "Cancel"  # Has text
                }
            }
        ],
        port=7010
    )

    if result.get("status") == "error":
        print(f"\n❌ Error: {result.get('message')}")
        return False

    print(f"\n✅ Created and verified: {result.get('ui_file')}")

    issues = result.get('issues', [])
    print(f"   Issues found: {len(issues)}")

    if issues:
        print("\n   Issues:")
        for issue in issues:
            print(f"     - [{issue.get('severity')}] {issue.get('message')}")
    else:
        print("\n   ✨ Perfect! No issues detected!")

    return True


def main():
    """Run all tests"""
    print("\n" + "🧪 UI VERIFICATION SYSTEM TESTS")
    print("=" * 60)
    print("\nNote: Make sure Live UI Editor is running on port 7010:")
    print("  rez-env pyside6 -- python live_ui_editor.py --ui empty_dialog.ui --port 7010")
    print()

    results = []

    # Test 1: Verify existing UI
    results.append(("Verify Existing UI", test_verify_existing_ui()))

    # Test 2: Create with issues
    results.append(("Create with Issues", test_create_and_verify()))

    # Test 3: Create good UI
    results.append(("Create Good UI", test_create_good_ui()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)

    print(f"\nPassed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
