import os
import sys
from pathlib import Path
from typing import Union

from PySide6 import QtGui, QtWidgets
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor

from __feature__ import snake_case

from snakeribbon.ribbonbar import RibbonBar
from snakeribbon.constants import Large, RibbonIcon
from snakeribbon.constants import RowWise
from snakeribbon.utils import DataFile, ThemeFile


def svg(file: os.PathLike, color: Union[str, list] = None) -> QIcon:
    if not file:
        return QIcon()

    pixmap = QPixmap(file)
    painter = QPainter(pixmap)
    painter.set_composition_mode(QPainter.CompositionMode.CompositionMode_SourceIn)

    painter.fill_rect(pixmap.rect(), QColor.from_string(color))
    painter.end()

    return QIcon(pixmap)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent

    app = QtWidgets.QApplication(sys.argv)
    app.set_font(QtGui.QFont("Times New Roman", 8))

    window = QtWidgets.QMainWindow()
    window.set_window_title("Pie-Ribbon Menu Bar")
    window.set_window_icon(QIcon(str(root / "icons/word.png")))
    centralWidget = QtWidgets.QWidget()
    window.set_central_widget(centralWidget)
    layout = QtWidgets.QVBoxLayout(centralWidget)

    # Define Ribbon instance without rendering it
    ribbon = RibbonBar()

    # Set-up internal icons and their path
    DataFile.update({
        RibbonIcon.Application: QIcon(str(root / "icons/save.png")),
        RibbonIcon.Backward: svg(root / "icons/svg/backward.svg"),
        RibbonIcon.Forward: svg(root / "icons/svg/box.svg"),
        RibbonIcon.Up: svg(root / "icons/svg/arrow-up.svg"),
        RibbonIcon.Down: svg(root / "icons/svg/arrow-down.svg"),
        RibbonIcon.More: svg(root / "icons/svg/box.svg"),
        RibbonIcon.PanelOptions: svg(root / "icons/svg/album.svg"),
        RibbonIcon.Help: svg(root / "icons/svg/info.svg"),
        RibbonIcon.Undo: svg(root / "icons/svg/undo.svg"),
        RibbonIcon.Redo: svg(root / "icons/svg/redo.svg"),
    })
    ThemeFile.update("themes/base.qss")
    ThemeFile.update("themes/default.qss")

    ribbon.set_style_sheet(ThemeFile.data())

    # Initialize Ribbon
    ribbon.init()
    window.set_menu_bar(ribbon)

    layout.add_widget(QtWidgets.QTextEdit(), 1)
    ribbon.set_application_text("App")
    ribbon.set_application_icon(DataFile(RibbonIcon.Application))

    undo_button = QtWidgets.QToolButton()
    undo_button.set_auto_raise(True)
    undo_button.set_text("Button")
    undo_button.set_icon(DataFile(RibbonIcon.Undo))
    undo_button.set_tool_tip("Undo")
    ribbon.add_quick_access_button(undo_button)

    redo_button = QtWidgets.QToolButton()
    redo_button.set_auto_raise(True)
    redo_button.set_text("Button")
    redo_button.set_icon(DataFile(RibbonIcon.Redo))
    redo_button.set_tool_tip("Redo")
    ribbon.add_quick_access_button(redo_button)

    # Home category
    home_category = ribbon.add_category("Home")
    options_category = ribbon.add_category("Options")

    clipboard_panel = home_category.add_panel("Clipboard", show_panel_option_button=True)
    clipboard_panel.panel_option_clicked.connect(lambda: print("SEX?"))
    paste_button = clipboard_panel.add_large_button(
        "Paste",
        icon=QIcon(str(root / "icons/paste.png")),
        tooltip="Paste"
    )
    paste_button.add_action(QtGui.QAction(QIcon(str(root / "icons/paste-special.png")), "Paste Special"))
    paste_button.add_action(QtGui.QAction(QIcon(str(root / "icons/paste-as-text.png")), "Paste as Text"))
    clipboard_panel.add_small_button(
        "Cut",
        icon=QIcon(str(root / "icons/close.png")),
        show_text=False,
        tooltip="Cut"
    )
    clipboard_panel.add_small_button(
        "Copy",
        icon=QIcon(str(root / "icons/close.png")),
        show_text=False,
        tooltip="Copy"
    )
    clipboard_panel.add_small_button(
        "Painter",
        icon=QIcon(str(root / "icons/close.png")),
        show_text=False,
        tooltip="Format Painter"
    )

    font_panel = home_category.add_panel("Font", show_panel_option_button=True)
    font_panel.add_small_toggle_button(
        "Bold",
        icon=QIcon(str(root / "icons/bold.png")),
        show_text=False,
        tooltip="Bold"
    )
    font_panel.add_small_toggle_button(
        "Italic",
        icon=QIcon(str(root / "icons/italic.png")),
        show_text=False,
        tooltip="Italic"
    )
    font_panel.add_small_toggle_button(
        "Underline",
        icon=QIcon(str(root / "icons/underline.png")),
        show_text=False,
        tooltip="Underline"
    )
    font_panel.add_small_toggle_button(
        "Toggle Button",
        icon=QIcon(str(root / "icons/strikethrough.png")),
        show_text=False,
        tooltip="Toggle me!"
    )
    font_panel.add_horizontal_separator()
    font_panel.add_date_time_edit(row_span=Large, col_span=Large)
    font_size_combo_box = font_panel.add_list_widget(["8", "9", "10"], fixed_height=True, mode=RowWise)
    spin_box = font_panel.add_double_spin_box(fixed_height=True, mode=RowWise)

    window.show_maximized()
    window.show()
    sys.exit(app.exec())
