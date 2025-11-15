# QtLiveDevTools Skill - Examples

## Example 1: Simple Login Dialog

### User Request
"Create a login dialog with username and password fields and a login button"

### Implementation Steps

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from mcp_server import create_ui_file, add_widget_to_ui

# 1. Create dialog
create_ui_file("login", "dialog", 400, 250)

# 2. Add title label
add_widget_to_ui("login.ui", "QLabel", "titleLabel", {
    "text": "User Login",
    "font": {"_type": "font", "family": "Arial", "pointsize": "16", "bold": "true"},
    "geometry": {"_type": "rect", "x": "10", "y": "10", "width": "380", "height": "40"}
})

# 3. Add username label
add_widget_to_ui("login.ui", "QLabel", "usernameLabel", {
    "text": "Username:",
    "geometry": {"_type": "rect", "x": "10", "y": "60", "width": "100", "height": "25"}
})

# 4. Add username field
add_widget_to_ui("login.ui", "QLineEdit", "usernameEdit", {
    "geometry": {"_type": "rect", "x": "120", "y": "60", "width": "260", "height": "25"}
})

# 5. Add password label
add_widget_to_ui("login.ui", "QLabel", "passwordLabel", {
    "text": "Password:",
    "geometry": {"_type": "rect", "x": "10", "y": "100", "width": "100", "height": "25"}
})

# 6. Add password field
add_widget_to_ui("login.ui", "QLineEdit", "passwordEdit", {
    "echoMode": {"_type": "enum", "value": "QLineEdit::Password"},
    "geometry": {"_type": "rect", "x": "120", "y": "100", "width": "260", "height": "25"}
})

# 7. Add login button
add_widget_to_ui("login.ui", "QPushButton", "loginButton", {
    "text": "Login",
    "styleSheet": "QPushButton { background-color: #2196F3; color: white; font-weight: bold; }",
    "geometry": {"_type": "rect", "x": "150", "y": "180", "width": "100", "height": "35"}
})
```

### Preview
```bash
rez-env pyside6 -- python live_ui_editor.py --ui login.ui --port 7010
```

---

## Example 2: File Browser with Layout

### User Request
"Make a file browser with a tree on the left and preview on the right"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from ui_manager import UIManager
from mcp_server import create_ui_file, add_widget_to_ui

# 1. Create MainWindow
create_ui_file("file_browser", "mainwindow", 800, 600)

# 2. Add central widget
manager = UIManager("file_browser.ui")

# 3. Add horizontal layout
manager.add_layout("QHBoxLayout", "mainLayout")

# 4. Add tree widget (left side)
add_widget_to_ui("file_browser.ui", "QTreeWidget", "fileTree", {
    "minimumWidth": 250,
    "headerHidden": False
})

# 5. Add preview label (right side)
add_widget_to_ui("file_browser.ui", "QLabel", "previewLabel", {
    "text": "Select a file to preview",
    "alignment": {"_type": "set", "value": "Qt::AlignCenter"},
    "styleSheet": "QLabel { border: 1px solid #ccc; background-color: #f5f5f5; }"
})

# Note: Widgets will be added to layout programmatically or via Qt Designer
```

---

## Example 3: Styled Settings Panel

### User Request
"Create a settings panel with tabs for General, Advanced, and About"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from mcp_server import create_ui_file, add_widget_to_ui

# 1. Create dialog
create_ui_file("settings", "dialog", 500, 400)

# 2. Add tab widget
add_widget_to_ui("settings.ui", "QTabWidget", "tabWidget", {
    "geometry": {"_type": "rect", "x": "10", "y": "10", "width": "480", "height": "340"}
})

# 3. Add General tab (QWidget)
add_widget_to_ui("settings.ui", "QWidget", "generalTab", {})

# 4. Add checkbox in General tab
add_widget_to_ui("settings.ui", "QCheckBox", "autoSaveCheck", {
    "text": "Enable Auto-Save",
    "geometry": {"_type": "rect", "x": "20", "y": "20", "width": "200", "height": "25"}
})

# 5. Add Advanced tab
add_widget_to_ui("settings.ui", "QWidget", "advancedTab", {})

# 6. Add About tab
add_widget_to_ui("settings.ui", "QWidget", "aboutTab", {})

# 7. Add label in About tab
add_widget_to_ui("settings.ui", "QLabel", "versionLabel", {
    "text": "Version 1.0.0",
    "alignment": {"_type": "set", "value": "Qt::AlignCenter"}
})

# Note: Tab hierarchy setup requires UIManager methods
```

---

## Example 4: Modify Existing UI

### User Request
"Change the login button color to green and make it bigger"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from ui_manager import UIManager

manager = UIManager("login.ui")

# 1. Update button stylesheet
manager.modify_widget_property(
    "loginButton",
    "styleSheet",
    "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; }"
)

# 2. Update geometry (bigger)
manager.modify_widget_property(
    "loginButton",
    "geometry",
    {"_type": "rect", "x": "140", "y": "180", "width": "120", "height": "45"}
)

manager.save()
```

---

## Example 5: Quick Preview Workflow

### User Request
"Show me what the dialog looks like"

### Bash Implementation

```bash
# Find available port
for port in {7010..7020}; do
  if ! nc -z localhost $port 2>/dev/null; then
    PREVIEW_PORT=$port
    break
  fi
done

# Launch live editor in background
rez-env pyside6 -- python /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools/live_ui_editor.py \
  --ui login.ui --port $PREVIEW_PORT &

# Wait for editor to start
sleep 2

# Take screenshot (using Python)
rez-env pyside6 -- python -c "
import sys
import json
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from editor_client import send_command

result = send_command($PREVIEW_PORT, {'action': 'screenshot'})
if result.get('success'):
    print('Screenshot captured')
    # Display base64 to user
else:
    print('Failed:', result.get('error'))
"
```

---

## Example 6: Convert for Maya 2023

### User Request
"Make this UI compatible with Maya 2023"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from pyside_converter import convert_pyside_version

# Maya 2023 uses PySide2
result = convert_pyside_version("pyside2", "/path/to/ui/directory/")

print(f"Converted {result['files_converted']} files to PySide2")
```

---

## Example 7: Add Signal/Slot Connection

### User Request
"Make the login button close the dialog when clicked"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from ui_manager import UIManager

manager = UIManager("login.ui")

# Connect button clicked() to dialog accept()
manager.add_connection(
    sender="loginButton",
    signal="clicked()",
    receiver="login",
    slot="accept()"
)

manager.save()
```

---

## Example 8: Complex Property - Font with Multiple Attributes

### User Request
"Make the title label use Courier New 18pt bold italic"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from ui_manager import UIManager

manager = UIManager("login.ui")

manager.modify_widget_property(
    "titleLabel",
    "font",
    {
        "_type": "font",
        "family": "Courier New",
        "pointsize": "18",
        "bold": "true",
        "italic": "true",
        "weight": "75"
    }
)

manager.save()
```

---

## Example 9: Using Bash for Simple UI Creation

### User Request
"Quick! Just create an empty dialog"

### Bash-Only Implementation

```bash
cat > simple_dialog.ui << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
 </widget>
 <resources/>
 <connections/>
</ui>
EOF

echo "Created simple_dialog.ui"
```

---

## Example 10: Reading UI Structure

### User Request
"What widgets are in this UI?"

### Implementation

```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from ui_manager import UIManager

manager = UIManager("login.ui")
structure = manager.get_ui_structure()

# Show hierarchy
for widget in structure['widgets']:
    print(f"- {widget['class']} ({widget['name']})")
```
