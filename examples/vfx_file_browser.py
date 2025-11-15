#!/usr/bin/env python3
"""
VFX File Browser Example
Demonstrates creating a practical VFX tool UI using QtLiveDevTools
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server import (
    create_ui_file,
    add_widget_to_ui,
    add_layout_to_ui,
    modify_widget_property,
    get_ui_structure
)


def create_vfx_file_browser():
    """Create a VFX-style file browser UI."""
    ui_file = "vfx_file_browser.ui"

    print("Creating VFX File Browser UI...")
    print("=" * 60)

    # Step 1: Create main window
    print("\n[1] Creating MainWindow (800x600)...")
    result = create_ui_file(ui_file, template="mainwindow", width=800, height=600)
    print(f"    {result.get('message')}")

    # Step 2: Add toolbar area
    print("\n[2] Adding toolbar widgets...")

    # Path label and input
    add_widget_to_ui(ui_file, "QLabel", "pathLabel", properties={
        "text": "경로:",
        "geometry": {"x": 10, "y": 10, "width": 50, "height": 25}
    })

    add_widget_to_ui(ui_file, "QLineEdit", "pathInput", properties={
        "text": "/home/m83/chulho",
        "geometry": {"x": 70, "y": 10, "width": 550, "height": 25}
    })

    add_widget_to_ui(ui_file, "QPushButton", "browseButton", properties={
        "text": "찾아보기...",
        "geometry": {"x": 630, "y": 10, "width": 80, "height": 25}
    })

    add_widget_to_ui(ui_file, "QPushButton", "refreshButton", properties={
        "text": "새로고침",
        "geometry": {"x": 720, "y": 10, "width": 70, "height": 25}
    })

    # Step 3: Add filter section
    print("\n[3] Adding filter section...")

    add_widget_to_ui(ui_file, "QLabel", "filterLabel", properties={
        "text": "필터:",
        "geometry": {"x": 10, "y": 45, "width": 50, "height": 25}
    })

    add_widget_to_ui(ui_file, "QComboBox", "filterCombo", properties={
        "geometry": {"x": 70, "y": 45, "width": 150, "height": 25}
    })

    add_widget_to_ui(ui_file, "QCheckBox", "showHiddenCheck", properties={
        "text": "숨김 파일 표시",
        "geometry": {"x": 230, "y": 45, "width": 120, "height": 25}
    })

    add_widget_to_ui(ui_file, "QCheckBox", "recursiveCheck", properties={
        "text": "하위 폴더 포함",
        "geometry": {"x": 360, "y": 45, "width": 120, "height": 25}
    })

    # Step 4: Add main content area
    print("\n[4] Adding main content area...")

    # File list
    add_widget_to_ui(ui_file, "QListWidget", "fileList", properties={
        "geometry": {"x": 10, "y": 80, "width": 380, "height": 450}
    })

    # Preview area
    add_widget_to_ui(ui_file, "QLabel", "previewLabel", properties={
        "text": "미리보기",
        "geometry": {"x": 400, "y": 80, "width": 390, "height": 30}
    })

    add_widget_to_ui(ui_file, "QLabel", "previewImage", properties={
        "text": "(이미지 미리보기 영역)",
        "geometry": {"x": 400, "y": 115, "width": 390, "height": 300}
    })

    # File info
    add_widget_to_ui(ui_file, "QTextEdit", "fileInfo", properties={
        "geometry": {"x": 400, "y": 425, "width": 390, "height": 105}
    })

    # Step 5: Add status bar
    print("\n[5] Adding status bar...")

    add_widget_to_ui(ui_file, "QLabel", "statusLabel", properties={
        "text": "준비",
        "geometry": {"x": 10, "y": 540, "width": 600, "height": 25}
    })

    add_widget_to_ui(ui_file, "QProgressBar", "progressBar", properties={
        "geometry": {"x": 620, "y": 540, "width": 170, "height": 25}
    })

    # Step 6: Add action buttons
    print("\n[6] Adding action buttons...")

    add_widget_to_ui(ui_file, "QPushButton", "openButton", properties={
        "text": "열기",
        "geometry": {"x": 500, "y": 540, "width": 90, "height": 40}
    })

    add_widget_to_ui(ui_file, "QPushButton", "importButton", properties={
        "text": "임포트",
        "geometry": {"x": 600, "y": 540, "width": 90, "height": 40}
    })

    add_widget_to_ui(ui_file, "QPushButton", "closeButton", properties={
        "text": "닫기",
        "geometry": {"x": 700, "y": 540, "width": 90, "height": 40}
    })

    # Show final structure
    print("\n[7] UI Structure Summary:")
    structure = get_ui_structure(ui_file)
    widget_tree = structure.get("widget_tree", {})

    print(f"    Window: {widget_tree.get('name')} ({widget_tree.get('type')})")
    print(f"    Total widgets: {len(widget_tree.get('children', []))}")

    # Count by type
    widget_types = {}
    for child in widget_tree.get("children", []):
        wtype = child.get("type")
        widget_types[wtype] = widget_types.get(wtype, 0) + 1

    print(f"\n    Widget breakdown:")
    for wtype, count in sorted(widget_types.items()):
        print(f"      - {wtype}: {count}")

    print(f"\n✓ VFX File Browser UI created: {ui_file}")
    print("=" * 60)

    return ui_file


def create_render_submit_ui():
    """Create a render submission UI (Maya/Houdini style)."""
    ui_file = "render_submit.ui"

    print("\n\nCreating Render Submit UI...")
    print("=" * 60)

    # Create dialog
    print("\n[1] Creating Dialog (600x700)...")
    create_ui_file(ui_file, template="dialog", width=600, height=700)

    # Header
    print("\n[2] Adding header section...")
    add_widget_to_ui(ui_file, "QLabel", "headerLabel", properties={
        "text": "렌더 제출",
        "geometry": {"x": 250, "y": 10, "width": 100, "height": 30}
    })

    # Job settings
    print("\n[3] Adding job settings...")
    y_pos = 60

    settings = [
        ("jobNameLabel", "작업 이름:", y_pos),
        ("jobNameInput", None, y_pos),
        ("sceneLabel", "씬 파일:", y_pos + 40),
        ("sceneInput", None, y_pos + 40),
        ("frameRangeLabel", "프레임 범위:", y_pos + 80),
        ("frameRangeInput", None, y_pos + 80),
        ("outputLabel", "출력 경로:", y_pos + 120),
        ("outputInput", None, y_pos + 120),
    ]

    for name, text, y in settings:
        if "Label" in name:
            add_widget_to_ui(ui_file, "QLabel", name, properties={
                "text": text,
                "geometry": {"x": 30, "y": y, "width": 100, "height": 25}
            })
        else:
            add_widget_to_ui(ui_file, "QLineEdit", name, properties={
                "geometry": {"x": 140, "y": y, "width": 430, "height": 25}
            })

    # Render settings
    print("\n[4] Adding render settings...")
    y_pos = 280

    add_widget_to_ui(ui_file, "QLabel", "renderSettingsLabel", properties={
        "text": "렌더 설정",
        "geometry": {"x": 30, "y": y_pos, "width": 200, "height": 25}
    })

    add_widget_to_ui(ui_file, "QComboBox", "rendererCombo", properties={
        "geometry": {"x": 30, "y": y_pos + 30, "width": 200, "height": 25}
    })

    add_widget_to_ui(ui_file, "QLabel", "qualityLabel", properties={
        "text": "품질:",
        "geometry": {"x": 250, "y": y_pos + 30, "width": 50, "height": 25}
    })

    add_widget_to_ui(ui_file, "QSlider", "qualitySlider", properties={
        "geometry": {"x": 310, "y": y_pos + 30, "width": 200, "height": 25}
    })

    # Options
    print("\n[5] Adding render options...")
    y_pos = 350

    options = [
        ("motionBlurCheck", "모션 블러", y_pos),
        ("dofCheck", "피사계 심도", y_pos + 30),
        ("shadowsCheck", "그림자", y_pos + 60),
        ("reflectionsCheck", "반사", y_pos + 90),
    ]

    for name, text, y in options:
        add_widget_to_ui(ui_file, "QCheckBox", name, properties={
            "text": text,
            "geometry": {"x": 30, "y": y, "width": 150, "height": 25}
        })

    # Priority and threads
    print("\n[6] Adding priority and thread settings...")
    y_pos = 500

    add_widget_to_ui(ui_file, "QLabel", "priorityLabel", properties={
        "text": "우선순위:",
        "geometry": {"x": 30, "y": y_pos, "width": 80, "height": 25}
    })

    add_widget_to_ui(ui_file, "QSpinBox", "prioritySpin", properties={
        "geometry": {"x": 120, "y": y_pos, "width": 100, "height": 25}
    })

    add_widget_to_ui(ui_file, "QLabel", "threadsLabel", properties={
        "text": "스레드 수:",
        "geometry": {"x": 250, "y": y_pos, "width": 80, "height": 25}
    })

    add_widget_to_ui(ui_file, "QSpinBox", "threadsSpin", properties={
        "geometry": {"x": 340, "y": y_pos, "width": 100, "height": 25}
    })

    # Email notification
    print("\n[7] Adding notification settings...")
    y_pos = 550

    add_widget_to_ui(ui_file, "QCheckBox", "emailCheck", properties={
        "text": "완료 시 이메일 알림",
        "geometry": {"x": 30, "y": y_pos, "width": 200, "height": 25}
    })

    add_widget_to_ui(ui_file, "QLineEdit", "emailInput", properties={
        "geometry": {"x": 30, "y": y_pos + 30, "width": 540, "height": 25}
    })

    # Action buttons
    print("\n[8] Adding action buttons...")
    y_pos = 630

    add_widget_to_ui(ui_file, "QPushButton", "submitButton", properties={
        "text": "제출",
        "geometry": {"x": 270, "y": y_pos, "width": 100, "height": 40}
    })

    add_widget_to_ui(ui_file, "QPushButton", "validateButton", properties={
        "text": "검증",
        "geometry": {"x": 380, "y": y_pos, "width": 100, "height": 40}
    })

    add_widget_to_ui(ui_file, "QPushButton", "cancelButton", properties={
        "text": "취소",
        "geometry": {"x": 490, "y": y_pos, "width": 80, "height": 40}
    })

    print(f"\n✓ Render Submit UI created: {ui_file}")
    print("=" * 60)

    return ui_file


def main():
    """Main entry point."""
    print("QtLiveDevTools - VFX Production Examples")
    print()

    # Create examples directory
    examples_dir = Path(__file__).parent
    examples_dir.mkdir(exist_ok=True)

    # Create example UIs
    file_browser = create_vfx_file_browser()
    render_submit = create_render_submit_ui()

    print("\n\n" + "=" * 60)
    print("✓ All VFX example UIs created successfully!")
    print("=" * 60)
    print(f"\nCreated files:")
    print(f"  1. {file_browser} - File browser (800x600, 23 widgets)")
    print(f"  2. {render_submit} - Render submission (600x700, 30+ widgets)")
    print(f"\nYou can:")
    print(f"  - Open in Qt Designer for manual editing")
    print(f"  - Load in Live Editor: ./start_live_editor.sh {file_browser}")
    print(f"  - Use in production pipeline")

    return 0


if __name__ == "__main__":
    sys.exit(main())
