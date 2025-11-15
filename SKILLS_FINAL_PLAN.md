# QtLiveDevTools Skills 최종 계획서

## 🎯 프로젝트 목표

**레퍼런스 이미지 기반 Qt UI 자동 제작 시스템**
- 사용자가 레퍼런스 이미지 제공 → Claude가 서브에이전트 팀을 조율하여 UI 완성
- 반복 평가 및 개선으로 80점 이상 달성까지 자동 진행

### 💎 핵심 기능: 실시간 협업 워크플로우

**Claude ↔ 사용자 동시 UI 작업**

```
Claude (Skills)              사용자 (Qt Designer)
    ↓                              ↓
.ui 파일 수정         ←→   .ui 파일 수정
    ↓                              ↓
Git 자동 감지         ←→   수동 저장
    ↓                              ↓
재평가 및 개선        ←→   시각적 조정
```

**장점:**
- ✅ Claude가 구조/로직 담당 → 사용자가 세밀한 디자인 조정
- ✅ .ui 파일 = 텍스트 XML → 동시 수정 가능 (Merge 가능)
- ✅ Qt Designer로 즉시 확인 → 빠른 피드백
- ✅ 각자 장점 활용: Claude=속도, 사용자=미적 감각

---

## 📋 기술 스택 및 환경

### 필수 패키지
```bash
rez-env qt6 pyside6 python-3.13
```

### 선택 패키지 (필요시 추가)
```bash
rez-env qt6 pyside6 python-3.13 tractor shotgun_api3
```

### 개발 원칙

1. **UI 파일 우선 (.ui)**
   - 모든 UI는 `.ui` 파일로 먼저 제작
   - Qt Designer XML 형식 준수
   - .ui 파일로 구현 불가능한 경우에만 PySide6 API 사용

2. **메인 UI 구조**
   - 메인 `.ui` 파일 1개 (main_window.ui)
   - 서브 UI 위젯들은 메인 UI 내부에 구성
   - 계층 구조로 관리

3. **Git 친화성**
   - 모든 `.ui` 파일은 텍스트 기반 XML
   - Diff 가능, 버전 관리 용이

---

## 🔄 작동 방식

### 전체 워크플로우

```
1. 사용자 입력
   ↓ (레퍼런스 이미지 or 요구사항)

2. Qt Designer로 .ui 파일 작성
   ↓ (main_window.ui 생성)

3. UI 실행 및 스크린샷
   ↓ (rez-env qt6 pyside6 python-3.13 -- python src/main.py)

4. 레퍼런스 vs 현재 UI 비교 (팀장 평가)
   ↓ (0-100점 점수 부여)

5. 서브에이전트 팀 병렬 작업 (80점 미만인 경우)
   ↓ (UI 구성, 배치, 레이아웃, 컬러, 아이콘 각 팀)

6. 재평가 및 반복
   ↓ (80점 이상 달성까지)

7. 완성 ✅
```

### 단계별 상세 설명

#### Step 1: 사용자 요구사항 입력

**입력 형식:**
- **레퍼런스 이미지**: `sample_ui_image.png`
- **텍스트 설명**: "Shotgun 스타일의 파일 관리 UI 만들어줘"
- **혼합**: 이미지 + 추가 요구사항

**예시:**
```
사용자: "이 이미지처럼 만들어줘 [sample_ui_image.png 첨부]"
         "왼쪽에 통계, 중간에 워크플로우, 오른쪽에 사이드바"
```

#### Step 2: .ui 파일 작성

**Skills에서 수행:**
```python
# ui_manager.py 사용
create_ui_file("main_window", "mainwindow", 1200, 800)

# 위젯 추가 (XML 기반)
add_widget_to_ui("main_window.ui", "QWidget", "centralWidget", {...})
add_layout_to_ui("main_window.ui", "QVBoxLayout", "mainLayout")

# 서브 위젯 추가
add_widget_to_ui("main_window.ui", "QWidget", "headerWidget", {...})
add_widget_to_ui("main_window.ui", "QWidget", "statsArea", {...})
add_widget_to_ui("main_window.ui", "QWidget", "workflowArea", {...})
```

**출력:**
- `main_window.ui` (Qt Designer 호환 XML)

#### Step 3: UI 실행 및 스크린샷

**실행 스크립트 (src/main.py):**
```python
#!/usr/bin/env python
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

def main():
    app = QApplication(sys.argv)
    loader = QUiLoader()

    # .ui 파일 로드
    window = loader.load("main_window.ui")
    window.show()

    # 스크린샷 자동 촬영 (선택)
    # pixmap = window.grab()
    # pixmap.save("current_ui_screenshot.png")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

**실행 명령:**
```bash
# UI 실행
rez-env qt6 pyside6 python-3.13 -- python src/main.py

# 백그라운드 실행
rez-env qt6 pyside6 python-3.13 -- python src/main.py &

# 스크린샷만 촬영 후 종료
rez-env qt6 pyside6 python-3.13 -- python src/screenshot.py
```

**스크린샷 스크립트 (src/screenshot.py):**
```python
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QTimer

app = QApplication(sys.argv)
loader = QUiLoader()
window = loader.load("main_window.ui")
window.show()

# 렌더링 대기 후 스크린샷
def capture():
    pixmap = window.grab()
    pixmap.save("current_ui_screenshot.png")
    print("✅ Screenshot saved: current_ui_screenshot.png")
    app.quit()

QTimer.singleShot(500, capture)  # 0.5초 대기
app.exec()
```

#### Step 4: 팀장 평가 (스크린샷 비교)

**팀장 역할:**
1. 레퍼런스 이미지 로드: `sample_ui_image.png`
2. 현재 UI 스크린샷 로드: `current_ui_screenshot.png`
3. 각 담당 팀별 점수 부여 (0-100점)

**평가 항목:**

| 팀 | 평가 항목 | 목표 점수 |
|-----|----------|----------|
| **UI 구성** | Header, Tabs, Stats, Workflow, Table, Buttons, Sidebar 존재 여부 | 80점 |
| **UI 배치** | Stats 4개 카드 간격, Workflow 위치, Tabs 정렬, Table 컬럼, 버튼 위치 | 80점 |
| **레이아웃** | Vertical spacing, Horizontal alignment, Padding, Card spacing | 80점 |
| **컬러** | Background, Card colors, Borders, Text colors, Badge colors | 80점 |
| **아이콘** | Stat icons, Workflow icons, Arrows, Tab icons, Button icons | 80점 |

**평가 출력 예시:**
```json
{
  "total_score": 65,
  "teams": {
    "ui_structure": {"score": 85, "status": "✅ PASS"},
    "ui_placement": {"score": 50, "status": "❌ FAIL - Stats 간격 불균등"},
    "layout": {"score": 70, "status": "❌ FAIL - Vertical spacing 부족"},
    "color": {"score": 60, "status": "❌ FAIL - Background gradient 누락"},
    "icon": {"score": 80, "status": "✅ PASS"}
  },
  "action": "80점 미만 팀에게 작업 지시"
}
```

#### Step 5: 서브에이전트 팀 병렬 작업

**팀 구성 및 역할:**

##### 1️⃣ 팀장 (Team Leader)
- **역할**: 스크린샷 평가 및 점수 부여
- **입력**: `sample_ui_image.png`, `current_ui_screenshot.png`
- **출력**: 각 팀별 점수 (0-100점)
- **목표**: 전체 80점 이상 달성

##### 2️⃣ UI 구성 담당 (UI Structure Team)
- **역할**: 필수 UI 요소 존재 확인 및 추가
- **체크 항목**:
  - ✅ Header (제목, 사용자 프로필, 설정 아이콘)
  - ✅ Mode Tabs (컨버팅 / 데이터 펍)
  - ✅ Stats Area (4개 통계 카드)
  - ✅ Workflow Area (3개 플로우 카드)
  - ✅ Status Filter Tabs (5개 탭)
  - ✅ File List Table (8개 컬럼)
  - ✅ Action Buttons (Scan, Convert)
  - ✅ Right Sidebar
- **작업 방법**: `.ui` 파일에 누락된 위젯 추가

##### 3️⃣ UI 배치 담당 (UI Placement Team) [최우선]
- **역할**: 위젯 정확한 위치 및 간격 조정
- **체크 항목**:
  - ✅ Stats Area: 4개 카드 동일 간격 (예: 10px)
  - ✅ Workflow Area: 3개 카드 + 2개 화살표 정확한 위치
  - ✅ Status Filter Tabs: 5개 탭 왼쪽 정렬
  - ✅ File List Table: 8개 컬럼 순서 및 너비
  - ✅ Action Buttons: 하단 오른쪽 정렬
  - ✅ Right Sidebar: 고정 너비 (예: 250px)
- **작업 방법**: `geometry` 속성 수정

##### 4️⃣ 레이아웃 담당 (Layout Team)
- **역할**: QVBoxLayout, QHBoxLayout 등 레이아웃 설정
- **체크 항목**:
  - ✅ Vertical spacing between sections (예: 20px)
  - ✅ Horizontal alignment (Left, Center, Right)
  - ✅ Container padding (예: 10px)
  - ✅ Card spacing (예: 15px)
  - ✅ Button grouping (QHBoxLayout)
  - ✅ Sidebar width ratio (예: 20%)
- **작업 방법**: `add_layout_to_ui()` 사용

##### 5️⃣ 컬러 담당 (Color Team)
- **역할**: 배경, 텍스트, 테두리 색상 설정
- **체크 항목**:
  - ✅ Main background gradient (slate-900 to slate-800)
  - ✅ Card backgrounds with transparency
  - ✅ Stat card borders (Blue, Gray, Yellow, Green)
  - ✅ Workflow card gradients (Blue, Purple, Green)
  - ✅ Button colors (Blue for scan, Green for convert)
  - ✅ Text colors (White, Gray-400)
  - ✅ Status badge colors (Green, Yellow, Red, Gray)
  - ✅ Mode tab colors (Active vs Inactive)
- **작업 방법**: `styleSheet` 속성 수정 (QSS)

##### 6️⃣ 아이콘 담당 (Icon Team)
- **역할**: 아이콘 추가 및 크기 조정
- **체크 항목**:
  - ✅ Stat card icons (☰, ⏱, ⟳, ✓) - 24x24px
  - ✅ Workflow card icons (📁, 🖥, ⚙) - 24x24px
  - ✅ Workflow arrows (→) - 16px
  - ✅ Mode tab icons (↻, ⬇) - 16px
  - ✅ Status filter icons - 16px
  - ✅ Action button icons
  - ✅ User profile/Settings icons
- **작업 방법**: `icon` 속성 또는 `text` 속성에 Unicode 이모지

**병렬 실행 예시:**

```python
# Claude Skills에서 Task Tool 사용
Task(
    subagent_type="general-purpose",
    description="UI 구성 수정",
    prompt="""
    main_window.ui 파일을 분석하고 누락된 UI 요소를 추가하세요.

    체크리스트:
    - Header Widget
    - Mode Tabs
    - Stats Area (4개 카드)
    - Workflow Area (3개 카드)
    - Status Filter Tabs (5개)
    - File List Table
    - Action Buttons
    - Right Sidebar

    누락된 항목을 ui_manager.py를 사용하여 추가하세요.
    """
)

Task(
    subagent_type="general-purpose",
    description="UI 배치 수정",
    prompt="""
    main_window.ui의 위젯 배치를 레퍼런스 이미지와 일치시키세요.

    우선순위:
    1. Stats Area 4개 카드 동일 간격
    2. Workflow Area 정확한 위치
    3. Table 컬럼 순서 및 너비
    4. Action Buttons 위치

    geometry 속성을 수정하세요.
    """
)

Task(
    subagent_type="general-purpose",
    description="컬러 수정",
    prompt="""
    main_window.ui의 색상을 레퍼런스 이미지와 일치시키세요.

    컬러 팔레트:
    - Background: slate-900 to slate-800 gradient
    - Stat borders: Blue, Gray, Yellow, Green
    - Workflow: Blue, Purple, Green gradients

    styleSheet 속성을 수정하세요.
    """
)

Task(
    subagent_type="general-purpose",
    description="아이콘 교체",
    prompt="""
    main_window.ui의 아이콘을 추가/교체하세요.

    아이콘 목록:
    - Stat icons: ☰ ⏱ ⟳ ✓ (24x24px)
    - Workflow icons: 📁 🖥 ⚙ (24x24px)
    - Arrows: → (16px)

    text 또는 icon 속성을 수정하세요.
    """
)
```

#### Step 6: 재평가 및 반복

**프로세스 재시작:**
```bash
# 기존 프로세스 종료
pkill -f "python src/main.py"

# UI 재실행
rez-env qt6 pyside6 python-3.13 -- python src/main.py &

# 스크린샷 재촬영
sleep 1
rez-env qt6 pyside6 python-3.13 -- python src/screenshot.py
```

**재평가:**
```
팀장 → 스크린샷 비교 → 점수 부여

if 총점 >= 80:
    완료 ✅
else:
    80점 미만 팀에게 재작업 지시 → Step 5 반복
```

**종료 조건:**
- 전체 80점 이상 달성
- 또는 최대 반복 횟수 도달 (예: 5회)

---

## 🤝 실시간 협업 워크플로우 (핵심!)

### Claude와 사용자가 동시에 UI 작업

**시나리오:**

```
1. Claude가 main_window.ui 기본 구조 생성
   ↓
2. 사용자가 Qt Designer로 main_window.ui 열기
   designer main_window.ui &
   ↓
3. Claude가 Stats Area 추가 (서브에이전트)
   ↓
4. 사용자가 Qt Designer에서 "새로고침" (F5)
   → Claude가 추가한 Stats Area 즉시 확인
   ↓
5. 사용자가 Stats 카드 위치를 드래그로 조정
   → Qt Designer에서 저장 (Ctrl+S)
   ↓
6. Claude가 .ui 파일 변경 감지
   → 사용자의 수정 사항 읽기
   → 다음 작업에 반영
   ↓
7. Claude가 Workflow Area 추가
   ↓
8. 사용자가 Qt Designer 새로고침
   → Workflow 확인 및 색상 조정
   ↓
... 반복 ...
```

### .ui 파일 동시 수정 가능한 이유

**XML 텍스트 기반:**
```xml
<!-- Claude가 추가한 부분 -->
<widget class="QWidget" name="statsArea">
  <property name="geometry">
    <rect><x>10</x><y>50</y><width>800</width><height>100</height></rect>
  </property>
</widget>

<!-- 사용자가 Qt Designer로 추가한 부분 -->
<widget class="QPushButton" name="customButton">
  <property name="text"><string>Custom</string></property>
</widget>
```

**Merge 가능:**
- Git처럼 병합 가능
- 충돌 시 사용자 우선 (Qt Designer 저장본 기준)

### 협업 규칙

#### Claude의 역할:
1. **구조 생성** - Header, Stats, Workflow, Table 등 큰 틀
2. **반복 작업** - 4개 Stats 카드, 5개 Status 탭 등
3. **속성 설정** - geometry, text, styleSheet 등
4. **자동 평가** - 레퍼런스와 비교하여 점수 부여

#### 사용자의 역할:
1. **시각적 조정** - 드래그로 위치 미세 조정
2. **색상 미세 조정** - Qt Designer 색상 팔레트 사용
3. **텍스트 수정** - 라벨, 버튼 텍스트 직접 입력
4. **추가 위젯** - 특수 위젯 드래그 앤 드롭

### 충돌 방지 전략

**1. 작업 영역 분리:**
```
Claude:
- Header (y: 0-50)
- Stats Area (y: 50-150)
- Workflow Area (y: 150-300)

사용자:
- 각 영역 내부의 세밀한 조정
- 색상, 폰트, 간격 등
```

**2. 턴 기반 작업:**
```
Turn 1: Claude → Stats Area 생성
        사용자 → Qt Designer에서 확인 및 조정

Turn 2: Claude → Workflow Area 생성
        사용자 → Qt Designer에서 확인 및 조정

Turn 3: Claude → Table 생성
        사용자 → 컬럼 너비 조정
```

**3. 변경 감지:**
```python
# helpers/file_watcher.py
import time
import os

last_modified = os.path.getmtime("main_window.ui")

while True:
    current_modified = os.path.getmtime("main_window.ui")
    if current_modified > last_modified:
        print("✅ User modified main_window.ui")
        print("   Waiting for user to finish...")
        time.sleep(2)  # 2초 대기
        last_modified = current_modified
    time.sleep(1)
```

### 실전 예시

**사용자:**
```
"로그인 창 만들어줘.
 내가 Qt Designer로 버튼 위치 조정할 테니까
 너는 기본 구조만 만들어줘."
```

**Claude (Skills):**
```python
# 1. 기본 구조 생성
create_ui_file("login_dialog", "dialog", 400, 300)
add_widget_to_ui("login_dialog.ui", "QLabel", "titleLabel", {...})
add_widget_to_ui("login_dialog.ui", "QLineEdit", "usernameEdit", {...})
add_widget_to_ui("login_dialog.ui", "QPushButton", "loginButton", {...})

print("✅ login_dialog.ui 생성 완료!")
print("   Qt Designer로 열어서 조정하세요:")
print("   designer login_dialog.ui")
```

**사용자:**
```bash
# Qt Designer 실행
designer login_dialog.ui

# (GUI로 버튼 드래그, 색상 변경)
# 저장 (Ctrl+S)
```

**Claude (자동 감지):**
```
✅ User modified login_dialog.ui
   Reading changes...
   - loginButton moved to (150, 250)
   - loginButton color changed to blue

   Applying these changes to evaluation...
```

### Qt Designer 실시간 새로고침 팁

**방법 1: 수동 새로고침**
```
Qt Designer에서:
1. File → Revert (또는 Ctrl+R)
2. Claude의 변경 사항 즉시 반영
```

**방법 2: 자동 새로고침 (inotify)**
```bash
# Linux에서 파일 변경 감지
inotifywait -m main_window.ui -e modify |
while read; do
    echo "File changed, reload Qt Designer!"
done
```

**방법 3: UI 재실행**
```bash
# Claude가 수정 후 자동 재실행
pkill -f "python src/main.py"
rez-env qt6 pyside6 python-3.13 -- python src/main.py &
```

### 협업 모드 활성화

**SKILL.md에 추가할 내용:**

```yaml
---
name: qtlivedevtools
description: Create Qt UI with real-time collaboration. User can edit .ui file with Qt Designer while Claude modifies structure. Use when user wants to co-design Qt interface.
collaboration_mode: true  # 협업 모드
---

## Collaboration Workflow

When user says:
- "나도 Qt Designer로 수정할게"
- "같이 작업하자"
- "내가 조정할 테니까 구조만 만들어줘"

Then activate collaboration mode:
1. Claude creates structure only
2. Wait for user's Qt Designer changes
3. Detect .ui file modification
4. Read user's changes
5. Apply to next iteration
6. Don't overwrite user's manual adjustments
```

### 협업 시 주의사항

**Claude가 하지 말아야 할 것:**
- ❌ 사용자가 수동 조정한 geometry 덮어쓰기
- ❌ 사용자가 추가한 위젯 삭제
- ❌ 사용자의 styleSheet 변경 무시

**Claude가 해야 할 것:**
- ✅ 사용자 변경 사항 읽기 및 학습
- ✅ 사용자 스타일 유지하며 새 위젯 추가
- ✅ 변경 알림 (예: "User adjusted button position, respecting change")

### 협업의 장점

**속도:**
- Claude: 반복 작업 빠름 (4개 카드 생성 1초)
- 사용자: 시각적 조정 빠름 (드래그 1초)
- **합계: 10배 빠른 UI 제작**

**품질:**
- Claude: 일관성 있는 구조
- 사용자: 미적 감각으로 세밀한 조정
- **합계: 구조 + 디자인 완벽**

**학습:**
- Claude: 사용자 패턴 학습
- 사용자: .ui 구조 이해
- **합계: 점점 더 나은 협업**

---

## ⚙️ 자동화 규칙

### 1. 질문 금지 원칙
- 서브에이전트는 사용자에게 질문하지 않음
- 자율적으로 판단하고 작업 진행
- 불확실한 경우 레퍼런스 이미지 기준으로 결정

### 2. 병렬 실행
- 여러 서브에이전트 팀 동시 작업
- Task Tool을 단일 메시지로 여러 개 호출
- 예: UI 구성 + 배치 + 컬러 + 아이콘 4개 팀 동시 실행

### 3. 반복 평가
- 80점 달성까지 자동 반복
- 각 반복마다 점수 향상 확인
- 무한 루프 방지: 최대 5회 제한

### 4. 명확한 피드백
- 점수와 함께 구체적인 개선 사항 제시
- 예: "UI 배치: 50점 - Stats 카드 간격이 불균등함 (10px로 통일 필요)"

---

## 📁 프로젝트 구조

```
QtLiveDevTools/
├── .claude/
│   └── skills/
│       └── qtlivedevtools/
│           ├── SKILL.md                    # Skills 정의 (재작성 필요)
│           ├── helpers/
│           │   ├── ui_helper.py           # UI 생성 헬퍼
│           │   ├── screenshot.py          # 스크린샷 도구
│           │   └── evaluator.py           # 팀장 평가 로직
│           └── examples.md                 # 예제
│
├── src/
│   ├── main.py                             # UI 실행 메인
│   ├── screenshot.py                       # 스크린샷 촬영
│   └── main_window.ui                      # 메인 UI 파일
│
├── ui_manager.py                           # UI XML 조작 라이브러리
├── mcp_server.py                           # 기존 함수 (재사용)
│
├── sample_ui_image.png                     # 레퍼런스 이미지
└── current_ui_screenshot.png               # 현재 UI 스크린샷
```

---

## 🎯 Skills 재작성 핵심 변경사항

### SKILL.md (새로운 버전)

```yaml
---
name: qtlivedevtools
description: Create Qt/PySide6 UI matching reference images using multi-agent team coordination. Automatically iterates until 80+ score achieved. Use when user provides UI reference image or requests Qt interface design.
allowed-tools: Read, Write, Edit, Bash, Task, Glob, Grep
---

# QtLiveDevTools - Reference-based UI Auto-generation

## Workflow

### 1. User Input
- Reference image: sample_ui_image.png
- Requirements: Text description

### 2. Team Leader Evaluation
- Compare reference vs current screenshot
- Score each team: 0-100 points
- Target: 80+ total score

### 3. Sub-agent Teams (Parallel)
1. UI Structure Team - Add missing widgets
2. UI Placement Team - Adjust positions [PRIORITY]
3. Layout Team - Set layouts and spacing
4. Color Team - Apply colors and styles
5. Icon Team - Add icons

### 4. Iteration
- Restart UI → Screenshot → Re-evaluate
- Repeat until 80+ score
- Max 5 iterations

## Implementation

### Team Leader (Evaluator)
```python
# helpers/evaluator.py 사용
from evaluator import evaluate_ui

scores = evaluate_ui(
    reference_image="sample_ui_image.png",
    current_screenshot="current_ui_screenshot.png"
)

# Output:
# {
#   "total": 65,
#   "ui_structure": 85,
#   "ui_placement": 50,  # FAIL
#   "layout": 70,        # FAIL
#   "color": 60,         # FAIL
#   "icon": 80
# }
```

### Sub-agent Execution
```python
# 80점 미만 팀만 실행
if scores["ui_placement"] < 80:
    Task(description="Fix UI placement", ...)

if scores["color"] < 80:
    Task(description="Fix colors", ...)
```

### Restart and Re-evaluate
```bash
pkill -f "python src/main.py"
rez-env qt6 pyside6 python-3.13 -- python src/main.py &
sleep 1
rez-env qt6 pyside6 python-3.13 -- python src/screenshot.py

# Re-evaluate
scores = evaluate_ui(...)
```
```

---

## 🚀 구현 단계

### Phase 1: 헬퍼 파일 작성 (1시간)

1. **helpers/screenshot.py** - 스크린샷 도구
2. **helpers/evaluator.py** - 팀장 평가 로직
3. **helpers/ui_helper.py** - UI 생성 헬퍼 (기존 간소화)

### Phase 2: SKILL.md 재작성 (1.5시간)

1. 서브에이전트 팀 구조 정의
2. 평가 기준 명시
3. 병렬 실행 워크플로우 작성
4. 자동 반복 로직 추가

### Phase 3: src/ 디렉토리 구성 (30분)

1. **src/main.py** - UI 실행 메인
2. **src/screenshot.py** - 스크린샷 촬영
3. 테스트 UI 파일 생성

### Phase 4: 테스트 (1시간)

1. 레퍼런스 이미지로 전체 워크플로우 테스트
2. 서브에이전트 병렬 실행 확인
3. 반복 평가 로직 검증
4. 80점 달성까지 자동 진행 확인

### Phase 5: 문서화 및 커밋 (30분)

1. README.md 업데이트
2. SKILLS_GUIDE.md 업데이트
3. Git 커밋 및 푸시

**총 예상 시간: 4.5시간**

---

## 📊 성공 기준

### 기능 요구사항
- ✅ 레퍼런스 이미지 기반 UI 생성
- ✅ 서브에이전트 팀 병렬 작업
- ✅ 자동 평가 및 반복
- ✅ 80점 이상 달성

### 성능 요구사항
- ✅ 1회 반복당 3분 이내
- ✅ 평균 3회 반복으로 80점 달성
- ✅ 총 소요 시간 10분 이내

### 품질 요구사항
- ✅ .ui 파일 Qt Designer 호환
- ✅ Git 버전 관리 가능
- ✅ Rez 환경 안정성

---

## ⚠️ 주의사항

### 제약사항
1. **Vision 모델 필요**: 스크린샷 비교를 위해 Claude의 이미지 인식 능력 활용
2. **Rez 환경**: qt6, pyside6, python-3.13 패키지 필수
3. **서브에이전트 제한**: Task Tool 사용 가능 여부 확인 필요

### 리스크
1. **무한 루프**: 최대 5회 제한으로 방지
2. **평가 정확도**: 팀장 평가 로직의 신뢰성 확보 필요
3. **병렬 실행 충돌**: 각 팀이 다른 파일 영역 수정하도록 설계

---

## 🎉 기대 효과

### 사용자 경험
- **자동화**: 레퍼런스만 제공하면 자동 완성
- **반복 불필요**: 80점 달성까지 자동 개선
- **시간 절약**: 수동 작업 대비 10배 빠름

### 개발자 경험
- **확장 가능**: 새로운 팀 추가 용이
- **디버깅 용이**: 각 팀별 점수로 문제 파악
- **재사용 가능**: .ui 파일로 다른 프로젝트에서 활용

### 팀 협업
- **일관성**: 레퍼런스 기반으로 동일한 결과
- **품질 보장**: 80점 기준으로 최소 품질 확보
- **Git 친화**: .ui 파일로 변경 이력 추적

---

## 📝 다음 단계

1. **Phase 1 시작**: helpers/ 파일 작성부터 시작
2. **점진적 구현**: 한 번에 하나씩 기능 추가 및 테스트
3. **피드백 반영**: 각 단계마다 결과 확인 및 조정

지금 바로 구현을 시작할까요?
