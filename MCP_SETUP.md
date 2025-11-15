# QtLiveDevTools MCP Server Setup Guide

## MCP 서버 등록 방법

### 1. 빠른 설치 (권장)

**글로벌 설정 (모든 디렉토리에서 사용 가능)**

```bash
claude mcp add qtlivedevtools \
  /storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python \
  /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools/qtlivedevtools_mcp.py
```

이 명령은 현재 디렉토리의 프로젝트 설정에만 추가됩니다. 모든 디렉토리에서 사용하려면 아래 글로벌 설정을 따르세요.

**글로벌 설정 (수동)**

`~/.claude.json` 파일의 `mcpServers` 섹션에 직접 추가:

```json
{
  "mcpServers": {
    "qtlivedevtools": {
      "type": "stdio",
      "command": "/storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python",
      "args": [
        "/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools/qtlivedevtools_mcp.py"
      ],
      "env": {}
    }
  }
}
```

### 2. 등록 확인

```bash
claude mcp list
```

다음과 같이 표시되면 정상입니다:
```
qtlivedevtools: /storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python ... - ✓ Connected
```

### 3. 수동 테스트

MCP 서버가 제대로 작동하는지 테스트:

```bash
cd /storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools
/storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python qtlivedevtools_mcp.py
```

정상 실행되면 MCP 프로토콜로 대기 상태가 됩니다 (Ctrl+C로 종료).

## 파일 구조

- `qtlivedevtools_mcp.py` - MCP 프로토콜 서버 (실제 서버 진입점)
- `mcp_server.py` - UI 관리 함수들 (라이브러리)
- `ui_manager.py` - Qt UI 파일 관리
- `editor_client.py` - 라이브 에디터 클라이언트
- `pyside_converter.py` - PySide 코드 변환

## 트러블슈팅

### 문제: MCP 서버가 목록에 나타나지 않음

**원인**:
- 잘못된 설정 파일 경로 또는 중복 설정
- Python 모듈 방식(`-m qtlivedevtools.server`)으로 실행 시도

**해결**:
1. 중복 설정 파일 제거:
   ```bash
   rm ~/.config/claude/mcp_settings.json
   ```

2. `qtlivedevtools_mcp.py`를 직접 실행하도록 설정:
   - ❌ 잘못된 방법: `-m qtlivedevtools.server`
   - ✅ 올바른 방법: `/path/to/qtlivedevtools_mcp.py`

### 문제: 서버 연결 실패

**확인 사항**:
1. Python 가상환경에 MCP SDK가 설치되어 있는지 확인
2. 의존성 패키지 설치 확인:
   ```bash
   /storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/pip list | grep mcp
   ```

### 문제: 서로 다른 툴에서 같은 MCP가 실행되지 않음

**원인**:
- **Python 버전 환경 차이**: PyCharm, VSCode, Terminal 등 각 툴이 서로 다른 Python 환경을 사용
- Claude CLI를 실행한 환경과 MCP 서버가 요구하는 Python 버전이 불일치
- 예: Claude는 시스템 Python 3.9 사용, MCP는 가상환경 Python 3.11 필요

**해결 방법**:

1. **현재 Python 환경 확인**:
   ```bash
   # Claude가 실행되는 환경에서 확인
   which python
   python --version

   # MCP 서버 설정에 지정된 Python 확인
   /storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/python --version
   ```

2. **일관된 Python 환경 사용**:
   - MCP 서버 설정(`~/.claude.json`)의 `command`가 올바른 Python 경로를 가리키는지 확인
   - 가상환경 활성화 후 Claude CLI 실행:
     ```bash
     source /storage/.NAS5/rocky9_core/TD/mcp/mcp-servers/.venv/bin/activate
     claude
     ```

3. **Rez 환경 사용 시**:
   ```bash
   # 특정 Python 버전과 함께 실행
   rez-env python-3.11 -- claude

   # PySide6 포함 환경
   rez-env python-3.11 pyside6 -- claude
   ```

4. **툴별 설정 확인**:
   - **PyCharm**: Settings → Python Interpreter 확인
   - **VSCode**: Python: Select Interpreter 명령 실행
   - **Terminal**: `echo $PATH` 확인하여 Python 경로 우선순위 확인

**중요**: MCP 서버는 Claude CLI와 **동일한 Python 환경**에서 접근 가능한 모듈을 사용해야 합니다. 환경이 다르면 import 에러나 연결 실패가 발생할 수 있습니다.

## 환경 변수 (선택사항)

```bash
# 작업 디렉토리 설정 (선택)
export PYTHONPATH=/storage/.NAS5/rocky9_core/TD/users/chulho/tools/QtLiveDevTools

# MCP 서버 타임아웃 설정 (기본: 30초)
export MCP_TIMEOUT=60000
```

## 사용 가능한 MCP Tools

QtLiveDevTools MCP 서버는 다음 도구들을 제공합니다:

- `create_ui_file` - Qt .ui 파일 생성
- `add_widget` - 위젯 추가
- `add_layout` - 레이아웃 추가
- `modify_widget_property` - 위젯 속성 수정
- `get_ui_structure` - UI 구조 조회
- `preview_ui` - UI 미리보기
- `analyze_ui` - UI 분석
- `send_command_to_editor` - 라이브 에디터 명령 전송

## 참고 문서

- MCP 프로토콜: https://modelcontextprotocol.io/
- Claude Code 문서: https://docs.claude.com/
