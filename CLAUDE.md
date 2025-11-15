# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

QtLiveDevTools is a live development tool for Qt/PySide6 applications that enables real-time UI creation and modification through **Claude CLI conversation**, similar to Chrome DevTools MCP for React applications.

**Primary Use Case**: Conversational UI development - talk to Claude to create and modify Qt UIs
**Runtime**: PySide6 (Qt for Python)
**Language**: Python
**Architecture**: MCP Server + Live UI Editor + .ui File Workflow

## Core Workflow

```
PyCharm Terminal → Claude CLI → MCP Server → Socket (port 7001) → Live UI Editor
                                     ↓
                               .ui File (XML)
                                     ↓
                            Screenshot + Analysis → Claude
```

### User Experience Goal

```
You: "로그인 창 만들어줘"
Claude: [.ui 파일 생성] → [Live Editor에 명령] → [스크린샷 캡처] → "만들었습니다. [이미지]"

You: "버튼을 오른쪽으로 이동"
Claude: [.ui 분석] → [XML 수정] → [Live Editor 업데이트] → [스크린샷] → "이동했습니다."

You: (필요시 Qt Designer로 login.ui 직접 편집)
Claude: "login.ui 다시 확인해줘" → [분석] → [스크린샷] → "변경사항 확인했습니다."
```

## Architecture Components

### 1. MCP Server (Claude ↔ Tool Bridge)

MCP tools that Claude uses to manipulate Qt UIs:

```python
# .ui File Management
create_ui_file(name, template="dialog|mainwindow|widget")
add_widget_to_ui(ui_file, widget_type, parent, properties)
modify_widget_property(ui_file, widget_name, property, value)
get_ui_structure(ui_file) → widget hierarchy as JSON

# Live UI Editor Control (Socket Communication)
send_command_to_editor(port, command) → Maya commandPort style
preview_ui(ui_file) → loads UI, takes screenshot
reload_ui(ui_file) → hot-reload without restart

# Multi-layer Analysis
analyze_ui(ui_file) → {
    "ui_structure": {...},      # XML parsing
    "widget_tree": {...},       # Runtime hierarchy
    "visual": {
        "screenshot_base64": "...",
        "widget_positions": [...]  # Bounding boxes
    },
    "styles": {...},            # QSS extraction
    "signals_slots": {...}      # Connections
}

# Advanced Analysis
find_widget_by_description(ui_file, "파란색 버튼") → widget_name
detect_layout_issues(ui_file) → [overlaps, out-of-bounds, etc.]
apply_stylesheet(ui_file, qss_string)
```

### 2. Live UI Editor (Maya commandPort 방식)

Custom PySide6 application that:
- Listens on **port 7001** for JSON commands (like Maya commandPort)
- Loads and displays .ui files in real-time
- Executes commands: add widget, modify property, screenshot, etc.
- Auto-saves changes back to .ui file
- Supports hot-reload without restarting

```python
# Live UI Editor 실행
$ python live_ui_editor.py --ui login.ui --port 7001

# MCP Server에서 명령 전송
socket.connect("localhost", 7001)
socket.send(json.dumps({
    "action": "add_widget",
    "type": "QPushButton",
    "parent": "mainLayout",
    "properties": {"text": "Login"}
}))
```

### 3. .ui File Workflow (Qt Designer 호환)

- **Primary Format**: .ui files (XML) - Qt Designer 표준 포맷
- **Benefits**:
  - Git-friendly (text-based XML)
  - Qt Designer로 직접 편집 가능
  - VFX pipeline 표준 워크플로우
  - 재사용 가능한 결과물
- **NOT using**: Runtime-only manipulation (no persistent .ui files)

## Multi-layer UI Analysis System

Screenshot만으로는 부족 - Claude가 UI를 **완벽히 이해**하려면:

### Layer 1: XML Structure (.ui file)
- 정확한 widget objectName, 위치, 크기
- 부모-자식 관계
- 속성 값 (text, geometry, etc.)

### Layer 2: Widget Tree (Runtime)
- 실제 레이아웃 구조 (QVBoxLayout, QHBoxLayout, etc.)
- 동적 생성된 위젯
- Signal/slot 연결 정보

### Layer 3: Visual + Bounding Boxes
- Screenshot (Claude vision 활용)
- 각 widget의 screen 좌표 (bbox)
- 시각적 위치 ↔ objectName 매핑

### Layer 4: Styling (QSS)
- 현재 적용된 stylesheet
- 색상, 폰트, 테두리 등

**Why Multi-layer?**
- Claude가 "로그인 버튼"이라고 지칭할 때 정확히 어떤 widget인지 특정
- 픽셀 단위 조정 가능
- 레이아웃 로직 이해 (VBox vs HBox vs Grid)
- 스타일 수정 시 현재 값 기반으로 변경

## Development Commands

### Running Live UI Editor
```bash
# Start editor with UI file
python live_ui_editor.py --ui myapp.ui --port 7001

# With auto-reload on file change
python live_ui_editor.py --ui myapp.ui --port 7001 --watch
```

### Running MCP Server
```bash
# Start MCP server (Claude connects to this)
python mcp_server.py --editor-port 7001
```

### Using from PyCharm
```bash
# Terminal 1: Start Live UI Editor
python live_ui_editor.py --ui login.ui --port 7001

# Terminal 2: Start Claude CLI
claude

# Now talk to Claude to create/modify UI
```

### Installing Dependencies
```bash
pip install PySide6
pip install mcp  # Model Context Protocol SDK
```

## Key Technical Decisions

### ✅ Chosen Approach: .ui File + Socket Control

**Why .ui files?**
- Standard Qt Designer format
- User can manually edit with Qt Designer
- Git-friendly (XML diff)
- Persistent, reusable artifacts

**Why Socket Control (Maya commandPort style)?**
- Real-time communication with running UI
- Claude can send commands and see immediate results
- Familiar pattern for VFX TDs
- Decoupled architecture (MCP ↔ Editor)

### ❌ Rejected Approaches

**Runtime-only manipulation (no .ui files)**
- 장점: Instant changes
- 단점: No persistent files, hard to manually edit, not standard

**Qt Designer plugin**
- 장점: Native Designer integration
- 단점: Requires C++, complex build, overkill

**Direct Qt Designer control**
- 불가능: Qt Designer has no external API

## Integration with Claude CLI

Claude uses natural language to control the UI:

```
"Create a login dialog with username, password fields and a login button"
"Move the login button to the right of the password field"
"Change the button color to blue"
"Add a QLabel above the username field with text 'Welcome'"
"Show me the current widget tree"
"Take a screenshot"
```

Claude's internal process:
1. Parse user intent
2. Call `analyze_ui()` to understand current state
3. Modify .ui file (XML manipulation)
4. Send command to Live Editor via socket
5. Capture screenshot
6. Show result to user

## Comparison with Chrome DevTools MCP

| Feature | Chrome DevTools MCP | QtLiveDevTools |
|---------|---------------------|----------------|
| Target | Browser DOM | Qt Widgets |
| Protocol | Chrome DevTools Protocol | Socket (JSON) |
| File Format | HTML/CSS/JS | .ui (XML) |
| Live Preview | Browser | PySide6 Window |
| Manual Edit | Browser Inspector | Qt Designer |
| Claude Integration | MCP | MCP |

## VFX Pipeline Integration

- .ui files are standard in VFX studios (Maya, Houdini, Nuke tools)
- Familiar workflow for TDs
- Compatible with existing Qt-based tools
- Can be version-controlled in production pipelines
