# 🔄 PySide Version Converter Guide

## 개요

PySide6와 PySide2 간 자동 변환 도구입니다.

**사용 시나리오**:
- 프로젝트를 PySide6에서 PySide2로 다운그레이드
- 레거시 시스템 호환성을 위한 변환
- Maya 2023 이하 (PySide2) vs Maya 2024+ (PySide6)
- 팀 간 다른 PySide 버전 사용 시

---

## 🎯 주요 기능

### 1. .ui 파일 변환
- XML 주석에 버전 정보 추가
- Qt enum 문법 변환 (PySide6 ↔ PySide2)

### 2. Python 스크립트 변환
- Import 문 자동 변경 (`PySide6` ↔ `PySide2`)
- API 차이 자동 수정 (`.exec()` ↔ `.exec_()`)
- Qt enum 문법 변환
- Qt6 전용 플래그 자동 주석 처리

### 3. 디렉토리 일괄 변환
- 모든 .ui 및 .py 파일 한 번에 변환
- 변환 리포트 자동 생성
- 에러 및 경고 추적

---

## 📝 API 차이점

### PySide6 → PySide2 변환 시

| 항목 | PySide6 | PySide2 | 자동 변환 |
|------|---------|---------|----------|
| Import | `from PySide6.QtWidgets import ...` | `from PySide2.QtWidgets import ...` | ✅ |
| Dialog exec | `.exec()` | `.exec_()` | ✅ |
| Qt Enums | `Qt.AlignmentFlag.AlignCenter` | `Qt.AlignCenter` | ✅ |
| HiDPI Flags | `Qt.AA_EnableHighDpiScaling` | (제거 - 주석 처리) | ✅ |

### 변환 예시

**Before (PySide6)**:
```python
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt

class MyDialog(QDialog):
    def show_dialog(self):
        return self.exec()  # PySide6 style
```

**After (PySide2)**:
```python
from PySide2.QtWidgets import QDialog, QPushButton
from PySide2.QtCore import Qt

class MyDialog(QDialog):
    def show_dialog(self):
        return self.exec_()  # PySide2 style
```

---

## 🚀 사용 방법

### 방법 1: Claude CLI에서 사용

```
You: "현재 디렉토리의 모든 파일을 PySide2로 변환해줘"

Claude:
[convert_pyside_version("pyside2", ".")]

Report:
✅ 33개 파일 변환 완료
   - 25개 UI 파일
   - 8개 Python 파일
```

### 방법 2: MCP 함수 (Python API)

```python
from mcp_server import convert_pyside_version

# 전체 프로젝트 변환
result = convert_pyside_version(
    target_version="pyside2",
    file_path=".",  # 현재 디렉토리
    ui_files=True,
    py_files=True
)

print(result['report'])
```

### 방법 3: 커맨드라인 도구

```bash
# 단일 파일 변환
python pyside_converter.py pyside2 --file my_dialog.ui

# 디렉토리 전체 변환
python pyside_converter.py pyside2 --dir /path/to/project

# UI 파일만 변환
python pyside_converter.py pyside2 --dir . --ui-only

# Python 파일만 변환
python pyside_converter.py pyside6 --dir . --py-only
```

---

## 📊 변환 리포트

### 샘플 리포트

```
======================================================================
PySide Version Conversion Report
======================================================================

✅ Files Converted: 33
⚠️  Warnings: 13
❌ Errors: 0

📁 Converted Files:
   ✓ login_dialog.ui
      - Added version comment: pyside2

   ✓ live_ui_editor.py
      - Imports: PySide6 → PySide2
      - Method: .exec() → .exec_()

   ✓ test_ui_viewer.py
      - Imports: PySide6 → PySide2
      - Method: .exec() → .exec_()

⚠️  Warnings:
   - ui_manager.py: No changes needed (no PySide imports)
   - mcp_server.py: No changes needed (no PySide imports)

======================================================================
```

---

## 🎬 실전 시나리오

### 시나리오 1: Maya 2023 호환성

**상황**: PySide6로 개발했지만 Maya 2023에서 사용해야 함

```
You: "이 프로젝트를 Maya 2023용으로 변환해줘"

Claude:
Maya 2023은 PySide2를 사용합니다.

[convert_pyside_version("pyside2", ".")]

✓ 전체 프로젝트 PySide2로 변환 완료
✓ Maya 2023에서 바로 사용 가능합니다
```

### 시나리오 2: 최신 버전 업그레이드

**상황**: 레거시 PySide2 프로젝트를 PySide6로 마이그레이션

```
You: "legacy 폴더를 PySide6로 업그레이드해줘"

Claude:
[convert_pyside_version("pyside6", "legacy")]

Report:
✓ 45개 파일 변환
✓ Python 3.9+ 및 Qt 6 호환

주의사항:
- Qt6에서 제거된 API 확인 필요
- 동작 테스트 권장
```

### 시나리오 3: 선택적 변환

**상황**: UI 파일만 변환하고 Python 코드는 유지

```
You: "UI 파일만 PySide2로 변환해줘"

Claude:
[convert_pyside_version("pyside2", ".", ui_files=True, py_files=False)]

✓ 25개 UI 파일 변환
✓ Python 스크립트는 변경 안 함
```

---

## ⚠️ 주의사항

### 1. 자동 변환 한계

**완전 자동 변환 가능**:
- ✅ Import 문
- ✅ `.exec()` / `.exec_()` 메서드
- ✅ 기본 Qt enum
- ✅ UI 파일 구조

**수동 확인 필요**:
- ⚠️ Qt6에서 제거된 API (deprecated 메서드)
- ⚠️ 커스텀 Qt 클래스 상속
- ⚠️ Signal/Slot 서명 변경
- ⚠️ 플랫폼 별 동작 차이

### 2. 변환 전 체크리스트

- [ ] 원본 백업 (Git commit 또는 복사)
- [ ] 타겟 PySide 버전 환경 준비
- [ ] 의존성 패키지 호환성 확인
- [ ] 테스트 환경 준비

### 3. 변환 후 체크리스트

- [ ] Import 문 확인
- [ ] 애플리케이션 실행 테스트
- [ ] UI 로딩 테스트
- [ ] Signal/Slot 동작 확인
- [ ] 플랫폼별 테스트 (Windows, Linux, macOS)

---

## 🔍 트러블슈팅

### 문제 1: "No changes needed" 경고 많이 발생

**원인**: 해당 파일에 PySide import가 없음

**해결**: 정상 동작입니다. PySide를 사용하지 않는 파일은 변환 불필요

### 문제 2: 변환 후 import 에러

**원인**: 타겟 PySide 버전이 설치 안 됨

**해결**:
```bash
# PySide2 설치
pip install PySide2

# 또는 PySide6 설치
pip install PySide6
```

### 문제 3: exec_() 관련 에러

**원인**: 자동 변환이 일부 누락

**해결**: 수동으로 확인
```python
# PySide6
dialog.exec()

# PySide2
dialog.exec_()
```

---

## 📦 VFX 파이프라인 통합

### Rez 환경에서 사용

```bash
# PySide6 환경
rez-env pyside6 -- python my_tool.py

# PySide2로 변환 후
python pyside_converter.py pyside2 --dir .

# PySide2 환경에서 실행
rez-env pyside2 -- python my_tool.py
```

### Maya 버전별 대응

```python
# Maya 버전에 따라 자동 변환
import os

maya_version = int(os.getenv("MAYA_VERSION", "2024"))

if maya_version < 2024:
    # Maya 2023 이하 - PySide2 사용
    convert_pyside_version("pyside2", ".")
else:
    # Maya 2024+ - PySide6 사용
    convert_pyside_version("pyside6", ".")
```

---

## 🧪 테스트

### 테스트 실행

```bash
python test_pyside_converter.py
```

### 테스트 커버리지

✅ UI 파일 변환 (PySide6 → PySide2)
✅ Python 스크립트 변환 (PySide6 → PySide2)
✅ 역변환 (PySide2 → PySide6)
✅ 디렉토리 배치 변환
✅ 상세 리포트 생성

---

## 🎯 다음 단계

### 변환 후:

1. **테스트 실행**
   ```bash
   # 모든 테스트 실행
   python -m pytest tests/
   ```

2. **UI 로딩 확인**
   ```bash
   # Live Editor로 확인
   rez-env pyside2 -- python live_ui_editor.py --ui my_dialog.ui
   ```

3. **변경사항 커밋**
   ```bash
   git add .
   git commit -m "Convert to PySide2 for Maya 2023 compatibility"
   ```

---

## 📚 관련 문서

- `FINAL_SUMMARY.md` - 프로젝트 전체 요약
- `QT_ALL_FEATURES_SUPPORTED.md` - Qt 기능 가이드
- `REFERENCE_CLONE_GUIDE.md` - UI 복제 가이드
- `SESSION_NOTES.md` - 개발 노트

---

## 💡 팁

### 빠른 변환

```bash
# 현재 디렉토리 전체를 PySide2로
python pyside_converter.py pyside2 --dir .

# 다시 PySide6로
python pyside_converter.py pyside6 --dir .
```

### Claude CLI와 함께

```
You: "이 프로젝트를 PySide2로 바꿔줘"
Claude: [자동 변환 + 리포트]

You: "테스트 돌려줘"
Claude: [pytest 실행 + 결과 분석]

You: "문제 있으면 고쳐줘"
Claude: [에러 수정 + 재테스트]
```

---

**작성일**: 2025-11-15
**버전**: 1.0
**상태**: 프로덕션 준비 완료

**개발자**: chulho@m83.studio
