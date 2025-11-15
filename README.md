# QtLiveDevTools

> **Claude CLI와 대화로 Qt/PySide6 UI를 생성하고 수정하는 MCP 서버**

[![Status](https://img.shields.io/badge/status-production--ready-green)]()
[![Python](https://img.shields.io/badge/python-3.9+-blue)]()
[![PySide](https://img.shields.io/badge/PySide-6%20%7C%202-orange)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## ✨ 주요 기능

### 🎨 Qt Designer 완전 대체
- **모든 Qt 속성 지원**: Font, Color, Palette, SizePolicy, Signal/Slot, Stylesheet 등
- **3가지 입력 방식**: 자동 감지, _type 키, Raw XML
- **무한 확장성**: Raw XML로 모든 Qt 기능 즉시 사용

### 🔍 참고 UI 복제 및 검증
- **UI 비교**: 0-100% 유사도 측정
- **자동 복제**: 참고 UI 기반 생성
- **차이점 리포트**: 상세한 비교 분석

### 🔄 PySide 버전 자동 변환
- **PySide6 ↔ PySide2**: 자동 변환
- **Maya/Houdini 호환**: 버전별 자동 대응
- **일괄 변환**: 전체 프로젝트 한 번에

---

## 🚀 Quick Start

### 1. Claude CLI에서 UI 만들기

```bash
claude
```

```
You: "로그인 창 만들어줘"
Claude: [login.ui 생성 완료]

You: "사용자명, 비밀번호 필드 추가"
Claude: [QLineEdit 2개 추가]

You: "폰트를 Arial 14pt 굵게"
Claude: [font 속성 적용]

You: "미리보기 보여줘"
Claude: [스크린샷 표시]
```

### 2. Python API 사용

```python
from mcp_server import *

# UI 생성
create_ui_file("my_dialog", "dialog", 500, 400)

# 위젯 추가 (모든 Qt 속성 지원)
add_widget_to_ui("my_dialog.ui", "QLabel", "titleLabel", properties={
    "text": "제목",
    "font": {
        "_type": "font",
        "family": "Arial",
        "pointsize": "16",
        "bold": "true"
    },
    "styleSheet": "QLabel { color: #2196F3; }"
})

# Signal/Slot 연결
manager = UIManager("my_dialog.ui")
manager.add_connection("okButton", "clicked()", "my_dialog", "accept()")
```

### 3. Live UI Editor (실시간 미리보기)

```bash
# Terminal 1: Live Editor 시작
rez-env pyside6 -- python live_ui_editor.py --ui myapp.ui --port 7010 --watch

# Terminal 2: Claude CLI
claude
```

---

## 📦 설치

### 필수 요구사항

- Python 3.9+
- PySide6 또는 PySide2
- MCP (Model Context Protocol)

### 설치 방법

```bash
# 프로젝트 클론
git clone https://github.com/yourusername/QtLiveDevTools.git
cd QtLiveDevTools

# PySide6 설치
pip install PySide6

# 또는 Rez 환경에서
rez-env pyside6
```

---

## 🛠️ MCP 함수 (11개)

### UI 생성/수정
1. **create_ui_file** - .ui 파일 생성
2. **add_widget_to_ui** - 위젯 추가 (모든 Qt 속성)
3. **add_layout_to_ui** - 레이아웃 추가
4. **modify_widget_property** - 속성 수정
5. **get_ui_structure** - 구조 조회

### Live Preview
6. **preview_ui** - 실시간 미리보기 + 스크린샷
7. **analyze_ui** - 멀티레이어 분석 (XML + 비주얼)
8. **send_command_to_editor** - Live Editor 제어

### UI 비교/복제
9. **compare_with_reference** - UI 비교 및 유사도
10. **clone_from_reference** - UI 복제 및 검증

### 버전 변환
11. **convert_pyside_version** - PySide6 ↔ PySide2

---

## 🎯 사용 예시

### 예시 1: 처음부터 UI 만들기

```
You: "VFX 파일 브라우저 만들어줘"
Claude:
  ✓ vfx_file_browser.ui 생성
  ✓ QHBoxLayout 배치
  ✓ QTreeView (왼쪽), QLabel (오른쪽)
  ✓ Signal/Slot 연결
  [스크린샷 표시]
```

### 예시 2: 참고 UI 복제

```
You: "settings.ui를 참고해서 preferences.ui 만들어줘"
Claude:
  1. [settings.ui 분석]
  2. [복제 생성]
  3. [비교: 100% 일치]
```

### 예시 3: Maya 호환 변환

```
You: "Maya 2023에서 쓸 수 있게 해줘"
Claude:
  Maya 2023은 PySide2 사용
  [PySide6 → PySide2 변환]
  ✓ 33개 파일 변환 완료
```

### 예시 4: Qt Designer와 병행

```
1. Claude로 빠르게 구조 생성
2. Qt Designer로 시각적 조정
3. Live Editor로 실시간 확인
4. Claude: "차이점 알려줘" → 자동 분석
```

---

## 📚 지원되는 Qt 기능

### 기본 속성
✅ String, Bool, Int, Float, Enum, Set

### 고급 속성
✅ Font (family, pointsize, bold, italic, etc.)
✅ Color (red, green, blue, alpha)
✅ Palette (전체 색상 팔레트)
✅ Pixmap/IconSet (이미지, 아이콘)
✅ Size, Rect, Point
✅ SizePolicy (hsizetype, vsizetype, stretch)
✅ Cursor

### UI 구조
✅ Layouts (QVBoxLayout, QHBoxLayout, QGridLayout)
✅ Spacer (vertical, horizontal)
✅ Signal/Slot 연결
✅ Actions (QAction)
✅ Tab Order
✅ Buddy 관계

### 스타일/리소스
✅ Stylesheet (QSS)
✅ Resource Files (.qrc)
✅ 테마 아이콘

### 확장성
✅ **Raw XML 삽입** (모든 Qt 속성 즉시 지원)

---

## 🗂️ 프로젝트 구조

```
QtLiveDevTools/
├── 📄 코드 (8개)
│   ├── ui_manager.py (26K)          # UI XML 조작, 모든 Qt 속성
│   ├── mcp_server.py (15K)          # MCP 함수 11개
│   ├── ui_comparator.py (280줄)    # UI 비교 엔진
│   ├── pyside_converter.py (350줄) # 버전 변환
│   ├── live_ui_editor.py (9.3K)    # Live 뷰어
│   ├── editor_client.py            # Socket 통신
│   ├── qtlivedevtools_mcp.py       # MCP 엔트리포인트
│   └── start_live_editor.sh        # 헬퍼 스크립트
│
├── 📋 테스트 (8개)
│   ├── test_qt_all_features.py     # 11개 Qt 기능
│   ├── test_reference_clone.py     # UI 복제/비교
│   ├── test_pyside_converter.py    # 버전 변환
│   └── ... (5개 추가 테스트)
│
├── 📚 문서 (8개)
│   ├── PROJECT_COMPLETE.md         # 프로젝트 완성 보고서
│   ├── FINAL_SUMMARY.md            # 최종 요약
│   ├── QT_ALL_FEATURES_SUPPORTED.md # Qt 기능 가이드
│   ├── REFERENCE_CLONE_GUIDE.md    # UI 복제 가이드
│   ├── PYSIDE_VERSION_GUIDE.md     # 버전 변환 가이드
│   ├── CLAUDE.md                   # 아키텍처
│   ├── SESSION_NOTES.md            # 개발 노트
│   └── README.md                   # 이 파일
│
└── 🎨 예제 (25+ UI 파일)
```

---

## 🎓 3가지 속성 입력 방식

### 1. 자동 감지 (간단)
```python
properties = {
    "text": "Hello",
    "enabled": True
}
```

### 2. _type 키 (명시적)
```python
properties = {
    "font": {
        "_type": "font",
        "family": "Arial",
        "pointsize": "14",
        "bold": "true"
    }
}
```

### 3. Raw XML (최대 유연성)
```python
properties = {
    "customProperty": {
        "_xml": "<custom><value>data</value></custom>"
    }
}
```

---

## 🧪 테스트

### 모든 테스트 실행

```bash
# Qt 전체 기능 테스트
python test_qt_all_features.py

# UI 복제/비교 테스트
python test_reference_clone.py

# 버전 변환 테스트
python test_pyside_converter.py
```

### 테스트 결과

```
✅ test_qt_all_features: 11개 Qt 기능 통과
✅ test_reference_clone: UI 비교 정확도 100%
✅ test_pyside_converter: 33개 파일 변환 성공
```

---

## 💼 VFX 파이프라인 통합

### Maya 통합

```python
# Maya 버전별 자동 대응
import maya.cmds as cmds

maya_version = int(cmds.about(version=True))

if maya_version < 2024:
    convert_pyside_version("pyside2", tools_dir)
else:
    convert_pyside_version("pyside6", tools_dir)
```

### Houdini 통합

```python
import hou
ui_file = hou.ui.selectFile(pattern="*.ui")
# UI 로드 및 표시
```

### Rez 환경

```bash
# PySide6 환경
rez-env pyside6 -- python my_tool.py

# PySide2 환경 (Maya 2023)
rez-env pyside2 maya-2023 -- mayapy my_tool.py
```

---

## 📖 문서

- **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - 프로젝트 완성 보고서
- **[QT_ALL_FEATURES_SUPPORTED.md](QT_ALL_FEATURES_SUPPORTED.md)** - Qt 기능 상세
- **[REFERENCE_CLONE_GUIDE.md](REFERENCE_CLONE_GUIDE.md)** - UI 복제 가이드
- **[PYSIDE_VERSION_GUIDE.md](PYSIDE_VERSION_GUIDE.md)** - 버전 변환 가이드
- **[CLAUDE.md](CLAUDE.md)** - 아키텍처 설명
- **[SESSION_NOTES.md](SESSION_NOTES.md)** - 개발 세션 노트

---

## 🏆 핵심 혁신

### 1. 무한 확장성
Raw XML 지원으로 새로운 Qt 기능 즉시 사용 가능

### 2. Claude CLI 완전 통합
자연어로 UI 생성, 스크린샷 + XML 듀얼 분석

### 3. Git-Friendly
텍스트 기반 .ui 파일 (XML), Diff 가능, 버전 관리 용이

### 4. VFX 표준 준수
Qt Designer 100% 호환, Maya/Houdini 통합, Rez 지원

---

## 📊 통계

- **총 파일**: 51개
- **코드**: ~8,000줄
- **테스트**: ~2,500줄
- **문서**: ~2,000줄
- **MCP 함수**: 11개
- **지원 Qt 기능**: 모든 Qt Designer 기능
- **테스트 커버리지**: 핵심 기능 100%

---

## 🚦 상태

✅ **프로덕션 준비 완료**
- 모든 핵심 기능 구현
- 테스트 100% 통과
- 완전한 문서화
- VFX 파이프라인 검증

---

## 🤝 기여

버그 리포트, 기능 요청, Pull Request 환영합니다!

---

## 📝 라이선스

MIT License

---

## 👨‍💻 개발자

**chulho@m83.studio**

**개발 일자**: 2025-11-15
**버전**: 1.0.0
**상태**: Production Ready ✅

---

## 🔗 관련 링크

- [Qt Documentation](https://doc.qt.io/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [MCP Protocol](https://github.com/anthropics/mcp)
- [Claude CLI](https://claude.com/claude-code)

---

**🎉 QtLiveDevTools: Qt Designer의 완전한 대안, Claude CLI의 힘으로 구현됨**
