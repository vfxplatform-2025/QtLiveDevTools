#!/usr/bin/env python3
"""
UI Comparator - Reference-based UI comparison and validation

Analyzes reference UI and compares with target UI to verify similarity.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class WidgetInfo:
    """Widget information extracted from UI."""
    name: str
    type: str
    geometry: Dict[str, int]
    properties: Dict[str, Any]
    parent: Optional[str] = None
    children: List[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class ComparisonResult:
    """Result of UI comparison."""
    similarity_score: float  # 0.0 to 1.0
    matching_widgets: List[str]
    missing_widgets: List[str]
    extra_widgets: List[str]
    property_differences: Dict[str, Dict[str, Any]]
    layout_differences: List[str]

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "similarity_score": self.similarity_score,
            "matching_widgets": self.matching_widgets,
            "missing_widgets": self.missing_widgets,
            "extra_widgets": self.extra_widgets,
            "property_differences": self.property_differences,
            "layout_differences": self.layout_differences
        }


class UIComparator:
    """Compares UI files and provides similarity analysis."""

    def __init__(self):
        self.reference_widgets: Dict[str, WidgetInfo] = {}
        self.target_widgets: Dict[str, WidgetInfo] = {}

    def load_reference(self, ui_file: str) -> Dict[str, WidgetInfo]:
        """
        Load reference UI file and extract widget information.

        Args:
            ui_file: Path to reference .ui file

        Returns:
            Dictionary of widget name -> WidgetInfo
        """
        tree = ET.parse(ui_file)
        root = tree.getroot()

        widgets = {}
        self._extract_widgets(root, widgets)
        self.reference_widgets = widgets

        return widgets

    def load_target(self, ui_file: str) -> Dict[str, WidgetInfo]:
        """
        Load target UI file for comparison.

        Args:
            ui_file: Path to target .ui file

        Returns:
            Dictionary of widget name -> WidgetInfo
        """
        tree = ET.parse(ui_file)
        root = tree.getroot()

        widgets = {}
        self._extract_widgets(root, widgets)
        self.target_widgets = widgets

        return widgets

    def _extract_widgets(self, element: ET.Element, widgets: Dict[str, WidgetInfo],
                        parent_name: Optional[str] = None):
        """Recursively extract widgets from XML."""
        # Handle both top-level widget and nested widgets
        for widget_elem in element.findall(".//widget"):
            self._process_widget(widget_elem, widgets, parent_name)

    def _process_widget(self, element: ET.Element, widgets: Dict[str, WidgetInfo],
                       parent_name: Optional[str] = None):
        """Process a single widget element."""
        if element.tag == "widget":
            widget_type = element.get("class", "Unknown")
            widget_name = element.get("name", "unnamed")

            # Extract geometry
            geometry = {}
            geom_elem = element.find(".//property[@name='geometry']/rect")
            if geom_elem is not None:
                geometry = {
                    "x": int(geom_elem.find("x").text or 0),
                    "y": int(geom_elem.find("y").text or 0),
                    "width": int(geom_elem.find("width").text or 0),
                    "height": int(geom_elem.find("height").text or 0)
                }

            # Extract properties
            properties = {}
            for prop in element.findall("property"):
                prop_name = prop.get("name")
                if prop_name and prop_name != "geometry":
                    # Simple property extraction
                    for child in prop:
                        if child.text:
                            properties[prop_name] = child.text
                            break

            widget_info = WidgetInfo(
                name=widget_name,
                type=widget_type,
                geometry=geometry,
                properties=properties,
                parent=parent_name
            )

            widgets[widget_name] = widget_info

    def compare(self) -> ComparisonResult:
        """
        Compare reference and target UIs.

        Returns:
            ComparisonResult with detailed comparison
        """
        ref_names = set(self.reference_widgets.keys())
        target_names = set(self.target_widgets.keys())

        # Find matching, missing, and extra widgets
        matching = list(ref_names & target_names)
        missing = list(ref_names - target_names)
        extra = list(target_names - ref_names)

        # Compare properties of matching widgets
        property_diffs = {}
        layout_diffs = []

        for name in matching:
            ref_widget = self.reference_widgets[name]
            target_widget = self.target_widgets[name]

            diffs = self._compare_widgets(ref_widget, target_widget)
            if diffs:
                property_diffs[name] = diffs

        # Calculate similarity score
        total_widgets = len(ref_names)
        if total_widgets == 0:
            similarity = 0.0
        else:
            matching_score = len(matching) / total_widgets
            property_score = 1.0 - (len(property_diffs) / max(len(matching), 1))
            similarity = (matching_score * 0.7) + (property_score * 0.3)

        return ComparisonResult(
            similarity_score=similarity,
            matching_widgets=matching,
            missing_widgets=missing,
            extra_widgets=extra,
            property_differences=property_diffs,
            layout_differences=layout_diffs
        )

    def _compare_widgets(self, ref: WidgetInfo, target: WidgetInfo) -> Dict[str, Any]:
        """Compare two widgets and return differences."""
        diffs = {}

        # Compare type
        if ref.type != target.type:
            diffs["type"] = {"reference": ref.type, "target": target.type}

        # Compare geometry
        if ref.geometry != target.geometry:
            geom_diffs = {}
            for key in ["x", "y", "width", "height"]:
                ref_val = ref.geometry.get(key, 0)
                target_val = target.geometry.get(key, 0)
                if ref_val != target_val:
                    geom_diffs[key] = {"reference": ref_val, "target": target_val}
            if geom_diffs:
                diffs["geometry"] = geom_diffs

        # Compare properties
        all_props = set(ref.properties.keys()) | set(target.properties.keys())
        prop_diffs = {}
        for prop in all_props:
            ref_val = ref.properties.get(prop)
            target_val = target.properties.get(prop)
            if ref_val != target_val:
                prop_diffs[prop] = {"reference": ref_val, "target": target_val}

        if prop_diffs:
            diffs["properties"] = prop_diffs

        return diffs

    def generate_report(self, result: ComparisonResult) -> str:
        """
        Generate human-readable comparison report.

        Args:
            result: ComparisonResult from compare()

        Returns:
            Formatted report string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("UI Comparison Report")
        lines.append("=" * 70)
        lines.append(f"\n📊 Similarity Score: {result.similarity_score:.1%}\n")

        # Matching widgets
        lines.append(f"✅ Matching Widgets ({len(result.matching_widgets)}):")
        for name in result.matching_widgets[:10]:  # Show first 10
            lines.append(f"   - {name}")
        if len(result.matching_widgets) > 10:
            lines.append(f"   ... and {len(result.matching_widgets) - 10} more")

        # Missing widgets
        if result.missing_widgets:
            lines.append(f"\n❌ Missing Widgets ({len(result.missing_widgets)}):")
            for name in result.missing_widgets:
                ref_widget = self.reference_widgets[name]
                lines.append(f"   - {name} ({ref_widget.type})")

        # Extra widgets
        if result.extra_widgets:
            lines.append(f"\n➕ Extra Widgets ({len(result.extra_widgets)}):")
            for name in result.extra_widgets:
                target_widget = self.target_widgets[name]
                lines.append(f"   - {name} ({target_widget.type})")

        # Property differences
        if result.property_differences:
            lines.append(f"\n⚠️  Property Differences ({len(result.property_differences)}):")
            for widget_name, diffs in list(result.property_differences.items())[:5]:
                lines.append(f"\n   Widget: {widget_name}")
                for prop, diff in diffs.items():
                    if isinstance(diff, dict):
                        lines.append(f"      {prop}:")
                        for key, values in diff.items():
                            ref_val = values.get("reference", "N/A")
                            target_val = values.get("target", "N/A")
                            lines.append(f"         {key}: {ref_val} → {target_val}")

        lines.append("\n" + "=" * 70)

        return "\n".join(lines)

    def get_missing_widget_specs(self) -> List[Dict[str, Any]]:
        """
        Get specifications for missing widgets to help recreation.

        Returns:
            List of widget specifications
        """
        result = self.compare()
        specs = []

        for name in result.missing_widgets:
            widget = self.reference_widgets[name]
            specs.append({
                "name": name,
                "type": widget.type,
                "geometry": widget.geometry,
                "properties": widget.properties,
                "parent": widget.parent
            })

        return specs


def main():
    """Example usage."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python ui_comparator.py <reference.ui> <target.ui>")
        sys.exit(1)

    comparator = UIComparator()

    print("Loading reference UI...")
    comparator.load_reference(sys.argv[1])

    print("Loading target UI...")
    comparator.load_target(sys.argv[2])

    print("\nComparing...")
    result = comparator.compare()

    print("\n" + comparator.generate_report(result))

    # Show missing widget specs
    missing_specs = comparator.get_missing_widget_specs()
    if missing_specs:
        print("\n📋 Missing Widget Specifications:")
        print(json.dumps(missing_specs, indent=2))


if __name__ == "__main__":
    main()
