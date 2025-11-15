# QtLiveDevTools Development Plan

## 개발 계획 분석

### 핵심 의존성 관계

```
Live UI Editor (독립 실행 가능)
    ↑
MCP Server (Editor에 명령 전송)
    ↑
Claude CLI (MCP Server 사용)
```

**결론**: Bottom-up 방식으로 개발해야 함 (Editor → MCP → Integration)

---

## 📋 Phase 1: Foundation (핵심 인프라)

**목표**: Claude 없이도 동작하는 기본 시스템

### 1.1 Live UI Editor 프로토타입 (최우선)
```python
# live_ui_editor.py
- PySide6로 .ui 파일 로드 & 표시
- Socket server (port 7001) 구현
- 기본 명령 처리:
  ✓ reload_ui
  ✓ take_screenshot
  ✓ get_widget_tree
```

**테스트 방법**: 수동으로 소켓 명령 전송해서 동작 확인
```bash
echo '{"action":"take_screenshot"}' | nc localhost 7001
```

### 1.2 .ui 파일 조작 라이브러리
```python
# ui_manager.py
- XML parsing/modification (ElementTree)
- create_empty_ui()
- add_widget() - XML에 widget 추가
- modify_property() - XML 속성 수정
- validate_ui() - .ui 파일 유효성 검사
```

**테스트**: 간단한 .ui 파일 생성/수정 스크립트

---

## 📋 Phase 2: Analysis System (Claude의 눈과 귀)

**목표**: Claude가 UI를 "이해"할 수 있게

### 2.1 Multi-layer Analyzer
```python
# ui_analyzer.py
- parse_ui_xml() → Layer 1 (XML structure)
- get_widget_tree_from_runtime() → Layer 2 (실행 중 트리)
- capture_with_bboxes() → Layer 3 (Visual + 좌표)
- extract_qss() → Layer 4 (Styling)
- analyze_ui() → 통합 분석 결과
```

### 2.2 Widget Inspector
```python
# widget_inspector.py
- find_widget_by_name()
- find_widget_by_description() - "파란색 버튼" → objectName
- detect_layout_issues() - 겹침, 범위 초과 등
- get_widget_bbox() - 화면 좌표 계산
```

**테스트**: 샘플 .ui로 분석 결과 JSON 출력

---

## 📋 Phase 3: MCP Server (Claude 연결)

**목표**: Claude CLI와 통신 가능

### 3.1 MCP Tools 구현
```python
# mcp_server.py
@mcp_tool - create_ui_file()
@mcp_tool - add_widget_to_ui()
@mcp_tool - modify_widget_property()
@mcp_tool - analyze_ui()
@mcp_tool - preview_ui()
@mcp_tool - send_command_to_editor()
```

### 3.2 Socket Client (MCP → Editor)
```python
# editor_client.py
- connect_to_editor(port)
- send_command(action, params)
- receive_response()
- handle_timeout/errors
```

**테스트**: Claude CLI 없이 Python 스크립트로 MCP tools 직접 호출

---

## 📋 Phase 4: Integration & Polish

### 4.1 End-to-End 워크플로우
- Claude CLI 설정 파일 작성
- 샘플 대화 시나리오 테스트
- 에러 핸들링 개선

### 4.2 편의 기능
- Widget template library (login dialog, file browser 등)
- QSS preset (Dark theme, Light theme)
- Auto-save .ui on change
- File watching (Qt Designer로 수정 시 자동 reload)

---

## 🎯 권장 개발 순서 (우선순위)

### Week 1: Minimal Viable Product
```
Day 1-2: Live UI Editor 기본 (소켓 서버 + .ui 로드)
Day 3-4: .ui XML 조작 라이브러리
Day 5-7: 통합 테스트 (수동 명령으로 UI 생성/수정)
```

### Week 2: Analysis & Intelligence
```
Day 1-3: Multi-layer Analyzer 구현
Day 4-5: Screenshot + Bounding Box 시스템
Day 6-7: Widget Inspector (description → objectName)
```

### Week 3: MCP Integration
```
Day 1-3: MCP Server + Tools 구현
Day 4-5: Claude CLI 연동 테스트
Day 6-7: 에러 처리 & 안정화
```

### Week 4: Polish & Templates
```
Day 1-3: Widget templates
Day 4-5: QSS presets
Day 6-7: Documentation & 사용 예제
```

---

## 🚀 Quick Start Path (빠른 프로토타입)

시간이 촉박하다면 이 순서로:

### Step 1: 초간단 Editor (2-3시간)
```python
# 소켓 없이, .ui만 로드하고 표시
from PySide6.QtWidgets import QApplication
from PySide6.uic import loadUi

app = QApplication([])
widget = loadUi("test.ui")
widget.show()
app.exec()
```

### Step 2: 수동 .ui 생성 (1-2시간)
```python
# XML 직접 작성하는 헬퍼 함수
def create_login_ui():
    xml = """<?xml version="1.0"?>
    <ui version="4.0">
      <widget class="QDialog" name="LoginDialog">
        ...
      </widget>
    </ui>"""
    with open("login.ui", "w") as f:
        f.write(xml)
```

### Step 3: Screenshot 기능 (1시간)
```python
pixmap = widget.grab()
pixmap.save("screenshot.png")
```

### Step 4: 소켓 서버 추가 (2-3시간)
```python
# 간단한 명령 수신
import socket, json, threading

def listen():
    s = socket.socket()
    s.bind(("localhost", 7001))
    s.listen(1)
    while True:
        conn, _ = s.accept()
        cmd = json.loads(conn.recv(4096))
        if cmd["action"] == "screenshot":
            # take screenshot
            pass
```

**결과**: 4-6시간이면 기본 동작하는 프로토타입 완성

---

## 📊 리스크 분석

### High Risk
- **Socket 통신 안정성**: timeout, connection loss 처리
- **XML 파싱 에러**: 잘못된 .ui 파일 핸들링
- **Multi-threading**: Qt main thread vs socket thread

### Medium Risk
- **Bounding box 계산**: Hidden widget, nested layout
- **QSS 추출**: Inline style vs external stylesheet

### Low Risk
- **MCP 연동**: 표준 프로토콜이라 문서 잘 되어있음
- **.ui 생성**: ElementTree로 충분

---

## 💡 추천 개발 전략

### 옵션 A: 안정적 개발 (3-4주)
Phase 1 → 2 → 3 → 4 순차 진행
- 각 단계 철저히 테스트
- VFX 파이프라인 품질

### 옵션 B: 빠른 프로토타입 (1주)
Quick Start Path → 필요한 기능만 추가
- 핵심 워크플로우 먼저 검증
- 나중에 리팩토링

### 옵션 C: 하이브리드 (2주) ⭐ **추천**
```
Week 1: Phase 1 (Editor + .ui 조작) - 완성도 높게
Week 2: Phase 2-3 (Analyzer + MCP) - 빠르게 통합
```

---

## 📁 프로젝트 구조 (예상)

```
QtLiveDevTools/
├── live_ui_editor.py       # Main: Live UI Editor with socket server
├── ui_manager.py            # .ui XML parsing/modification
├── ui_analyzer.py           # Multi-layer analysis system
├── widget_inspector.py      # Widget search and inspection
├── mcp_server.py            # MCP server implementation
├── editor_client.py         # Socket client (MCP → Editor)
├── templates/               # Widget templates
│   ├── login_dialog.ui
│   ├── file_browser.ui
│   └── preferences.ui
├── styles/                  # QSS presets
│   ├── dark_theme.qss
│   └── light_theme.qss
├── tests/                   # Test .ui files
│   └── sample.ui
├── screenshots/             # Generated screenshots
├── CLAUDE.md               # Project documentation
├── PLAN.md                 # This file
└── requirements.txt        # Dependencies
```

---

## 🔧 기술 스택

### Core Dependencies
```
PySide6          # Qt for Python
mcp              # Model Context Protocol SDK
```

### Standard Library
```
xml.etree.ElementTree  # .ui XML parsing
socket                 # Network communication
threading              # Socket server thread
json                   # Command serialization
base64                 # Screenshot encoding
argparse               # CLI arguments
```

### Optional
```
watchdog         # File watching (.ui auto-reload)
pillow           # Advanced image processing
```

---

## 🎬 Next Steps

1. **Decide development strategy**: Quick Start vs Hybrid vs Full
2. **Set up project structure**: Create directories and empty files
3. **Install dependencies**: PySide6, MCP
4. **Start coding**: Begin with Quick Start Step 1 or Phase 1.1

Choose your path and let's build!
