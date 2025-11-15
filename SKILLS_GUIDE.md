# QtLiveDevTools Skills Guide

## Overview

QtLiveDevTools는 이제 **두 가지 방식**으로 사용할 수 있습니다:

| 방식 | 장점 | 적합한 경우 |
|------|------|------------|
| **MCP Server** | - 새로운 Tool 제공<br>- 독립적 실행<br>- 빠른 응답 | 외부 시스템 통합, 새로운 기능 추가 |
| **Skills** | - 설정 간편<br>- 기존 Tool 조합<br>- Git으로 공유 | 팀 워크플로우, 프로젝트별 설정 |

## Skills vs MCP 비교

### MCP Server 방식

**장점:**
- ✅ 전용 Tool 제공 (create_ui_file, add_widget, preview_ui 등)
- ✅ 독립 프로세스로 실행 (안정성)
- ✅ JSON-RPC 통신 (표준 프로토콜)
- ✅ 다양한 클라이언트 지원

**단점:**
- ❌ `~/.claude.json` 설정 필요
- ❌ Python 환경 일치 필요
- ❌ 디버깅 복잡

**사용 예:**
```json
{
  "mcpServers": {
    "qtlivedevtools": {
      "type": "stdio",
      "command": "/path/to/python",
      "args": ["/path/to/qtlivedevtools_mcp.py"]
    }
  }
}
```

### Skills 방식

**장점:**
- ✅ 폴더만 만들면 즉시 사용
- ✅ Git으로 팀과 공유
- ✅ 프로젝트별 커스터마이징 가능
- ✅ 디버깅 간단 (SKILL.md 수정)

**단점:**
- ❌ 기존 Tool만 사용 (Read, Write, Edit, Bash, Glob, Grep)
- ❌ 자동 트리거 (Claude가 판단)
- ❌ 복잡한 로직은 Python 코드 직접 작성 필요

**사용 예:**
```
~/.claude/skills/qtlivedevtools/
├── SKILL.md       # Skill 정의
└── examples.md    # 사용 예제
```

## Skills 설치

### 방법 1: Personal Skills (글로벌)

모든 프로젝트에서 사용 가능:

```bash
# 이미 설치됨!
ls ~/.claude/skills/qtlivedevtools/
# SKILL.md
# examples.md
```

### 방법 2: Project Skills (프로젝트별)

특정 프로젝트에서만 사용:

```bash
# 이미 설치됨!
cd /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools
ls .claude/skills/qtlivedevtools/
# SKILL.md
# examples.md
```

### 방법 3: Git으로 공유 (팀 사용)

```bash
# 팀원이 프로젝트를 clone하면 자동으로 Skill 포함
git clone https://github.com/vfxplatform-2025/QtLiveDevTools.git
cd QtLiveDevTools
# .claude/skills/qtlivedevtools/ 자동 사용 가능
```

## Skills 사용 방법

### 자동 트리거 (권장)

Claude가 자동으로 Skill을 사용:

```
You: "Create a Qt login dialog"
Claude: [qtlivedevtools Skill 자동 활성화]
        [Python 코드 실행하여 login.ui 생성]
        "Created login dialog with username and password fields."
```

### 트리거 키워드

다음 키워드를 사용하면 Skill이 활성화됩니다:
- "Create a Qt dialog/window/widget"
- "Make a PySide6 UI"
- "Build a login form with Qt"
- "Add a button/label/layout to the UI"
- "Modify .ui file"
- "Show me a preview of the UI"
- "Convert to PySide6/PySide2"

### 수동 확인 (디버깅)

Skill이 로드되었는지 확인:

```bash
# Claude CLI에서
# (현재는 /skills 명령이 없지만, 향후 추가될 예정)
```

## Skills 내부 구조

### SKILL.md

```yaml
---
name: qtlivedevtools
description: Create, modify, and preview Qt/PySide6 UI files (.ui) using natural language.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# QtLiveDevTools Skill

[상세 가이드...]
```

**핵심 필드:**
- `name`: Skill 식별자 (소문자, 하이픈만 사용)
- `description`: Claude가 언제 이 Skill을 사용할지 판단 (최대 1024자)
- `allowed-tools`: 이 Skill에서 사용 가능한 Tool 제한 (보안)

### examples.md

10가지 실제 사용 예제:
1. Simple Login Dialog
2. File Browser with Layout
3. Styled Settings Panel
4. Modify Existing UI
5. Quick Preview Workflow
6. Convert for Maya 2023
7. Add Signal/Slot Connection
8. Complex Property - Font
9. Using Bash for Simple UI
10. Reading UI Structure

## 실제 사용 예시

### 예시 1: 처음부터 UI 만들기

**대화:**
```
You: "Create a login dialog with username, password, and login button"

Claude (qtlivedevtools Skill 사용):
  1. Python 환경 확인
  2. ui_manager.py import
  3. create_ui_file("login", "dialog", 400, 250)
  4. add_widget_to_ui() 호출하여 위젯 추가
  5. 스크린샷 캡처 (optional)
  6. "Created login.ui with 3 widgets: username field, password field, login button"
```

**생성된 파일:**
```
login.ui  # Qt Designer와 호환되는 XML 파일
```

### 예시 2: UI 수정

**대화:**
```
You: "Make the login button blue and bigger"

Claude:
  1. login.ui 읽기
  2. UIManager로 loginButton 찾기
  3. styleSheet 속성 수정
  4. geometry 속성 수정
  5. 파일 저장
  6. "Updated login button: blue background, size increased to 120x45"
```

### 예시 3: 미리보기

**대화:**
```
You: "Show me what it looks like"

Claude:
  1. rez-env pyside6 -- python live_ui_editor.py 실행
  2. 포트 7010에서 UI 로드
  3. 스크린샷 캡처
  4. [이미지 표시]
```

## MCP vs Skills: 언제 무엇을 사용할까?

### MCP Server 사용 시

**적합한 경우:**
- ✅ 프로덕션 환경 (안정성 중요)
- ✅ 다양한 Tool 필요 (preview_ui, analyze_ui 등)
- ✅ 빠른 응답 필요 (독립 프로세스)
- ✅ 여러 클라이언트에서 접근 (Maya, Houdini, VSCode 등)

**예시 사용 케이스:**
- VFX 스튜디오의 파이프라인 툴
- 실시간 협업 UI 제작
- 복잡한 UI 분석 및 비교

### Skills 사용 시

**적합한 경우:**
- ✅ 빠른 프로토타이핑
- ✅ 팀 워크플로우 공유 (Git)
- ✅ 프로젝트별 커스터마이징
- ✅ 간단한 설정

**예시 사용 케이스:**
- 개인 개발자의 UI 제작
- 프로젝트별 UI 템플릿
- 팀 내부 UI 가이드라인 적용

## Skills 커스터마이징

### 프로젝트별 Skill 수정

```bash
cd /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools
nano .claude/skills/qtlivedevtools/SKILL.md
```

**수정 예시:**

1. **기본 경로 변경**:
```yaml
# SKILL.md 수정
description: Create Qt UIs in /project/ui/ directory. Use when...
```

2. **Tool 제한 강화**:
```yaml
allowed-tools: Read, Glob  # Write, Edit 제거 (읽기 전용)
```

3. **회사별 가이드 추가**:
```markdown
## Company UI Guidelines

All UIs must follow:
- Font: Arial 12pt
- Button color: #company_blue
- Window size: 800x600
```

### Personal Skills 업데이트

```bash
cd ~/.claude/skills/qtlivedevtools
nano SKILL.md

# 수정 후 바로 적용 (재시작 불필요)
```

## 팀 공유 워크플로우

### 1. Skill을 Git에 추가

```bash
cd /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools
git add .claude/skills/qtlivedevtools/
git commit -m "Add QtLiveDevTools Skill for team"
git push
```

### 2. 팀원이 사용

```bash
# 팀원 컴퓨터에서
git clone https://github.com/vfxplatform-2025/QtLiveDevTools.git
cd QtLiveDevTools
claude

# Skill 자동 사용 가능!
```

### 3. Skill 업데이트

```bash
# 팀원 컴퓨터에서
git pull
# 최신 Skill 자동 적용
```

## 디버깅

### Skill이 활성화되지 않을 때

**원인 1: description이 불명확**
```yaml
# ❌ 나쁜 예
description: A tool for UI

# ✅ 좋은 예
description: Create, modify, and preview Qt/PySide6 UI files (.ui) using natural language. Use when user asks to create Qt widgets, design dialogs, build PySide6 interfaces.
```

**원인 2: YAML 문법 오류**
```yaml
# ❌ 탭 사용 금지
description:	Create UI

# ✅ 스페이스 사용
description: Create UI
```

**원인 3: 파일 경로 오류**
```bash
# 확인
ls ~/.claude/skills/qtlivedevtools/SKILL.md
ls .claude/skills/qtlivedevtools/SKILL.md
```

### Python 환경 오류

**증상:** "ModuleNotFoundError: No module named 'PySide6'"

**해결:**
```bash
# Skill에서 Bash 사용 시 Rez 환경 지정
rez-env pyside6 -- python script.py

# 또는 절대 경로
/storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python script.py
```

## 성능 비교

| 작업 | MCP Server | Skills |
|------|------------|--------|
| UI 생성 | 0.5초 | 1-2초 |
| UI 수정 | 0.3초 | 1초 |
| 미리보기 | 1초 | 2-3초 |
| 설정 시간 | 5분 | 30초 |

**결론:**
- **속도**: MCP > Skills
- **간편성**: Skills > MCP
- **프로덕션**: MCP 권장
- **프로토타이핑**: Skills 권장

## 추천 사용 전략

### 개인 개발자
```
Personal Skills (~/.claude/skills/qtlivedevtools/)
→ 빠른 UI 제작, 프로토타이핑
```

### 팀 프로젝트
```
Project Skills (.claude/skills/qtlivedevtools/)
→ Git으로 공유, 일관된 워크플로우
```

### VFX 스튜디오
```
MCP Server + Project Skills 병행
→ MCP: 프로덕션 툴
→ Skills: 아티스트용 간편 UI 제작
```

## 참고 자료

- **MCP 설정**: `MCP_SETUP.md`
- **아키텍처**: `CLAUDE.md`
- **Qt 기능**: `QT_ALL_FEATURES_SUPPORTED.md`
- **Skills 예제**: `.claude/skills/qtlivedevtools/examples.md`

## FAQ

**Q: MCP와 Skills를 동시에 사용할 수 있나요?**
A: 네! 동시 사용 가능합니다. Claude가 상황에 맞게 선택합니다.

**Q: Skills가 MCP보다 느린 이유는?**
A: Skills는 Python 코드를 Bash Tool로 실행하므로 오버헤드가 있습니다. MCP는 전용 프로세스라 빠릅니다.

**Q: 어떤 방식을 선택해야 하나요?**
A:
- 빠른 프로토타이핑 → Skills
- 프로덕션 환경 → MCP
- 팀 공유 → Skills (Git)
- 복잡한 기능 → MCP

**Q: Skill 수정 후 재시작 필요한가요?**
A: 아니요. SKILL.md 수정 즉시 적용됩니다.

---

**🎉 QtLiveDevTools: MCP와 Skills 두 가지 방식으로 사용 가능!**
