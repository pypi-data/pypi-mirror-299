from __feature__ import snake_case

from enum import IntEnum

from PySide6 import QtGui


class RibbonCategoryStyle(IntEnum):
    """The button style of a category."""

    Normal = 0
    Context = 1


Normal = RibbonCategoryStyle.Normal
Context = RibbonCategoryStyle.Context


#: A list of context category colors
context_colors = [
    QtGui.QColor(201, 89, 156),  # 玫红
    QtGui.QColor(242, 203, 29),  # 黄
    QtGui.QColor(255, 157, 0),  # 橙
    QtGui.QColor(14, 81, 167),  # 蓝
    QtGui.QColor(228, 0, 69),  # 红
    QtGui.QColor(67, 148, 0),  # 绿
]


class RibbonSpaceFindMode(IntEnum):
    """Mode to find available space in a grid layout, ColumnWise or RowWise."""

    ColumnWise = 0
    RowWise = 1


ColumnWise = RibbonSpaceFindMode.ColumnWise
RowWise = RibbonSpaceFindMode.RowWise


class RibbonButtonStyle(IntEnum):
    """Button style, Small, Medium, or Large."""

    Small = 0
    Medium = 1
    Large = 2


Small = RibbonButtonStyle.Small
Medium = RibbonButtonStyle.Medium
Large = RibbonButtonStyle.Large


class RibbonIcon:
    """
    Internal icons
    """
    Application = "icons/application.svg"
    Backward = "icons/backward.svg"
    Forward = "icons/forward.svg"
    Up = "icons/up.svg"
    Down = "icons/down.svg"
    More = "icons/more.svg"
    PanelOptions = "icons/linking.svg"
    Help = "icons/help.svg"
    Undo = "icons/undo.svg"
    Redo = "icons/redo.svg"
