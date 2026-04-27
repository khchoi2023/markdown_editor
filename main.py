import html
import os
import sys
from pathlib import Path

os.environ.setdefault(
    "QTWEBENGINE_CHROMIUM_FLAGS",
    "--disable-gpu --disable-gpu-compositing --disable-accelerated-2d-canvas --use-angle=swiftshader",
)
os.environ.setdefault("QT_OPENGL", "software")
os.environ.setdefault("QT_LOGGING_RULES", "qt.webenginecontext=false")

import markdown
import pymdownx.tasklist
import pymdownx.tilde
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QKeySequence,
    QTextCharFormat,
    QTextCursor,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QTextEdit,
)
from PySide6.QtWebEngineWidgets import QWebEngineView


APP_TITLE = "Markdown Live Editor"

SAMPLE_MARKDOWN = """# Markdown Live Editor

이 문서는 샘플 Markdown 문서입니다.

## 체크리스트

- [x] Markdown 편집
- [x] 실시간 미리보기
- [x] Ctrl + F 검색
- [ ] PDF 내보내기

## 표 예시

| 기능 | 상태 |
|---|---|
| 편집 | 완료 |
| 미리보기 | 완료 |
| 검색 | 완료 |

## 코드 예시

```python
print("Hello Markdown")
```

> Markdown 문서를 작성하면 오른쪽 미리보기 화면에 바로 렌더링됩니다.

[Python 공식 사이트](https://www.python.org)
"""


LIGHT_CSS = """
body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 36px 42px;
    color: #24292f;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}
h1, h2 { border-bottom: 1px solid #d0d7de; padding-bottom: .3em; }
h1 { font-size: 2em; }
h2 { font-size: 1.5em; }
p, blockquote, ul, ol, dl, table, pre { margin-top: 0; margin-bottom: 16px; }
.task-list-item { list-style-type: none; }
.task-list-item input { margin: 0 .45em .2em -1.4em; vertical-align: middle; }
blockquote {
    padding: 0 1em;
    color: #57606a;
    border-left: .25em solid #d0d7de;
}
code {
    padding: .2em .4em;
    margin: 0;
    font-size: 85%;
    white-space: break-spaces;
    background-color: rgba(175,184,193,0.2);
    border-radius: 6px;
}
pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
}
pre code {
    padding: 0;
    background: transparent;
    border-radius: 0;
}
table {
    border-spacing: 0;
    border-collapse: collapse;
    display: block;
    width: max-content;
    max-width: 100%;
    overflow: auto;
}
td, th {
    padding: 6px 13px;
    border: 1px solid #d0d7de;
}
tr { background-color: #ffffff; border-top: 1px solid #d8dee4; }
tr:nth-child(2n) { background-color: #f6f8fa; }
img { max-width: 100%; height: auto; }
hr {
    height: .25em;
    padding: 0;
    margin: 24px 0;
    background-color: #d0d7de;
    border: 0;
}
"""

DARK_CSS = """
body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 36px 42px;
    color: #d0d7de;
    background: #0d1117;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3, h4, h5, h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}
h1, h2 { border-bottom: 1px solid #30363d; padding-bottom: .3em; }
h1 { font-size: 2em; }
h2 { font-size: 1.5em; }
p, blockquote, ul, ol, dl, table, pre { margin-top: 0; margin-bottom: 16px; }
.task-list-item { list-style-type: none; }
.task-list-item input { margin: 0 .45em .2em -1.4em; vertical-align: middle; }
blockquote {
    padding: 0 1em;
    color: #8b949e;
    border-left: .25em solid #30363d;
}
code {
    padding: .2em .4em;
    margin: 0;
    font-size: 85%;
    white-space: break-spaces;
    background-color: rgba(110,118,129,0.4);
    border-radius: 6px;
}
pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #161b22;
    border-radius: 6px;
}
pre code {
    padding: 0;
    background: transparent;
    border-radius: 0;
}
table {
    border-spacing: 0;
    border-collapse: collapse;
    display: block;
    width: max-content;
    max-width: 100%;
    overflow: auto;
}
td, th {
    padding: 6px 13px;
    border: 1px solid #30363d;
}
tr { background-color: #0d1117; border-top: 1px solid #21262d; }
tr:nth-child(2n) { background-color: #161b22; }
img { max-width: 100%; height: auto; }
hr {
    height: .25em;
    padding: 0;
    margin: 24px 0;
    background-color: #30363d;
    border: 0;
}
"""


class SearchLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.owner = parent

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() & Qt.ShiftModifier:
                self.owner.find_previous()
            else:
                self.owner.find_next()
            return
        if event.key() == Qt.Key_Escape:
            self.owner.hide_search_panel()
            return
        super().keyPressEvent(event)


class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file: Path | None = None
        self.is_modified = False
        self.is_dark_mode = False
        self.search_ranges: list[tuple[int, int]] = []
        self.current_search_index = -1

        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(300)
        self.preview_timer.timeout.connect(self.update_preview)

        self.setWindowTitle(APP_TITLE)
        self.resize(1400, 850)

        self._build_ui()
        self._build_menus()
        self._connect_signals()

        self.editor.setPlainText(SAMPLE_MARKDOWN)
        self.is_modified = False
        self.update_preview()
        self.update_window_title()
        self.update_status("샘플 문서")

    def _build_ui(self):
        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.search_panel = QWidget(self)
        self.search_panel.setVisible(False)
        self.search_panel.setFixedWidth(640)
        self.search_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        outer_search_layout = QHBoxLayout(self.search_panel)
        outer_search_layout.setContentsMargins(8, 6, 8, 6)
        outer_search_layout.setSpacing(0)

        self.search_box = QWidget(self.search_panel)
        self.search_box.setObjectName("searchBox")
        self.search_box.setFixedWidth(620)
        search_layout = QHBoxLayout(self.search_box)
        search_layout.setContentsMargins(8, 4, 8, 4)
        search_layout.setSpacing(6)

        search_layout.addWidget(QLabel("찾기:"))
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("검색어 입력")
        self.search_input.setMinimumWidth(180)
        self.search_input.setMaximumWidth(220)
        search_layout.addWidget(self.search_input)

        self.prev_button = QPushButton("이전")
        self.next_button = QPushButton("다음")
        self.prev_button.setFixedWidth(54)
        self.next_button.setFixedWidth(54)
        self.case_checkbox = QCheckBox("대소문자 구분")
        self.search_count_label = QLabel("0 / 0")
        self.search_count_label.setMinimumWidth(82)
        self.close_search_button = QToolButton()
        self.close_search_button.setText("X")
        self.close_search_button.setToolTip("검색 닫기")
        self.close_search_button.setFixedWidth(28)

        search_layout.addWidget(self.prev_button)
        search_layout.addWidget(self.next_button)
        search_layout.addWidget(self.case_checkbox)
        search_layout.addWidget(self.search_count_label)
        search_layout.addWidget(self.close_search_button)
        outer_search_layout.addWidget(self.search_box, 0, Qt.AlignLeft)
        outer_search_layout.addStretch(1)

        self.splitter = QSplitter(Qt.Horizontal, self)
        self.editor = QPlainTextEdit(self)
        self.editor.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.editor.setTabStopDistance(4 * self.editor.fontMetrics().horizontalAdvance(" "))
        editor_font = QFont("Consolas", 11)
        if not editor_font.exactMatch():
            editor_font = QFont("Courier New", 11)
        self.editor.setFont(editor_font)

        self.preview = QWebEngineView(self)
        self.preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([700, 700])

        root.addWidget(self.search_panel, 0, Qt.AlignLeft)
        root.addWidget(self.splitter)
        self.setCentralWidget(central)

        self.status = QStatusBar(self)
        self.file_label = QLabel("파일: 새 문서")
        self.modified_label = QLabel("저장됨")
        self.search_status_label = QLabel("검색: 0 / 0")
        self.mode_label = QLabel("라이트모드")
        self.status.addWidget(self.file_label, 1)
        self.status.addPermanentWidget(self.modified_label)
        self.status.addPermanentWidget(self.search_status_label)
        self.status.addPermanentWidget(self.mode_label)
        self.setStatusBar(self.status)
        self.apply_editor_theme()

    def _build_menus(self):
        file_menu = self.menuBar().addMenu("파일")
        edit_menu = self.menuBar().addMenu("편집")
        view_menu = self.menuBar().addMenu("보기")

        self.new_action = QAction("새 문서", self)
        self.new_action.setShortcut(QKeySequence.New)
        self.open_action = QAction("열기", self)
        self.open_action.setShortcut(QKeySequence.Open)
        self.save_action = QAction("저장", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_as_action = QAction("다른 이름으로 저장", self)
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.export_html_action = QAction("HTML 내보내기", self)
        self.exit_action = QAction("종료", self)
        self.exit_action.setShortcut(QKeySequence.Quit)

        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_html_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        self.find_action = QAction("찾기", self)
        self.find_action.setShortcut(QKeySequence.Find)
        self.select_all_action = QAction("모두 선택", self)
        self.select_all_action.setShortcut(QKeySequence.SelectAll)
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.select_all_action)

        self.refresh_preview_action = QAction("미리보기 새로고침", self)
        self.refresh_preview_action.setShortcut(QKeySequence.Refresh)
        self.toggle_dark_action = QAction("다크모드 전환", self)
        self.toggle_dark_action.setCheckable(True)
        view_menu.addAction(self.refresh_preview_action)
        view_menu.addAction(self.toggle_dark_action)

    def _connect_signals(self):
        self.editor.textChanged.connect(self.on_text_changed)
        self.search_input.textChanged.connect(self.recalculate_search)
        self.case_checkbox.stateChanged.connect(self.recalculate_search)
        self.next_button.clicked.connect(self.find_next)
        self.prev_button.clicked.connect(self.find_previous)
        self.close_search_button.clicked.connect(self.hide_search_panel)

        self.new_action.triggered.connect(self.new_document)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_file_as)
        self.export_html_action.triggered.connect(self.export_html)
        self.exit_action.triggered.connect(self.close)
        self.find_action.triggered.connect(self.show_search_panel)
        self.select_all_action.triggered.connect(self.editor.selectAll)
        self.refresh_preview_action.triggered.connect(self.update_preview)
        self.toggle_dark_action.triggered.connect(self.toggle_dark_mode)

    def on_text_changed(self):
        if not self.is_modified:
            self.is_modified = True
            self.update_window_title()
            self.update_status()
        self.preview_timer.start()
        if self.search_panel.isVisible():
            self.recalculate_search()

    def markdown_to_html(self) -> str:
        return markdown.markdown(
            self.editor.toPlainText(),
            extensions=[
                "extra",
                "sane_lists",
                "nl2br",
                "pymdownx.tilde",
                "pymdownx.tasklist",
            ],
            extension_configs={
                "pymdownx.tasklist": {
                    "custom_checkbox": True,
                    "clickable_checkbox": False,
                }
            },
            output_format="html5",
        )

    def full_html(self) -> str:
        css = DARK_CSS if self.is_dark_mode else LIGHT_CSS
        body = self.markdown_to_html()
        return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""

    def update_preview(self):
        base_url = self.current_file.parent.as_uri() + "/" if self.current_file else Path.cwd().as_uri() + "/"
        self.preview.setHtml(self.full_html(), base_url)

    def apply_editor_theme(self):
        if self.is_dark_mode:
            self.editor.setStyleSheet(
                "QPlainTextEdit { background: #0d1117; color: #d0d7de; "
                "selection-background-color: #264f78; border: 0; padding: 8px; }"
            )
            self.search_panel.setStyleSheet(
                "QWidget { color: #d0d7de; } "
                "QWidget#searchBox { background: #161b22; border: 1px solid #30363d; } "
                "QLineEdit { background: #0d1117; color: #d0d7de; border: 1px solid #30363d; padding: 4px; } "
                "QPushButton, QToolButton { background: #21262d; color: #d0d7de; border: 1px solid #30363d; padding: 4px 10px; }"
            )
            self.mode_label.setText("다크모드")
        else:
            self.editor.setStyleSheet(
                "QPlainTextEdit { background: #ffffff; color: #24292f; "
                "selection-background-color: #add6ff; border: 0; padding: 8px; }"
            )
            self.search_panel.setStyleSheet("")
            self.mode_label.setText("라이트모드")

    def update_window_title(self):
        name = self.current_file.name if self.current_file else "새 문서"
        marker = "*" if self.is_modified else ""
        self.setWindowTitle(f"{marker}{name} - {APP_TITLE}")

    def update_status(self, message: str | None = None):
        path = str(self.current_file) if self.current_file else "새 문서"
        self.file_label.setText(f"파일: {path}")
        self.modified_label.setText("수정됨" if self.is_modified else "저장됨")
        if message:
            self.status.showMessage(message, 3000)

    def maybe_save_changes(self) -> bool:
        if not self.is_modified:
            return True
        answer = QMessageBox.question(
            self,
            "저장되지 않은 변경사항",
            "변경사항을 저장하시겠습니까?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save,
        )
        if answer == QMessageBox.StandardButton.Save:
            return self.save_file()
        if answer == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def new_document(self):
        if not self.maybe_save_changes():
            return
        self.current_file = None
        self.editor.setPlainText(SAMPLE_MARKDOWN)
        self.is_modified = False
        self.clear_search()
        self.update_preview()
        self.update_window_title()
        self.update_status("새 문서")

    def open_file(self):
        if not self.maybe_save_changes():
            return
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Markdown 파일 열기",
            "",
            "Markdown Files (*.md *.markdown *.txt);;All Files (*.*)",
        )
        if not filename:
            return
        path = Path(filename)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="cp949")
        except OSError as exc:
            QMessageBox.critical(self, "열기 실패", f"파일을 열 수 없습니다.\n\n{exc}")
            return
        self.current_file = path
        self.editor.setPlainText(text)
        self.is_modified = False
        self.clear_search()
        self.update_preview()
        self.update_window_title()
        self.update_status("파일을 열었습니다.")

    def save_file(self) -> bool:
        if self.current_file is None:
            return self.save_file_as()
        try:
            self.current_file.write_text(self.editor.toPlainText(), encoding="utf-8")
        except OSError as exc:
            QMessageBox.critical(self, "저장 실패", f"파일을 저장할 수 없습니다.\n\n{exc}")
            return False
        self.is_modified = False
        self.update_window_title()
        self.update_status("저장 완료")
        return True

    def save_file_as(self) -> bool:
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "다른 이름으로 저장",
            str(self.current_file) if self.current_file else "untitled.md",
            "Markdown Files (*.md);;All Files (*.*)",
        )
        if not filename:
            return False
        path = Path(filename)
        if path.suffix == "":
            path = path.with_suffix(".md")
        self.current_file = path
        return self.save_file()

    def export_html(self):
        default_name = "export.html"
        if self.current_file:
            default_name = self.current_file.with_suffix(".html").name
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "HTML 내보내기",
            default_name,
            "HTML Files (*.html *.htm);;All Files (*.*)",
        )
        if not filename:
            return
        path = Path(filename)
        if path.suffix == "":
            path = path.with_suffix(".html")
        try:
            path.write_text(self.full_html(), encoding="utf-8")
        except OSError as exc:
            QMessageBox.critical(self, "내보내기 실패", f"HTML 파일을 저장할 수 없습니다.\n\n{exc}")
            return
        self.update_status(f"HTML 저장 완료: {path}")

    def show_search_panel(self):
        self.search_panel.setVisible(True)
        selected = self.editor.textCursor().selectedText()
        if selected and "\u2029" not in selected:
            self.search_input.setText(selected)
        self.search_input.setFocus()
        self.search_input.selectAll()
        self.recalculate_search()

    def hide_search_panel(self):
        self.search_panel.setVisible(False)
        self.clear_search()
        self.editor.setFocus()

    def clear_search(self):
        self.search_ranges = []
        self.current_search_index = -1
        self.editor.setExtraSelections([])
        self.search_count_label.setText("0 / 0")
        self.search_status_label.setText("검색: 0 / 0")

    def recalculate_search(self):
        term = self.search_input.text()
        if not term:
            self.clear_search()
            return

        text = self.editor.toPlainText()
        haystack = text if self.case_checkbox.isChecked() else text.lower()
        needle = term if self.case_checkbox.isChecked() else term.lower()

        self.search_ranges = []
        start = 0
        while True:
            index = haystack.find(needle, start)
            if index == -1:
                break
            self.search_ranges.append((index, index + len(term)))
            start = index + max(1, len(term))

        if not self.search_ranges:
            self.current_search_index = -1
            self.apply_search_highlights()
            self.search_count_label.setText("검색 결과 없음")
            self.search_status_label.setText("검색: 검색 결과 없음")
            return

        cursor_pos = self.editor.textCursor().position()
        self.current_search_index = 0
        for i, (start_pos, end_pos) in enumerate(self.search_ranges):
            if start_pos <= cursor_pos <= end_pos or start_pos >= cursor_pos:
                self.current_search_index = i
                break
        self.apply_search_highlights()
        self.update_search_labels()

    def apply_search_highlights(self):
        selections = []

        all_format = QTextCharFormat()
        all_format.setBackground(QColor("#fff2a8" if not self.is_dark_mode else "#5f4b00"))

        current_format = QTextCharFormat()
        current_format.setBackground(QColor("#ff9f43" if not self.is_dark_mode else "#d29922"))
        current_format.setForeground(QColor("#000000"))

        for i, (start, end) in enumerate(self.search_ranges):
            cursor = self.editor.textCursor()
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.format = current_format if i == self.current_search_index else all_format
            selections.append(selection)

        self.editor.setExtraSelections(selections)

    def update_search_labels(self):
        total = len(self.search_ranges)
        if total == 0:
            label = "검색 결과 없음" if self.search_input.text() else "0 / 0"
        else:
            label = f"{self.current_search_index + 1} / {total}"
        self.search_count_label.setText(label)
        self.search_status_label.setText(f"검색: {label}")

    def move_to_search_result(self):
        if not self.search_ranges or self.current_search_index < 0:
            self.update_search_labels()
            return
        start, end = self.search_ranges[self.current_search_index]
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()
        self.apply_search_highlights()
        self.update_search_labels()

    def find_next(self):
        if not self.search_ranges:
            self.update_search_labels()
            return
        self.current_search_index = (self.current_search_index + 1) % len(self.search_ranges)
        self.move_to_search_result()

    def find_previous(self):
        if not self.search_ranges:
            self.update_search_labels()
            return
        self.current_search_index = (self.current_search_index - 1) % len(self.search_ranges)
        self.move_to_search_result()

    def toggle_dark_mode(self):
        self.is_dark_mode = self.toggle_dark_action.isChecked()
        self.apply_editor_theme()
        self.apply_search_highlights()
        self.update_preview()
        mode = "다크모드" if self.is_dark_mode else "라이트모드"
        self.update_status(f"{mode}로 전환했습니다.")

    def closeEvent(self, event):
        if self.maybe_save_changes():
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and self.search_panel.isVisible():
            self.hide_search_panel()
            return
        super().keyPressEvent(event)


def main():
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL, True)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    window = MarkdownEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
