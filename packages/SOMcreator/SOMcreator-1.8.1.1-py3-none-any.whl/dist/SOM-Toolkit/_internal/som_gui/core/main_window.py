from __future__ import annotations
from typing import TYPE_CHECKING, Type

from ifcopenshell.express.rules.IFC4X1 import project

import som_gui
from som_gui.core import project as core_project
from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
    from som_gui.tool import MainWindow, Appdata, Project, Popups
    from som_gui import tool


def create_main_window(application: QApplication, main_window: Type[tool.MainWindow]):
    mw = main_window.create(application)
    mw.show()
    main_window.hide_console()


def close_event(project_tool: Type[Project], appdata: Type[Appdata],
                popups_tool: Type[Popups], main_window: Type[tool.MainWindow]):
    reply = popups_tool.request_save_before_exit()
    if reply is None:  # abort Dialog
        return False
    if reply is False:  # No
        return True
    core_project.save_clicked(project_tool, popups_tool, appdata, main_window)
    return True


def create_menus(main_window_tool: Type[MainWindow], util: Type[tool.Util]):
    menu_dict = main_window_tool.get_menu_dict()
    menu_bar = main_window_tool.get_menu_bar()
    menu_dict["menu"] = menu_bar
    util.menu_bar_create_actions(menu_dict, None)


def refresh_main_window(main_window_tool: Type[MainWindow], project_tool: Type[Project]):
    proj = project_tool.get()
    name = proj.name
    version = f"Version: {proj.version}"
    phase_names = ",".join(proj.get_phase_by_index(i).name for i in proj.active_phases)
    usecase_names = ",".join(proj.get_usecase_by_index(i).name for i in proj.active_usecases)
    status = " | ".join([name, version, phase_names, usecase_names])
    main_window_tool.set_status_bar_text(status)
    main_window_tool.set_window_title(f"SOM-Toolkit v{som_gui.__version__}")


def toggle_console_clicked(main_window: Type[tool.MainWindow]):
    main_window.toggle_console()
