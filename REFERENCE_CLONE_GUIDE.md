# 📋 Reference-Based UI Cloning Guide

## 개요

참고 UI 파일을 기반으로 새 UI를 생성하고, 자동으로 비교 및 검증하는 시스템입니다.

**유즈케이스**:
- 기존 UI를 참고해서 비슷한 UI 만들기
- 디자인 가이드라인 준수 확인
- UI 변경사항 추적
- 일관성 검증

---

## 🎯 3가지 워크플로우

### 1. 완전 복제 (Clone)

기존 UI를 그대로 복사합니다.

```
You: "login_dialog.ui를 참고해서 signup_dialog.ui 만들어줘"

Claude:
1. clone_from_reference("login_dialog.ui", "signup_dialog.ui")
2. 자동 검증: 100% 일치
3. "완벽하게 복제되었습니다."
```

**Python API**:
```python
from mcp_server import clone_from_reference

result = clone_from_reference(
    reference_ui="login_dialog.ui",
    target_ui="signup_dialog.ui",
    verify=True
)

print(f"Similarity: {result['verification']['similarity_score']}")
# Output: Similarity: 1.0 (100%)
```

### 2. 참고 후 수정 (Clone + Modify)

기존 UI를 복사한 후 일부 수정합니다.

```
You: "login_dialog.ui를 기반으로 signup_dialog.ui 만들되,
      비밀번호 확인 필드 추가해줘"

Claude:
1. clone_from_reference("login_dialog.ui", "signup_dialog.ui")
2. add_widget("QLineEdit", "confirmPasswordField")
3. compare_with_reference("login_dialog.ui", "signup_dialog.ui")
4. 리포트: "85% 일치, 1개 위젯 추가됨"
```

**Python API**:
```python
from mcp_server import clone_from_reference, compare_with_reference
from ui_manager import UIManager

# 1. Clone
clone_from_reference("login_dialog.ui", "signup_dialog.ui")

# 2. Modify
manager = UIManager("signup_dialog.ui")
manager.add_widget("QLineEdit", "confirmPasswordField", properties={
    "geometry": {"x": 100, "y": 150, "width": 200, "height": 25}
})
manager.save()

# 3. Compare
result = compare_with_reference("login_dialog.ui", "signup_dialog.ui")
print(result['report'])
```

### 3. 참고하여 새로 만들기 (Reference-Guided Creation)

참고 UI를 보면서 새로 만들고, 주기적으로 비교합니다.

```
You: "settings_dialog.ui를 참고해서 비슷한 느낌의
      preferences_dialog.ui 만들어줘"

Claude:
1. analyze_ui("settings_dialog.ui") → 구조 파악
2. create_ui_file("preferences_dialog")
3. add_widget(...) → 비슷한 구조로 생성
4. compare_with_reference() → 차이 확인
5. 반복 수정으로 유사도 향상
```

---

## 📊 비교 리포트 해석

### 유사도 점수 (Similarity Score)

```
100%   - 완전히 동일
90-99% - 거의 동일 (미세한 차이)
80-89% - 유사함 (몇 가지 차이 있음)
70-79% - 부분적으로 유사
< 70%  - 다른 UI
```

### 리포트 섹션

#### ✅ Matching Widgets
```
✅ Matching Widgets (5):
   - okButton
   - cancelButton
   - titleLabel
   - usernameField
   - passwordField
```
→ 양쪽 UI에 모두 존재하는 위젯

#### ❌ Missing Widgets
```
❌ Missing Widgets (2):
   - submitButton (QPushButton)
   - helpLabel (QLabel)
```
→ 참고 UI에는 있지만 타겟 UI에는 없는 위젯

#### ➕ Extra Widgets
```
➕ Extra Widgets (1):
   - extraField (QLineEdit)
```
→ 타겟 UI에만 추가로 있는 위젯

#### ⚠️ Property Differences
```
⚠️ Property Differences (2):

   Widget: okButton
      geometry:
         x: 100 → 150 (50px 이동)
         y: 200 → 220 (20px 이동)
         width: 80 → 100 (20px 증가)

   Widget: titleLabel
      properties:
         text: "Login" → "Sign Up"
```
→ 같은 위젯이지만 속성이 다른 경우

---

## 🔄 실전 시나리오

### 시나리오 1: 스타일 가이드 준수 확인

**목표**: 새로 만든 UI가 회사 스타일 가이드를 따르는지 확인

```
You: "new_dialog.ui가 company_standard.ui의 스타일을
      잘 따르고 있는지 확인해줘"

Claude:
[compare_with_reference("company_standard.ui", "new_dialog.ui")]

Report:
📊 Similarity: 78%

⚠️ Differences:
   - primaryButton:
     - font: "Arial 12pt" → "Helvetica 14pt" (❌ 표준 위반)
     - color: blue → green (❌ 표준 위반)

   - titleLabel:
     - font: "Arial 16pt bold" (✅ 표준 준수)

추천:
"primaryButton의 폰트를 Arial 12pt로, 색상을 파란색으로 변경하세요."
```

### 시나리오 2: 반복 개선

**목표**: 참고 UI와 90% 이상 유사하게 만들기

```
Iteration 1:
You: "reference.ui를 참고해서 만들어줘"
Claude: [creates UI] → 70% similarity

Iteration 2:
You: "더 비슷하게 만들어줘"
Claude: [adds missing widgets] → 85% similarity

Iteration 3:
You: "거의 다 왔네, 마저 맞춰줘"
Claude: [fixes property differences] → 95% similarity

✓ 목표 달성!
```

### 시나리오 3: 버전 간 차이 추적

**목표**: UI 변경 사항 파악

```
You: "dialog_v1.ui와 dialog_v2.ui의 차이를 알려줘"

Claude:
[compare_with_reference("dialog_v1.ui", "dialog_v2.ui")]

Changes:
📊 Similarity: 92%

Added (v2):
  + saveButton (QPushButton)
  + statusBar (QStatusBar)

Removed (v1 → v2):
  - helpButton (QPushButton)

Modified:
  - okButton: position moved (10, 200) → (50, 200)
  - titleLabel: text "Version 1" → "Version 2"

Summary:
"버전 2에서 저장 버튼과 상태바가 추가되었고,
 도움말 버튼이 제거되었습니다."
```

---

## 💻 MCP 함수 레퍼런스

### compare_with_reference()

```python
compare_with_reference(
    reference_ui: str,
    target_ui: str,
    detailed: bool = True
) -> Dict[str, Any]
```

**파라미터**:
- `reference_ui`: 참고 UI 파일 경로
- `target_ui`: 비교할 타겟 UI 파일 경로
- `detailed`: 상세 정보 포함 여부

**반환값**:
```python
{
    "status": "success",
    "similarity_score": 0.85,  # 0.0 ~ 1.0
    "matching_widgets": ["okButton", "cancelButton"],
    "missing_widgets": ["helpButton"],
    "extra_widgets": ["extraField"],
    "property_differences": {
        "okButton": {
            "geometry": {
                "x": {"reference": 100, "target": 150}
            }
        }
    },
    "missing_specs": [
        {
            "name": "helpButton",
            "type": "QPushButton",
            "geometry": {"x": 200, "y": 50, "width": 80, "height": 30},
            "properties": {"text": "Help"}
        }
    ],
    "report": "====== UI Comparison Report ======\n..."
}
```

### clone_from_reference()

```python
clone_from_reference(
    reference_ui: str,
    target_ui: str,
    verify: bool = True
) -> Dict[str, Any]
```

**파라미터**:
- `reference_ui`: 참고 UI 파일 경로
- `target_ui`: 새로 만들 UI 파일 경로
- `verify`: 복제 후 자동 검증 여부

**반환값**:
```python
{
    "status": "success",
    "message": "Cloned reference.ui to target.ui",
    "reference_ui": "reference.ui",
    "target_ui": "target.ui",
    "verification": {
        "similarity_score": 1.0,
        "verified": True
    }
}
```

---

## 🎨 Claude CLI와의 대화 예시

### 예시 1: 간단한 복제
```
You: "login.ui를 복사해서 signup.ui 만들어줘"

Claude:
[clone_from_reference("login.ui", "signup.ui")]
✓ signup.ui가 생성되었습니다.
검증: 100% 일치
```

### 예시 2: 스타일 확인
```
You: "new_dialog.ui가 standard.ui 스타일을 따르는지 확인해줘"

Claude:
[compare_with_reference("standard.ui", "new_dialog.ui")]

📊 유사도: 82%

차이점:
- 폰트가 다릅니다 (Arial → Helvetica)
- 버튼 크기가 표준보다 작습니다 (80px → 100px 권장)
- 색상 팔레트가 일부 다릅니다

수정하시겠습니까?
```

### 예시 3: 반복 개선
```
You: "settings.ui를 참고해서 비슷하게 만들어줘"

Claude:
[creates initial UI]
현재 유사도: 65%

You: "더 비슷하게"

Claude:
[adds missing widgets]
현재 유사도: 85%

You: "완벽하게"

Claude:
[fixes all differences]
현재 유사도: 98% ✓
```

---

## 🔧 고급 활용

### 자동 스타일 적용

```python
from ui_comparator import UIComparator
from ui_manager import UIManager

# 1. 표준 UI 분석
comparator = UIComparator()
comparator.load_reference("company_standard.ui")

# 2. 표준에서 스타일 추출
ref_widgets = comparator.reference_widgets
button_style = ref_widgets['standardButton'].properties

# 3. 새 UI에 스타일 적용
manager = UIManager("new_dialog.ui")
for widget_name in manager.get_all_widgets():
    if widget_name.endswith('Button'):
        manager.apply_style(widget_name, button_style)
```

### 배치 검증

```python
# 여러 UI 파일을 표준과 비교
ui_files = ["dialog1.ui", "dialog2.ui", "dialog3.ui"]
standard = "company_standard.ui"

for ui_file in ui_files:
    result = compare_with_reference(standard, ui_file)
    print(f"{ui_file}: {result['similarity_score']:.1%}")
```

---

## 📈 유사도 계산 방식

```
Similarity = (Matching Widgets Score × 0.7) + (Property Match Score × 0.3)

Matching Widgets Score = matching_count / total_reference_widgets
Property Match Score = 1.0 - (different_properties / matching_widgets)
```

**예시**:
```
Reference: 10개 위젯
Target:
  - 8개 매칭
  - 2개 누락
  - 1개 추가
  - 3개 위젯의 속성이 다름

Matching Score = 8 / 10 = 0.8
Property Score = 1.0 - (3 / 8) = 0.625

Similarity = (0.8 × 0.7) + (0.625 × 0.3) = 0.56 + 0.1875 = 0.7475
           = 74.75%
```

---

## ✅ 체크리스트

### 복제 전:
- [ ] 참고 UI 파일이 존재하는가?
- [ ] 참고 UI가 원하는 스타일/구조를 가지고 있는가?
- [ ] 타겟 파일명이 중복되지 않는가?

### 복제 후:
- [ ] 자동 검증 결과가 100%인가?
- [ ] 필요한 수정사항을 파악했는가?
- [ ] 수정 후 재검증을 했는가?

### 비교 시:
- [ ] 유사도 점수를 확인했는가?
- [ ] 차이점 리포트를 검토했는가?
- [ ] 누락/추가 위젯을 확인했는가?
- [ ] 속성 차이를 확인했는가?

---

## 🚀 다음 단계

1. **테스트 실행**:
   ```bash
   python test_reference_clone.py
   ```

2. **실제 사용**:
   ```bash
   claude  # Claude CLI 실행

   You: "login.ui를 참고해서 signup.ui 만들어줘"
   ```

3. **문서 확인**:
   - `FINAL_SUMMARY.md` - 프로젝트 전체 요약
   - `QT_ALL_FEATURES_SUPPORTED.md` - Qt 기능 가이드
   - `REFERENCE_CLONE_GUIDE.md` - 이 문서

---

**작성일**: 2025-11-15
**버전**: 1.0
**상태**: 프로덕션 준비 완료
