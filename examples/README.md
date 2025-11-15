# QtLiveDevTools

Live development tool for Qt/PySide6 applications - Create and modify Qt UIs through **conversational interface with Claude CLI**.

## Overview

QtLiveDevTools enables real-time Qt UI creation and modification through natural language conversation with Claude. Similar to Chrome DevTools MCP for React applications, but for Qt/PySide6.

### Key Features

- 🎨 **Conversational UI Development** - Talk to Claude to create UIs
- 🔄 **Real-time Preview** - See changes instantly with Live UI Editor
- 📁 **Standard .ui Files** - Qt Designer compatible XML format
- 🛠️ **VFX Pipeline Ready** - Designed for production use
- 🤖 **MCP Integration** - Full Model Context Protocol support

## Quick Start

### Using MCP Tools with Claude CLI

Talk to Claude to create UIs:

```
You: "로그인 창 만들어줘"
Claude: [Creates login_dialog.ui] → [Shows structure]

You: "버튼을 오른쪽으로 이동"
Claude: [Modifies .ui file] → [Shows changes]
```

### Using Python API

```python
from mcp_server import create_ui_file, add_widget_to_ui

# Create UI
create_ui_file("my_dialog", template="dialog", width=500, height=400)

# Add button
add_widget_to_ui("my_dialog.ui", "QPushButton", "submitButton",
    properties={"text": "제출", "geometry": {"x": 200, "y": 300, "width": 100, "height": 40}})
```

### Using Live Editor

```bash
# Start Live UI Editor
./start_live_editor.sh my_dialog.ui 7010

# Test integration
python test_integration.py
```

## Available MCP Tools

- `create_ui_file` - Create new .ui files
- `add_widget` - Add widgets (QPushButton, QLabel, QLineEdit, etc.)
- `add_layout` - Add layouts (QVBoxLayout, QHBoxLayout, QGridLayout)
- `modify_property` - Modify widget properties
- `get_ui_structure` - Get widget hierarchy as JSON
- `analyze_ui` - Multi-layer UI analysis
- `preview_ui` - Live preview and screenshot

## Examples

### VFX Production Examples

```bash
cd examples
python vfx_file_browser.py
```

Creates:
- **vfx_file_browser.ui** - File browser (800x600, 17 widgets)
- **render_submit.ui** - Render submission (600x700, 30+ widgets)

## Testing

```bash
# Integration test
python test_integration.py

# Live workflow
python test_live_workflow.py

# Advanced features
python test_advanced_features.py
```

## Requirements

- Python 3.11+
- PySide6 (via rez-env)
- MCP SDK

## License

Internal tool for M83 VFX Studio

---

**Contact: chulho@m83.studio**
