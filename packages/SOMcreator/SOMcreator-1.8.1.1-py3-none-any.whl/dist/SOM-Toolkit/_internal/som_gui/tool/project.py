from __future__ import annotations
from typing import TYPE_CHECKING


import logging

import som_gui.core.tool
import SOMcreator
import SOMcreator.tools.merge_projects
import som_gui
from som_gui.module.project.prop import ProjectProperties, InfoDict
from som_gui.module.project.constants import VERSION, AUTHOR, NAME, PROJECT_PHASE
from som_gui.module.project.constants import CLASS_REFERENCE
from som_gui.module.project.ui import MergeDialog
from PySide6.QtWidgets import QFormLayout, QLineEdit, QComboBox, QWidget, QTableWidgetItem, QTableWidget
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from som_gui.module.project import ui



class Project(som_gui.core.tool.Project):
    @classmethod
    def update_plugin_dict(cls, project: SOMcreator.Project, key, value):
        if not project.plugin_dict.get(key):
            project.plugin_dict[key] = value
        elif isinstance(project.plugin_dict[key], (dict, set)):
            project.plugin_dict[key].update(value)
        elif isinstance(project.plugin_dict[key], (list, tuple)):
            project.plugin_dict[key] += value
        else:
            project.plugin_dict[key] = value

    @classmethod
    def add_plugin_save_function(cls, func: Callable):
        """
        add Function that gets called before Project is saved to JSON
        """
        cls.get_properties().plugin_save_functions.append(func)

    @classmethod
    def get_plugin_functions(cls):
        return cls.get_properties().plugin_save_functions

    @classmethod
    def delete_plugin_dict(cls):
        proj = cls.get()
        proj.plugin_dict = dict()

    @classmethod
    def get_filter_matrix(cls):
        return cls.get().get_filter_matrix()

    @classmethod
    def get_use_cases(cls):
        return cls.get().get_usecases()

    @classmethod
    def get_phases(cls):
        return cls.get().get_phases()

    @classmethod
    def get_properties(cls) -> ProjectProperties:
        return som_gui.ProjectProperties

    @classmethod
    def create_project(cls):
        logging.info("Create new Project")
        proj = SOMcreator.Project()
        prop: ProjectProperties = cls.get_properties()
        prop.active_project = proj
        som_gui.on_new_project()

    @classmethod
    def get_project_phase_list(cls):
        proj = cls.get()
        return proj.get_phases()

    @classmethod
    def load_project(cls, path: str):
        proj = SOMcreator.Project.open(path)
        proj.path = path
        return proj

    @classmethod
    def set_active_project(cls, proj: SOMcreator.Project):
        prop = cls.get_properties()
        prop.active_project = proj

    @classmethod
    def get(cls) -> SOMcreator.Project:
        return cls.get_properties().active_project

    @classmethod
    def get_all_objects(cls) -> list[SOMcreator.Object]:
        proj: SOMcreator.Project = cls.get_properties().active_project
        return list(proj.get_all_objects())

    @classmethod
    def get_root_objects(cls, filter_objects=True, proj: SOMcreator.Project = None):
        if proj is None:
            proj: SOMcreator.Project = cls.get_properties().active_project
        if proj is None:
            return []
        if filter_objects:
            return [obj for obj in proj.objects if obj.parent is None]
        else:
            return [obj for obj in proj.get_all_objects() if obj.parent is None]


    @classmethod
    def create_combobox(cls, filter_1):
        box = QComboBox()
        box.addItems([f.name for f in filter_1])
        for index, f in enumerate(filter_1):
            box.setItemData(index, f, CLASS_REFERENCE)
        return box

    @classmethod
    def fill_mapping_table(cls, table: QTableWidget,
                           filter_1: list[SOMcreator.classes.ProjectFilter],
                           filter_2: list[SOMcreator.classes.ProjectFilter]):

        table.setRowCount(len(filter_2))
        for row, f in enumerate(filter_2):
            item = QTableWidgetItem(f.name)
            item.setData(CLASS_REFERENCE, f)
            table.setItem(row, 0, item)
            table.setCellWidget(row, 1, cls.create_combobox(filter_1))

    @classmethod
    def get_mapping_from_table(cls, table: QTableWidget):
        """
        returns dict with imported filter as Key and existing filter as value
        """
        mapping_dict = dict()
        for row in range(table.rowCount()):
            f2 = table.item(row, 0).data(CLASS_REFERENCE)
            box: QComboBox = table.cellWidget(row, 1)
            f1 = box.itemData(box.currentIndex(), CLASS_REFERENCE)
            mapping_dict[f2] = f1
        return mapping_dict

    @classmethod
    def create_mapping_window(cls, filter_1: list[SOMcreator.classes.ProjectFilter],
                              filter_2: list[SOMcreator.classes.ProjectFilter]):
        dialog = MergeDialog()
        cls.fill_mapping_table(dialog.widget.tableWidget, filter_1, filter_2)
        if not dialog.exec():
            return None
        else:
            return cls.get_mapping_from_table(dialog.widget.tableWidget)

    @classmethod
    def get_phase_mapping(cls, p1: SOMcreator.Project, p2: SOMcreator.Project):
        return cls.create_mapping_window(p1.get_phases(), p2.get_phases())

    @classmethod
    def get_use_case_mapping(cls, p1: SOMcreator.Project, p2: SOMcreator.Project):
        return cls.create_mapping_window(p1.get_usecases(), p2.get_usecases())

    @classmethod
    def merge_projects(cls, project_1, project_2):
        phase_mapping = cls.get_phase_mapping(project_1, project_2)
        if phase_mapping is None:
            return
        use_case_mapping = cls.get_use_case_mapping(project_1, project_2)
        if use_case_mapping is None:
            return
        SOMcreator.tools.merge_projects.merge_projects(project_1, project_2, phase_mapping, use_case_mapping)

    @classmethod
    def set_settings_general_widget(cls, widget: ui.SettingsGeneral):
        cls.get_properties().settings_general_widget = widget

    @classmethod
    def get_settings_general_widget(cls) -> ui.SettingsGeneral:
        return cls.get_properties().settings_general_widget

    @classmethod
    def set_settings_path_widget(cls, widget: ui.SettingsPath):
        cls.get_properties().settings_path_widget = widget

    @classmethod
    def get_settings_path_widget(cls, ) -> ui.SettingsPath:
        return cls.get_properties().settings_path_widget
