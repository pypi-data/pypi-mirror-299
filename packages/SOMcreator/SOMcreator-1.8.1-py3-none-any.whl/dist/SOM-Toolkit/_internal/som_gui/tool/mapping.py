from __future__ import annotations
from typing import TYPE_CHECKING
import som_gui.core.tool
import som_gui
from som_gui.module.mapping import ui, trigger
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6.QtCore import Qt
import SOMcreator

if TYPE_CHECKING:
    from som_gui.module.mapping.prop import MappingProperties
from som_gui.module.project.constants import CLASS_REFERENCE


class Mapping(som_gui.core.tool.Mapping):
    @classmethod
    def get_properties(cls) -> MappingProperties:
        return som_gui.MappingProperties

    @classmethod
    def get_window(cls):
        prop = cls.get_properties()
        if prop.window is None:
            prop.window = ui.MappingWindow()
            prop.object_tree = prop.window.widget.object_tree
            prop.pset_tree = prop.window.widget.pset_tree
        return prop.window

    @classmethod
    def connect_window_triggers(cls, window: ui.MappingWindow) -> None:
        window.widget.action_ifc.triggered.connect(trigger.export_revit_ifc_mapping)
        window.widget.action_shared_parameters.triggered.connect(trigger.export_revit_shared_parameters)
        window.widget.object_tree.itemSelectionChanged.connect(trigger.update_pset_tree)
        cls.get_object_tree().itemChanged.connect(trigger.tree_item_changed)
        cls.get_pset_tree().itemChanged.connect(trigger.tree_item_changed)

    @classmethod
    def get_object_tree(cls) -> ui.ObjectTreeWidget:
        return cls.get_properties().object_tree

    @classmethod
    def get_pset_tree(cls) -> ui.PropertySetTreeWidget:
        return cls.get_properties().pset_tree

    @classmethod
    def get_selected_object(cls) -> SOMcreator.Object | None:
        tree = cls.get_object_tree()
        selected_items = tree.selectedItems()
        if not selected_items:
            return None
        return selected_items[0].data(0, CLASS_REFERENCE)

    @classmethod
    def fill_object_tree(cls, root_objects: list[SOMcreator.Object]) -> None:
        tree = cls.get_object_tree()
        cls.update_tree(set(root_objects), tree.invisibleRootItem(), tree)

    @classmethod
    def update_tree(cls, entities: set[SOMcreator.Attribute | SOMcreator.Object], parent_item: QTreeWidgetItem,
                    tree: ui.ObjectTreeWidget):

        existing_entities_dict = {parent_item.child(index).data(0, CLASS_REFERENCE): index for index in
                                  range(parent_item.childCount())}

        old_entities = set(existing_entities_dict.keys())
        new_entities = entities.difference(old_entities)
        delete_entities = old_entities.difference(entities)

        for entity in reversed(sorted(delete_entities, key=lambda o: existing_entities_dict[o])):
            row_index = existing_entities_dict[entity]
            parent_item.removeChild(parent_item.child(row_index))

        for new_entity in sorted(new_entities, key=lambda x: x.name):
            child = cls.create_child(new_entity)
            parent_item.addChild(child)

        for child_row in range(parent_item.childCount()):
            class_item = parent_item.child(child_row)
            entity = cls.get_entity_from_item(class_item)
            if not (parent_item.isExpanded() or parent_item == tree.invisibleRootItem()):
                continue
            if isinstance(entity, SOMcreator.Object):
                cls.update_tree(set(entity.get_all_children()), class_item, tree)
            if isinstance(entity, SOMcreator.PropertySet):
                cls.update_tree(set(entity.attributes), class_item, tree)

    @classmethod
    def create_child(cls, entity: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute) -> QTreeWidgetItem:
        entity_item = QTreeWidgetItem()
        entity_item.setData(0, CLASS_REFERENCE, entity)
        entity_item.setText(0, entity.name)
        cs = Qt.CheckState.Checked if cls.get_checkstate(entity) else Qt.CheckState.Unchecked
        entity_item.setCheckState(0, cs)
        if isinstance(entity, SOMcreator.Object):
            mapping_text = "; ".join(entity.ifc_mapping)

        elif isinstance(entity, SOMcreator.PropertySet):
            mapping_text = ""
        else:
            disable_state = not cls.get_checkstate(entity.property_set)
            entity_item.setDisabled(disable_state)
            mapping_text = entity.revit_name
        entity_item.setText(1, mapping_text)
        return entity_item

    @classmethod
    def get_checkstate(cls, entity: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute):
        if entity not in cls.get_properties().check_state_dict:
            cls.set_checkstate(entity, True)
        return cls.get_properties().check_state_dict[entity]

    @classmethod
    def set_checkstate(cls, entity: SOMcreator.Object | SOMcreator.PropertySet | SOMcreator.Attribute,
                       checkstate: bool) -> None:
        cls.get_properties().check_state_dict[entity] = checkstate

    @classmethod
    def get_entity_from_item(cls, item: QTreeWidgetItem):
        return item.data(0, CLASS_REFERENCE)

    @classmethod
    def disable_all_child_entities(cls, item: QTreeWidgetItem, disabled: bool):
        for child_index in range(item.childCount()):
            child_item = item.child(child_index)
            child_item.setDisabled(disabled)
            if child_item.checkState(0) == Qt.CheckState.Unchecked:
                continue
            cls.disable_all_child_entities(child_item, disabled)

    @classmethod
    def create_export_dict(cls, root_objects: list[SOMcreator.Object]) -> dict:
        def _loop_objects(o: SOMcreator.Object):
            cs = cls.get_checkstate(o)
            if not cs:
                return
            cls.add_object_to_ifc_export_data(o)
            for child in o.children:
                _loop_objects(child)

        cls.reset_export_dict()
        for obj in root_objects:
            _loop_objects(obj)
        return cls.get_ifc_export_dict()

    @classmethod
    def add_object_to_ifc_export_data(cls, obj: SOMcreator.Object) -> None:
        export_dict = cls.get_properties().ifc_export_dict
        for property_set in obj.get_all_property_sets():
            if not cls.get_checkstate(property_set):
                continue
            for attribute in property_set.get_all_attributes():
                if not cls.get_checkstate(attribute):
                    continue
                if property_set.name not in export_dict:
                    export_dict[property_set.name] = (list(), set())
                property_set_list = export_dict[property_set.name]
                if attribute.name not in set(a.name for a in property_set_list[0]):
                    property_set_list[0].append(attribute)
                property_set_list[1].update(obj.ifc_mapping)
        cls.get_properties().ifc_export_dict = export_dict

    @classmethod
    def get_ifc_export_dict(cls):
        return cls.get_properties().ifc_export_dict

    @classmethod
    def reset_export_dict(cls):
        cls.get_properties().ifc_export_dict = dict()
