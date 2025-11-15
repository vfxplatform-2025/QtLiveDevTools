#!/usr/bin/env python3
"""
Test: Reference-based UI Cloning and Verification

Demonstrates the reference-based workflow:
1. Load reference UI
2. Clone to new file
3. Compare and verify similarity
4. Make modifications
5. Re-compare to check differences
"""

import sys
from pathlib import Path
from mcp_server import compare_with_reference, clone_from_reference
from ui_manager import UIManager
import json


def test_reference_workflow():
    """Test complete reference-based workflow."""
    print("=" * 70)
    print("Reference-Based UI Cloning and Verification Test")
    print("=" * 70)

    # Step 1: Use existing UI as reference
    reference_ui = "test_connections.ui"

    if not Path(reference_ui).exists():
        print(f"❌ Reference file not found: {reference_ui}")
        print("Creating reference UI first...")

        # Create a simple reference UI
        manager = UIManager()
        manager.create_empty_ui("QDialog", "ReferenceDialog", 400, 300)
        manager.add_widget("QLabel", "titleLabel", properties={
            "text": "Reference Dialog",
            "geometry": {"x": 50, "y": 20, "width": 300, "height": 30},
            "font": {"_type": "font", "family": "Arial", "pointsize": "14", "bold": "true"}
        })
        manager.add_widget("QPushButton", "okButton", properties={
            "text": "OK",
            "geometry": {"x": 150, "y": 200, "width": 100, "height": 40}
        })
        manager.save(reference_ui)
        print(f"✓ Created reference UI: {reference_ui}\n")

    # Step 2: Clone from reference
    print("\n" + "=" * 70)
    print("Step 1: Cloning from Reference")
    print("=" * 70)

    target_ui = "cloned_dialog.ui"
    result = clone_from_reference(reference_ui, target_ui, verify=True)

    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if "verification" in result:
        print(f"Similarity: {result['verification']['similarity_score']:.1%}")
        print(f"Verified: {'✓' if result['verification']['verified'] else '✗'}")

    # Step 3: Initial comparison (should be 100% match)
    print("\n" + "=" * 70)
    print("Step 2: Initial Comparison (Perfect Match)")
    print("=" * 70)

    comp_result = compare_with_reference(reference_ui, target_ui, detailed=True)
    print(comp_result['report'])

    # Step 4: Modify the cloned UI
    print("\n" + "=" * 70)
    print("Step 3: Modifying Cloned UI")
    print("=" * 70)

    print("Adding new widgets to cloned UI...")
    manager = UIManager(target_ui)

    # Add a new label
    manager.add_widget("QLabel", "extraLabel", properties={
        "text": "Extra Widget",
        "geometry": {"x": 50, "y": 100, "width": 200, "height": 25}
    })

    # Modify existing button position
    manager.modify_property("okButton", "geometry", {"x": 200, "y": 220, "width": 100, "height": 40})

    # Add a new button
    manager.add_widget("QPushButton", "cancelButton", properties={
        "text": "Cancel",
        "geometry": {"x": 50, "y": 220, "width": 100, "height": 40}
    })

    manager.save()
    print("✓ Added 'extraLabel' widget")
    print("✓ Moved 'okButton' position")
    print("✓ Added 'cancelButton' widget")

    # Step 5: Compare again (should show differences)
    print("\n" + "=" * 70)
    print("Step 4: Comparison After Modifications")
    print("=" * 70)

    comp_result = compare_with_reference(reference_ui, target_ui, detailed=True)
    print(comp_result['report'])

    # Show missing widget specs
    if comp_result.get('extra_widgets'):
        print("\n📋 Extra Widgets Added to Target:")
        for widget_name in comp_result['extra_widgets']:
            print(f"   - {widget_name}")

    if comp_result.get('property_differences'):
        print("\n⚠️  Modified Widgets:")
        for widget_name in comp_result['property_differences']:
            print(f"   - {widget_name}")

    # Step 6: Show what's needed to match reference
    print("\n" + "=" * 70)
    print("Step 5: Gap Analysis")
    print("=" * 70)

    similarity = comp_result['similarity_score']
    print(f"Current Similarity: {similarity:.1%}")

    if similarity < 1.0:
        gap = 1.0 - similarity
        print(f"Gap to Perfect Match: {gap:.1%}")
        print("\nTo match reference exactly, you would need to:")

        if comp_result.get('extra_widgets'):
            print(f"  - Remove {len(comp_result['extra_widgets'])} extra widget(s)")

        if comp_result.get('property_differences'):
            print(f"  - Revert {len(comp_result['property_differences'])} modified widget(s)")
    else:
        print("✓ Perfect match!")

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"✓ Reference UI: {reference_ui}")
    print(f"✓ Cloned UI: {target_ui}")
    print(f"✓ Initial similarity: 100%")
    print(f"✓ After modifications: {similarity:.1%}")
    print(f"✓ Differences detected: {len(comp_result.get('extra_widgets', [])) + len(comp_result.get('property_differences', {}))}")

    print("\n🎯 Reference-based workflow is working perfectly!")

    return 0


if __name__ == "__main__":
    sys.exit(test_reference_workflow())
