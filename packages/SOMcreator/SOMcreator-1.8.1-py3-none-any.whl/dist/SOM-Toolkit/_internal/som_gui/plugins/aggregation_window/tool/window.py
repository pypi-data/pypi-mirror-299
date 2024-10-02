from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import SOMcreator
import som_gui
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
import som_gui.plugins.aggregation_window.core.tool
from som_gui.plugins.aggregation_window import tool as aw_tool
from som_gui.plugins.aggregation_window.module.window import ui as ui_window
from som_gui.plugins.aggregation_window.module.window import trigger
if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.window.prop import WindowProperties
    from PySide6.QtWidgets import QMenuBar, QStatusBar
    from som_gui.module.util.prop import MenuDict


class Window(som_gui.plugins.aggregation_window.core.tool.Window):


    @classmethod
    def get_properties(cls) -> WindowProperties:
        return som_gui.WindowProperties

    @classmethod
    def create_window(cls) -> ui_window.AggregationWindow:
        window = ui_window.AggregationWindow()
        cls.get_properties().aggregation_window = window
        return window

    @classmethod
    def create_combo_box(cls) -> ui_window.ComboBox:
        cls.get_properties().combo_box = ui_window.ComboBox()
        cls.get_properties().combo_box.customContextMenuRequested.connect(cls.create_combobox_context_menu)
        return cls.get_properties().combo_box

    @classmethod
    def create_combobox_context_menu(cls, pos):
        menu = QMenu()
        action = QAction("Umbenennen")
        action.triggered.connect(cls.request_scene_rename)
        menu.addAction(action)
        menu.exec(cls.get_combo_box().mapToGlobal(pos))

    @classmethod
    def request_scene_rename(cls):
        trigger.request_scene_rename()



    @classmethod
    def add_widget_to_layout(cls, widget, *args, **kwargs) -> None:
        window = cls.get_properties().aggregation_window
        if window is None:
            return
        window.central_layout.addWidget(widget, *args, **kwargs)

    @classmethod
    def get_combo_box(cls) -> ui_window.ComboBox:
        return cls.get_properties().combo_box

    @classmethod
    def get_combo_box_texts(cls) -> list[str]:
        cb = cls.get_combo_box()
        return [cb.itemText(i) for i in range(cb.count())]

    @classmethod
    def get_combo_box_text(cls) -> str:
        return cls.get_combo_box().currentText()

    @classmethod
    def get_menu_bar(cls) -> QMenuBar:
        return cls.get_properties().aggregation_window.menuBar()

    @classmethod
    def get_menu_dict(cls) -> MenuDict:
        return cls.get_properties().menu_dict

    @classmethod
    def get_aggregation_window(cls) -> ui_window.AggregationWindow:
        return cls.get_properties().aggregation_window

    @classmethod
    def get_menu_list(cls) -> list[tuple[str, Callable]]:
        return cls.get_properties().menu_list

    @classmethod
    def set_combo_box(cls, text: str) -> None:
        combo_box = cls.get_combo_box()
        combo_box.setCurrentText(text)

    @classmethod
    def is_filter_activated(cls) -> bool:
        return cls.get_properties().filter_is_activated

    @classmethod
    def activate_filter(cls) -> None:
        cls.get_properties().filter_is_activated = True

    @classmethod
    def remove_filter(cls) -> None:
        cls.get_properties().filter_is_activated = False
        cls.set_filter_object(None)

    @classmethod
    def get_allowed_scenes(cls) -> list:
        if not cls.is_filter_activated():
            return aw_tool.View.get_all_scenes()
        return cls.get_properties().allowed_scenes

    @classmethod
    def set_allowed_scenes(cls, scene_list: list) -> None:
        cls.get_properties().allowed_scenes = scene_list

    @classmethod
    def set_filter_object(cls, obj: SOMcreator.Object | None) -> None:
        cls.get_properties().filter_object = obj

    @classmethod
    def get_status_bar(cls) -> QStatusBar:
        return cls.get_aggregation_window().statusBar()

    @classmethod
    def calculate_statusbar_text(cls) -> str:
        filter_object = cls.get_properties().filter_object
        texts = list()
        if filter_object is not None:
            texts.append(f"Filter by {filter_object.name}")
        return " | ".join(texts)
