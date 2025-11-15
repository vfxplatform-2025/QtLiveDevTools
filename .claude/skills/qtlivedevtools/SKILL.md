---
name: qtlivedevtools
description: Create, modify, and preview Qt/PySide6 UI files (.ui) using natural language. Use when user asks to create Qt widgets, design dialogs, build PySide6 interfaces, or work with .ui XML files. Supports all Qt properties, layouts, stylesheets, and live preview with screenshots.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# QtLiveDevTools Skill

Create and modify Qt/PySide6 UI files through conversational interface, similar to Qt Designer but using natural language.

## When to Use This Skill

Activate this Skill when the user mentions:
- "Create a Qt dialog/window/widget"
- "Make a PySide6 UI"
- "Build a login form with Qt"
- "Add a button/label/layout to the UI"
- "Modify .ui file"
- "Show me a preview of the UI"
- "Convert to PySide6/PySide2"

## Core Capabilities

### 1. UI File Creation
Create .ui files (Qt Designer XML format) from scratch:
- Dialog, MainWindow, or Widget templates
- Custom dimensions
- Standard Qt structure

### 2. Widget Management
Add and modify Qt widgets with all properties:
- Basic widgets: QPushButton, QLabel, QLineEdit, QTextEdit, etc.
- Containers: QGroupBox, QTabWidget, QScrollArea
- Advanced: QTableView, QTreeView, QListWidget
- All Qt properties: font, color, palette, stylesheet, geometry, etc.

### 3. Layout System
Organize widgets with Qt layouts:
- QVBoxLayout, QHBoxLayout, QGridLayout
- Spacers (horizontal/vertical)
- Nested layouts
- Margins and spacing

### 4. Live Preview
Display UI with screenshot:
- Launch PySide6 preview window
- Capture screenshot
- Show visual result to user

### 5. Advanced Features
- Signal/Slot connections
- Stylesheets (QSS)
- Property animations
- PySide6 ↔ PySide2 conversion

## Implementation Details

### Directory Structure
```
/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools/
├── ui_manager.py          # Core UI manipulation
├── mcp_server.py          # Function library (reusable)
├── live_ui_editor.py      # Preview tool
├── pyside_converter.py    # Version converter
└── editor_client.py       # Socket communication
```

### Python Environment
**CRITICAL**: Use the correct Python environment:
```bash
# Check available Python
rez-env pyside6 -- python --version

# Or use MCP venv
/storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python
```

### Core Workflow

#### Step 1: Import Required Modules
```python
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from ui_manager import UIManager
from mcp_server import create_ui_file, add_widget_to_ui, preview_ui
```

#### Step 2: Create UI File
```python
# Create new .ui file
create_ui_file(
    name="login_dialog",
    template="dialog",  # or "mainwindow", "widget"
    width=400,
    height=300
)
```

#### Step 3: Add Widgets
```python
# Add widgets with properties
add_widget_to_ui(
    ui_file="login_dialog.ui",
    widget_type="QLabel",
    object_name="titleLabel",
    properties={
        "text": "Login",
        "font": {
            "_type": "font",
            "family": "Arial",
            "pointsize": "16",
            "bold": "true"
        },
        "geometry": {
            "_type": "rect",
            "x": "10", "y": "10",
            "width": "380", "height": "40"
        }
    }
)

add_widget_to_ui(
    ui_file="login_dialog.ui",
    widget_type="QPushButton",
    object_name="loginButton",
    properties={
        "text": "Login",
        "geometry": {
            "_type": "rect",
            "x": "150", "y": "250",
            "width": "100", "height": "30"
        }
    }
)
```

#### Step 4: Add Layouts (Optional)
```python
manager = UIManager("login_dialog.ui")
manager.add_layout("QVBoxLayout", "mainLayout")
# Move widgets into layout programmatically if needed
```

#### Step 5: Preview UI
```python
# Launch preview and take screenshot
result = preview_ui("login_dialog.ui", port=7010)
# Returns: {"success": true, "screenshot_base64": "..."}
# Display screenshot to user
```

### Property Types Reference

#### Basic Properties
```python
{
    "text": "Hello",           # String
    "enabled": True,           # Bool
    "width": 100,              # Int
    "minimumWidth": 50         # Int
}
```

#### Font Property
```python
{
    "font": {
        "_type": "font",
        "family": "Arial",
        "pointsize": "14",
        "bold": "true",
        "italic": "false"
    }
}
```

#### Color Property
```python
{
    "color": {
        "_type": "color",
        "red": "255",
        "green": "0",
        "blue": "0"
    }
}
```

#### Geometry (Rect)
```python
{
    "geometry": {
        "_type": "rect",
        "x": "10",
        "y": "20",
        "width": "200",
        "height": "100"
    }
}
```

#### Stylesheet
```python
{
    "styleSheet": "QPushButton { background-color: #2196F3; color: white; }"
}
```

### Live Preview Setup

#### Method 1: Bash Command (Recommended for Skills)
```bash
# Find available port
for port in {7010..7020}; do
  if ! nc -z localhost $port 2>/dev/null; then
    echo "Using port $port"
    # Launch live editor
    rez-env pyside6 -- python /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools/live_ui_editor.py \
      --ui login_dialog.ui --port $port &
    sleep 2
    break
  fi
done

# Take screenshot using Python
rez-env pyside6 -- python -c "
import sys
sys.path.insert(0, '/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools')
from editor_client import send_command
result = send_command(port=$port, command={'action': 'screenshot'})
print(result['screenshot_base64'])
"
```

#### Method 2: Direct Python (Alternative)
Use Bash tool to execute Python with proper environment.

### Common Widget Types

- **Text**: QLabel, QLineEdit, QTextEdit, QPlainTextEdit
- **Buttons**: QPushButton, QToolButton, QRadioButton, QCheckBox
- **Containers**: QGroupBox, QFrame, QWidget, QScrollArea
- **Lists**: QListWidget, QTableWidget, QTreeWidget
- **Input**: QSpinBox, QDoubleSpinBox, QComboBox, QSlider
- **Layouts**: QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout
- **Views**: QListView, QTableView, QTreeView (with models)

### Signal/Slot Connections

```python
manager = UIManager("login_dialog.ui")
manager.add_connection(
    sender="loginButton",
    signal="clicked()",
    receiver="login_dialog",
    slot="accept()"
)
```

### PySide Version Conversion

```python
from pyside_converter import convert_pyside_version

# Convert to PySide2 (for Maya 2023)
convert_pyside_version("pyside2", "/path/to/ui_files/")

# Convert to PySide6
convert_pyside_version("pyside6", "/path/to/ui_files/")
```

## User Interaction Pattern

### Example Conversation

**User**: "Create a login dialog with username and password fields"

**Claude (using this Skill)**:
1. Import modules
2. Create login_dialog.ui (Dialog, 400x300)
3. Add QLabel "Username:" at (10, 10)
4. Add QLineEdit "usernameEdit" at (10, 40)
5. Add QLabel "Password:" at (10, 80)
6. Add QLineEdit "passwordEdit" at (10, 110), echoMode=Password
7. Add QPushButton "Login" at (150, 250)
8. Launch preview, capture screenshot
9. Show screenshot to user: "Created login dialog with username/password fields"

**User**: "Make the login button blue"

**Claude**:
1. Read login_dialog.ui
2. Modify loginButton stylesheet: "background-color: #2196F3; color: white;"
3. Reload preview, capture screenshot
4. Show updated screenshot

**User**: "Show me the .ui file structure"

**Claude**:
1. Read login_dialog.ui
2. Parse XML and show widget hierarchy as JSON
3. Explain structure to user

## Error Handling

### Common Issues

**Problem**: PySide6 not found
```bash
# Solution: Use Rez environment
rez-env pyside6 -- python script.py
```

**Problem**: Port already in use
```bash
# Solution: Find available port
for port in {7010..7020}; do
  if ! nc -z localhost $port 2>/dev/null; then
    echo $port
    break
  fi
done
```

**Problem**: UI file not found
```bash
# Solution: Use absolute paths
/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools/login_dialog.ui
```

## Best Practices

1. **Always use absolute paths** for reliability
2. **Verify Python environment** before importing modules
3. **Take screenshots** after modifications to show visual results
4. **Explain changes** to user in natural language
5. **Handle errors gracefully** with clear messages
6. **Use Rez environments** for consistent PySide versions

## Integration with VFX Pipeline

### Maya Integration
```python
# Maya 2023 uses PySide2
if maya_version < 2024:
    convert_pyside_version("pyside2", ui_dir)
```

### Houdini Integration
```python
# Houdini uses PySide2
convert_pyside_version("pyside2", ui_dir)
```

## Reference Files

See these files in the QtLiveDevTools directory for implementation details:
- `ui_manager.py` - XML manipulation
- `mcp_server.py` - High-level functions
- `CLAUDE.md` - Architecture guide
- `QT_ALL_FEATURES_SUPPORTED.md` - Complete Qt property reference

## Success Criteria

When using this Skill, ensure:
- ✅ .ui file is created/modified correctly
- ✅ Screenshot shows visual result
- ✅ User understands what was done
- ✅ File is compatible with Qt Designer
- ✅ Changes are persistent (saved to disk)
