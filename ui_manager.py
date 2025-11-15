"""
UI Manager - .ui file creation and manipulation via XML

Handles Qt Designer .ui file format (XML) for PySide6 applications.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, Optional, List


class UIManager:
    """Manages .ui file creation and modification through XML manipulation."""

    def __init__(self, ui_file: Optional[str] = None):
        """
        Initialize UIManager.

        Args:
            ui_file: Path to existing .ui file (optional)
        """
        self.ui_file = ui_file
        self.tree = None
        self.root = None

        if ui_file and Path(ui_file).exists():
            self.load(ui_file)

    def load(self, ui_file: str):
        """Load existing .ui file."""
        self.ui_file = ui_file
        self.tree = ET.parse(ui_file)
        self.root = self.tree.getroot()

    def save(self, output_path: Optional[str] = None):
        """
        Save .ui file.

        Args:
            output_path: Output file path (defaults to self.ui_file)
        """
        if output_path is None:
            output_path = self.ui_file

        if output_path is None:
            raise ValueError("No output path specified")

        # Ensure proper XML formatting
        self._indent(self.root)
        self.tree.write(output_path, encoding='utf-8', xml_declaration=True)

    def _indent(self, elem, level=0):
        """Add indentation to XML for readable output."""
        indent = "\n" + "  " * level
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self._indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent

    def create_empty_ui(self, widget_type: str = "QDialog", name: str = "Dialog",
                       width: int = 400, height: int = 300):
        """
        Create a new empty .ui file.

        Args:
            widget_type: Root widget type (QDialog, QMainWindow, QWidget)
            name: Widget object name
            width: Initial width
            height: Initial height
        """
        # Create root <ui> element
        self.root = ET.Element("ui", version="4.0")
        self.tree = ET.ElementTree(self.root)

        # Add class name
        class_elem = ET.SubElement(self.root, "class")
        class_elem.text = name

        # Create main widget
        widget = ET.SubElement(self.root, "widget", {
            "class": widget_type,
            "name": name
        })

        # Add geometry
        geometry = ET.SubElement(widget, "property", name="geometry")
        rect = ET.SubElement(geometry, "rect")
        ET.SubElement(rect, "x").text = "0"
        ET.SubElement(rect, "y").text = "0"
        ET.SubElement(rect, "width").text = str(width)
        ET.SubElement(rect, "height").text = str(height)

        # Add window title
        title_prop = ET.SubElement(widget, "property", name="windowTitle")
        ET.SubElement(title_prop, "string").text = name

        return self

    def add_widget(self, widget_type: str, object_name: str,
                   parent_name: str = None, properties: Dict[str, Any] = None):
        """
        Add a widget to the UI.

        Args:
            widget_type: Widget class (QPushButton, QLabel, QLineEdit, etc.)
            object_name: Unique object name for the widget
            parent_name: Parent widget name (None for root widget)
            properties: Dictionary of property_name: value pairs

        Returns:
            The created widget element
        """
        # Find parent widget
        if parent_name:
            parent = self._find_widget(parent_name)
            if parent is None:
                raise ValueError(f"Parent widget '{parent_name}' not found")
        else:
            # Use root widget
            parent = self.root.find(".//widget")

        # Create widget element
        widget = ET.SubElement(parent, "widget", {
            "class": widget_type,
            "name": object_name
        })

        # Add properties
        if properties:
            for prop_name, value in properties.items():
                self._add_property(widget, prop_name, value)

        return widget

    def add_layout(self, layout_type: str, object_name: str, parent_name: str = None):
        """
        Add a layout to the UI.

        Args:
            layout_type: Layout class (QVBoxLayout, QHBoxLayout, QGridLayout)
            object_name: Unique object name for the layout
            parent_name: Parent widget name

        Returns:
            The created layout element
        """
        if parent_name:
            parent = self._find_widget(parent_name)
            if parent is None:
                raise ValueError(f"Parent widget '{parent_name}' not found")
        else:
            parent = self.root.find(".//widget")

        # Create layout element
        layout = ET.SubElement(parent, "layout", {
            "class": layout_type,
            "name": object_name
        })

        return layout

    def add_connection(self, sender: str, signal: str, receiver: str, slot: str):
        """
        Add a signal/slot connection.

        Args:
            sender: Sender widget object name
            signal: Signal name (e.g., "clicked()")
            receiver: Receiver widget object name
            slot: Slot name (e.g., "accept()")
        """
        # Find or create connections section
        connections = self.root.find("connections")
        if connections is None:
            connections = ET.SubElement(self.root, "connections")

        # Add connection
        connection = ET.SubElement(connections, "connection")
        ET.SubElement(connection, "sender").text = sender
        ET.SubElement(connection, "signal").text = signal
        ET.SubElement(connection, "receiver").text = receiver
        ET.SubElement(connection, "slot").text = slot

        return connection

    def add_action(self, object_name: str, properties: Dict[str, Any] = None):
        """
        Add a QAction to the UI.

        Args:
            object_name: Action object name
            properties: Action properties (text, icon, shortcut, etc.)
        """
        # Find or create widget section
        widget = self.root.find(".//widget")
        if widget is None:
            raise ValueError("No widget found in UI")

        # Create action
        action = ET.SubElement(widget, "action", name=object_name)

        # Add properties
        if properties:
            for prop_name, value in properties.items():
                self._add_property(action, prop_name, value)

        return action

    def add_resource(self, resource_path: str):
        """
        Add a resource reference (.qrc file).

        Args:
            resource_path: Path to .qrc file
        """
        # Find or create resources section
        resources = self.root.find("resources")
        if resources is None:
            resources = ET.SubElement(self.root, "resources")

        # Add include
        include = ET.SubElement(resources, "include", location=resource_path)
        return include

    def add_stylesheet(self, qss: str):
        """
        Add stylesheet (QSS) to the main widget.

        Args:
            qss: Qt Stylesheet string
        """
        widget = self.root.find(".//widget")
        if widget is None:
            raise ValueError("No widget found in UI")

        # Add or update styleSheet property
        self._add_property(widget, "styleSheet", qss)

    def add_spacer(self, parent_layout_name: str, orientation: str = "vertical",
                   size_hint: Dict[str, int] = None):
        """
        Add a spacer item to a layout.

        Args:
            parent_layout_name: Parent layout object name
            orientation: "vertical" or "horizontal"
            size_hint: Dict with width and height
        """
        # Find parent layout
        parent = self.root.find(f".//layout[@name='{parent_layout_name}']")
        if parent is None:
            raise ValueError(f"Layout '{parent_layout_name}' not found")

        # Create spacer
        import random
        spacer_id = f"spacer_{random.randint(1000, 9999)}"
        spacer = ET.SubElement(parent, "spacer", name=spacer_id)

        # Add orientation property
        orient_value = "Qt::Vertical" if orientation == "vertical" else "Qt::Horizontal"
        self._add_property(spacer, "orientation", {"_type": "enum", "value": orient_value})

        # Add sizeHint
        if size_hint:
            self._add_property(spacer, "sizeHint", size_hint)
        else:
            default_size = {"width": 20, "height": 40} if orientation == "vertical" else {"width": 40, "height": 20}
            self._add_property(spacer, "sizeHint", default_size)

        return spacer

    def set_tab_order(self, widget_names: list):
        """
        Set tab order for widgets.

        Args:
            widget_names: List of widget names in tab order
        """
        # Find or create tabstops section
        tabstops = self.root.find("tabstops")
        if tabstops is not None:
            # Remove existing tabstops
            self.root.remove(tabstops)

        tabstops = ET.SubElement(self.root, "tabstops")

        # Add tabstops
        for widget_name in widget_names:
            ET.SubElement(tabstops, "tabstop").text = widget_name

    def set_buddy(self, label_name: str, widget_name: str):
        """
        Set buddy relationship between label and widget.

        Args:
            label_name: Label widget name
            widget_name: Buddy widget name
        """
        label = self._find_widget(label_name)
        if label is None:
            raise ValueError(f"Label '{label_name}' not found")

        # Add buddy property
        self._add_property(label, "buddy", widget_name)

    def add_custom_widget(self, class_name: str, extends: str, header: str):
        """
        Add a custom widget declaration.

        Args:
            class_name: Custom widget class name
            extends: Base class it extends
            header: Header file path
        """
        # Find or create customwidgets section
        customwidgets = self.root.find("customwidgets")
        if customwidgets is None:
            customwidgets = ET.SubElement(self.root, "customwidgets")

        # Create customwidget
        customwidget = ET.SubElement(customwidgets, "customwidget")
        ET.SubElement(customwidget, "class").text = class_name
        ET.SubElement(customwidget, "extends").text = extends
        ET.SubElement(customwidget, "header").text = header

        return customwidget

    def modify_property(self, widget_name: str, property_name: str, value: Any):
        """
        Modify a widget property.

        Args:
            widget_name: Widget object name
            property_name: Property to modify
            value: New value
        """
        widget = self._find_widget(widget_name)
        if widget is None:
            raise ValueError(f"Widget '{widget_name}' not found")

        # Find existing property or create new one
        prop = widget.find(f"./property[@name='{property_name}']")
        if prop is not None:
            # Remove old property
            widget.remove(prop)

        # Add new property
        self._add_property(widget, property_name, value)

    def _find_widget(self, widget_name: str):
        """Find widget by object name."""
        return self.root.find(f".//widget[@name='{widget_name}']")

    def _add_property(self, widget, property_name: str, value: Any):
        """
        Add a property to a widget.

        Supports multiple formats:
        1. Simple types: str, bool, int
        2. Dict with _type key for complex Qt types
        3. Dict with _xml key for raw XML insertion
        4. Auto-detection for common patterns (geometry, font, etc.)
        """
        prop = ET.SubElement(widget, "property", name=property_name)

        # Format 1: Raw XML string (most flexible)
        if isinstance(value, str) and value.strip().startswith('<'):
            # Parse and insert XML directly
            try:
                xml_elem = ET.fromstring(value)
                prop.append(xml_elem)
                return
            except ET.ParseError:
                # Not valid XML, treat as string
                pass

        # Format 2: Dict with _xml key for raw XML
        if isinstance(value, dict) and "_xml" in value:
            try:
                xml_elem = ET.fromstring(value["_xml"])
                prop.append(xml_elem)
                return
            except ET.ParseError as e:
                raise ValueError(f"Invalid XML in _xml property: {e}")

        # Format 3: Dict with _type key for structured Qt types
        if isinstance(value, dict) and "_type" in value:
            return self._add_typed_property(prop, value)

        # Format 4: Auto-detection for common types
        if isinstance(value, str):
            ET.SubElement(prop, "string").text = value
        elif isinstance(value, bool):
            ET.SubElement(prop, "bool").text = "true" if value else "false"
        elif isinstance(value, int):
            ET.SubElement(prop, "number").text = str(value)
        elif isinstance(value, float):
            ET.SubElement(prop, "double").text = str(value)
        elif isinstance(value, dict):
            # Auto-detect common patterns
            self._add_dict_property(prop, property_name, value)
        else:
            ET.SubElement(prop, "string").text = str(value)

    def _add_typed_property(self, prop, value_dict: dict):
        """
        Add a typed property based on _type key.

        Supports all Qt Designer property types:
        - font, palette, color, pixmap, iconset
        - size, rect, point, sizepolicy
        - enum, set, cursor, etc.
        """
        prop_type = value_dict["_type"]
        data = {k: v for k, v in value_dict.items() if k != "_type"}

        if prop_type == "font":
            self._add_font_property(prop, data)
        elif prop_type == "palette":
            self._add_palette_property(prop, data)
        elif prop_type == "color":
            self._add_color_property(prop, data)
        elif prop_type == "pixmap":
            self._add_pixmap_property(prop, data)
        elif prop_type == "iconset":
            self._add_iconset_property(prop, data)
        elif prop_type == "size":
            self._add_size_property(prop, data)
        elif prop_type == "rect":
            self._add_rect_property(prop, data)
        elif prop_type == "point":
            self._add_point_property(prop, data)
        elif prop_type == "sizepolicy":
            self._add_sizepolicy_property(prop, data)
        elif prop_type == "enum":
            self._add_enum_property(prop, data)
        elif prop_type == "set":
            self._add_set_property(prop, data)
        elif prop_type == "cursor":
            self._add_cursor_property(prop, data)
        else:
            # Fallback: create element with type name
            elem = ET.SubElement(prop, prop_type)
            for key, val in data.items():
                ET.SubElement(elem, key).text = str(val)

    def _add_dict_property(self, prop, property_name: str, value: dict):
        """Auto-detect dict property type and add appropriately."""
        # Geometry (rect with x, y, width, height)
        if all(k in value for k in ["x", "y", "width", "height"]):
            rect = ET.SubElement(prop, "rect")
            ET.SubElement(rect, "x").text = str(value["x"])
            ET.SubElement(rect, "y").text = str(value["y"])
            ET.SubElement(rect, "width").text = str(value["width"])
            ET.SubElement(rect, "height").text = str(value["height"])
        # Size (width, height only)
        elif "width" in value and "height" in value and len(value) == 2:
            size = ET.SubElement(prop, "size")
            ET.SubElement(size, "width").text = str(value["width"])
            ET.SubElement(size, "height").text = str(value["height"])
        # Point (x, y only)
        elif "x" in value and "y" in value and len(value) == 2:
            point = ET.SubElement(prop, "point")
            ET.SubElement(point, "x").text = str(value["x"])
            ET.SubElement(point, "y").text = str(value["y"])
        # Font-like structure
        elif any(k in value for k in ["family", "pointsize", "weight", "bold", "italic"]):
            font = ET.SubElement(prop, "font")
            for key, val in value.items():
                ET.SubElement(font, key).text = str(val)
        # Color-like structure
        elif any(k in value for k in ["red", "green", "blue", "alpha"]):
            color = ET.SubElement(prop, "color")
            for key, val in value.items():
                ET.SubElement(color, key).text = str(val)
        else:
            # Generic nested structure
            for key, val in value.items():
                ET.SubElement(prop, key).text = str(val)

    # Specific property type handlers
    def _add_font_property(self, prop, data: dict):
        """Add font property."""
        font = ET.SubElement(prop, "font")
        if "family" in data:
            ET.SubElement(font, "family").text = str(data["family"])
        if "pointsize" in data:
            ET.SubElement(font, "pointsize").text = str(data["pointsize"])
        if "weight" in data:
            ET.SubElement(font, "weight").text = str(data["weight"])
        if "italic" in data:
            ET.SubElement(font, "italic").text = str(data["italic"]).lower()
        if "bold" in data:
            ET.SubElement(font, "bold").text = str(data["bold"]).lower()
        if "underline" in data:
            ET.SubElement(font, "underline").text = str(data["underline"]).lower()
        if "strikeout" in data:
            ET.SubElement(font, "strikeout").text = str(data["strikeout"]).lower()

    def _add_palette_property(self, prop, data: dict):
        """Add palette property."""
        palette = ET.SubElement(prop, "palette")
        # Simplified palette - full implementation would be more complex
        for role, color_data in data.items():
            colorrole = ET.SubElement(palette, "colorrole", role=role)
            if isinstance(color_data, dict):
                self._add_color_element(colorrole, color_data)

    def _add_color_property(self, prop, data: dict):
        """Add color property."""
        self._add_color_element(prop, data)

    def _add_color_element(self, parent, data: dict):
        """Add color element."""
        color = ET.SubElement(parent, "color")
        if "alpha" in data:
            color.set("alpha", str(data["alpha"]))
        if "red" in data:
            ET.SubElement(color, "red").text = str(data["red"])
        if "green" in data:
            ET.SubElement(color, "green").text = str(data["green"])
        if "blue" in data:
            ET.SubElement(color, "blue").text = str(data["blue"])

    def _add_pixmap_property(self, prop, data: dict):
        """Add pixmap property."""
        pixmap = ET.SubElement(prop, "pixmap")
        if "resource" in data:
            pixmap.set("resource", data["resource"])
        if "path" in data:
            pixmap.text = data["path"]

    def _add_iconset_property(self, prop, data: dict):
        """Add iconset property."""
        iconset = ET.SubElement(prop, "iconset")
        if "resource" in data:
            iconset.set("resource", data["resource"])
        if "theme" in data:
            iconset.set("theme", data["theme"])
        # Can contain multiple pixmaps for different states/modes

    def _add_size_property(self, prop, data: dict):
        """Add size property."""
        size = ET.SubElement(prop, "size")
        ET.SubElement(size, "width").text = str(data.get("width", 0))
        ET.SubElement(size, "height").text = str(data.get("height", 0))

    def _add_rect_property(self, prop, data: dict):
        """Add rect property."""
        rect = ET.SubElement(prop, "rect")
        ET.SubElement(rect, "x").text = str(data.get("x", 0))
        ET.SubElement(rect, "y").text = str(data.get("y", 0))
        ET.SubElement(rect, "width").text = str(data.get("width", 0))
        ET.SubElement(rect, "height").text = str(data.get("height", 0))

    def _add_point_property(self, prop, data: dict):
        """Add point property."""
        point = ET.SubElement(prop, "point")
        ET.SubElement(point, "x").text = str(data.get("x", 0))
        ET.SubElement(point, "y").text = str(data.get("y", 0))

    def _add_sizepolicy_property(self, prop, data: dict):
        """Add sizepolicy property."""
        sizepolicy = ET.SubElement(prop, "sizepolicy")
        if "hsizetype" in data:
            sizepolicy.set("hsizetype", str(data["hsizetype"]))
        if "vsizetype" in data:
            sizepolicy.set("vsizetype", str(data["vsizetype"]))
        if "horstretch" in data:
            ET.SubElement(sizepolicy, "horstretch").text = str(data["horstretch"])
        if "verstretch" in data:
            ET.SubElement(sizepolicy, "verstretch").text = str(data["verstretch"])

    def _add_enum_property(self, prop, data: dict):
        """Add enum property."""
        enum = ET.SubElement(prop, "enum")
        enum.text = data.get("value", "")

    def _add_set_property(self, prop, data: dict):
        """Add set property."""
        setelem = ET.SubElement(prop, "set")
        setelem.text = data.get("value", "")

    def _add_cursor_property(self, prop, data: dict):
        """Add cursor property."""
        cursor = ET.SubElement(prop, "cursor")
        cursor.text = str(data.get("shape", "ArrowCursor"))

    def get_widget_tree(self) -> Dict:
        """
        Get widget hierarchy as dictionary.

        Returns:
            Dictionary representing widget tree structure
        """
        if self.root is None:
            return {}

        main_widget = self.root.find(".//widget")
        if main_widget is None:
            return {}

        return self._widget_to_dict(main_widget)

    def _widget_to_dict(self, widget_elem) -> Dict:
        """Convert widget XML element to dictionary."""
        result = {
            "type": widget_elem.get("class"),
            "name": widget_elem.get("name"),
            "properties": {},
            "children": []
        }

        # Extract properties
        for prop in widget_elem.findall("./property"):
            prop_name = prop.get("name")
            prop_value = self._extract_property_value(prop)
            result["properties"][prop_name] = prop_value

        # Extract child widgets
        for child in widget_elem.findall("./widget"):
            result["children"].append(self._widget_to_dict(child))

        # Extract layouts
        for layout in widget_elem.findall("./layout"):
            layout_dict = {
                "type": layout.get("class"),
                "name": layout.get("name"),
                "children": []
            }
            for child in layout.findall("./widget"):
                layout_dict["children"].append(self._widget_to_dict(child))
            result["children"].append(layout_dict)

        return result

    def _extract_property_value(self, prop_elem):
        """Extract value from property element."""
        for child in prop_elem:
            if child.tag == "string":
                return child.text or ""
            elif child.tag == "bool":
                return child.text == "true"
            elif child.tag == "number":
                return int(child.text)
            elif child.tag == "rect":
                return {
                    "x": int(child.find("x").text),
                    "y": int(child.find("y").text),
                    "width": int(child.find("width").text),
                    "height": int(child.find("height").text)
                }
        return None


def create_template_ui(template_type: str, output_path: str, **kwargs):
    """
    Create a .ui file from template.

    Args:
        template_type: "dialog", "mainwindow", or "widget"
        output_path: Where to save the .ui file
        **kwargs: Additional parameters (name, width, height)
    """
    name = kwargs.get("name", template_type.capitalize())
    width = kwargs.get("width", 400)
    height = kwargs.get("height", 300)

    ui_manager = UIManager()

    if template_type == "dialog":
        ui_manager.create_empty_ui("QDialog", name, width, height)
    elif template_type == "mainwindow":
        ui_manager.create_empty_ui("QMainWindow", name, width, height)
    elif template_type == "widget":
        ui_manager.create_empty_ui("QWidget", name, width, height)
    else:
        raise ValueError(f"Unknown template type: {template_type}")

    ui_manager.save(output_path)
    return output_path


if __name__ == "__main__":
    # Test: Create a simple dialog
    manager = UIManager()
    manager.create_empty_ui("QDialog", "TestDialog", 400, 300)

    # Add a button
    manager.add_widget("QPushButton", "pushButton", properties={
        "text": "Click Me",
        "geometry": {"x": 150, "y": 200, "width": 100, "height": 30}
    })

    # Save
    manager.save("test_output.ui")
    print("Created test_output.ui")

    # Print widget tree
    import json
    tree = manager.get_widget_tree()
    print(json.dumps(tree, indent=2))
