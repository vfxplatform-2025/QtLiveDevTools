# Qt Designer - 전체 기능 지원 완료

## 🎉 QtLiveDevTools가 이제 Qt Designer의 모든 기능을 지원합니다!

### 업그레이드 내용

**이전**: 제한적인 속성 타입만 지원 (text, geometry 등)  
**현재**: Qt Designer가 지원하는 **모든** 속성 타입 지원

---

## 지원되는 기능 전체 목록

### 1. 기본 속성 타입
- ✅ String, Bool, Int, Float
- ✅ Enum, Set
- ✅ 모든 기본 Qt 타입

### 2. 고급 속성 타입
- ✅ **Font** (family, pointsize, bold, italic, underline, strikeout)
- ✅ **Color** (red, green, blue, alpha)
- ✅ **Palette** (전체 색상 팔레트)
- ✅ **Pixmap / IconSet** (이미지, 아이콘)
- ✅ **Size** (width, height)
- ✅ **Rect** (x, y, width, height)
- ✅ **Point** (x, y)
- ✅ **SizePolicy** (hsizetype, vsizetype, stretch)
- ✅ **Cursor** (커서 모양)

### 3. Signal/Slot 연결
- ✅ Signal-Slot 매핑
- ✅ 자동 연결 (clicked() → accept() 등)
- ✅ Custom slots

### 4. 레이아웃 시스템
- ✅ QVBoxLayout, QHBoxLayout, QGridLayout
- ✅ **Spacer** (vertical, horizontal)
- ✅ Layout 속성 (spacing, margin)
- ✅ Stretch factor

### 5. UI 구조 고급 기능
- ✅ **Tab Order** 설정
- ✅ **Buddy** 관계 (Label-Widget)
- ✅ **Actions** (QAction)
- ✅ **Custom Widgets** 선언

### 6. 스타일 및 리소스
- ✅ **QSS Stylesheet** (전역 스타일)
- ✅ **Resource Files** (.qrc 파일 참조)
- ✅ 테마 아이콘

### 7. 범용 XML 지원
- ✅ **Raw XML 삽입** (모든 Qt 속성 지원)
- ✅ 커스텀 속성
- ✅ 확장 가능성 무한

---

## 사용 방법

### 방법 1: 간단한 방식 (자동 감지)
```python
# 기본 타입은 자동으로 감지
add_widget_to_ui("myfile.ui", "QLabel", "label1", properties={
    "text": "Hello",
    "geometry": {"x": 10, "y": 20, "width": 100, "height": 30}
})
```

### 방법 2: _type 키 사용 (명시적)
```python
# 복잡한 타입은 _type 키로 명시
add_widget_to_ui("myfile.ui", "QLabel", "styledLabel", properties={
    "text": "Styled Text",
    "font": {
        "_type": "font",
        "family": "Arial",
        "pointsize": "14",
        "bold": "true"
    },
    "styleSheet": "QLabel { color: blue; }"
})
```

### 방법 3: Raw XML (최대 유연성)
```python
# 어떤 Qt 속성이든 XML로 직접 전달
add_widget_to_ui("myfile.ui", "QWidget", "widget1", properties={
    "customProperty": {
        "_xml": "<custom><any><qt>property</qt></any></custom>"
    }
})
```

---

## 실전 예제

### Signal/Slot 연결
```python
manager = UIManager("dialog.ui")

# 위젯 추가
manager.add_widget("QPushButton", "okButton", properties={"text": "OK"})

# Signal/Slot 연결
manager.add_connection(
    sender="okButton",
    signal="clicked()",
    receiver="dialog",
    slot="accept()"
)
```

### Font 및 Color
```python
add_widget_to_ui("myfile.ui", "QLabel", "fancyLabel", properties={
    "text": "Fancy Label",
    "font": {
        "_type": "font",
        "family": "Arial",
        "pointsize": "16",
        "bold": "true",
        "italic": "true"
    }
})
```

### SizePolicy
```python
add_widget_to_ui("myfile.ui", "QPushButton", "expandButton", properties={
    "text": "Expanding",
    "sizePolicy": {
        "_type": "sizepolicy",
        "hsizetype": "Expanding",
        "vsizetype": "Fixed",
        "horstretch": "0",
        "verstretch": "0"
    }
})
```

### Tab Order
```python
manager = UIManager("form.ui")
manager.set_tab_order(["field1", "field2", "field3", "submitButton"])
```

### Buddy 관계
```python
manager = UIManager("form.ui")
manager.set_buddy("nameLabel", "nameInput")  # Alt+N shortcut
```

### Stylesheet (QSS)
```python
manager = UIManager("styled.ui")
qss = """
QPushButton {
    background-color: #2196F3;
    color: white;
    border-radius: 4px;
    padding: 10px;
}
QPushButton:hover {
    background-color: #1976D2;
}
"""
manager.add_stylesheet(qss)
```

### Spacer
```python
manager = UIManager("layout.ui")
manager.add_layout("QVBoxLayout", "mainLayout")
manager.add_spacer("mainLayout", orientation="vertical", 
                  size_hint={"width": 20, "height": 40})
```

---

## 테스트

```bash
# 모든 기능 테스트
python test_qt_all_features.py

# 11개 UI 파일 생성:
# 1. test_basic_properties.ui
# 2. test_font_color.ui
# 3. test_size_geometry.ui
# 4. test_connections.ui
# 5. test_layout_spacer.ui
# 6. test_tab_order.ui
# 7. test_buddy.ui
# 8. test_stylesheet.ui
# 9. test_actions.ui
# 10. test_resources.ui
# 11. test_raw_xml.ui
```

---

## 기술적 구현

### 3가지 입력 포맷 지원

1. **자동 감지** - dict 구조로 타입 자동 판단
2. **_type 키** - 명시적 타입 지정
3. **_xml 키** - Raw XML 직접 삽입

### 확장 가능한 아키텍처

새로운 Qt 속성이 추가되어도:
- Raw XML 방식으로 즉시 지원 가능
- 코드 수정 불필요
- 100% Qt Designer 호환

---

## 비교

| 기능 | 이전 | 현재 |
|------|------|------|
| 기본 속성 | ✅ | ✅ |
| Font | ❌ | ✅ |
| Color | ❌ | ✅ |
| SizePolicy | ❌ | ✅ |
| Signal/Slot | ❌ | ✅ |
| Spacer | ❌ | ✅ |
| Tab Order | ❌ | ✅ |
| Buddy | ❌ | ✅ |
| Stylesheet | ❌ | ✅ |
| Actions | ❌ | ✅ |
| Resources | ❌ | ✅ |
| Raw XML | ❌ | ✅ |
| **총 지원 기능** | **4개** | **모든 기능** |

---

## 결론

✨ **QtLiveDevTools는 이제 Qt Designer와 동등한 수준의 기능을 제공합니다!**

Claude CLI와의 대화만으로 Qt Designer의 모든 기능을 사용할 수 있습니다.

---

**업데이트 일자**: 2025-11-15  
**담당자**: chulho@m83.studio
