from __future__ import annotations
from typing import TYPE_CHECKING
from SOMcreator.datastructure.som_json import IFC_MAPPINGS, ABBREVIATION, PROPERTY_SETS, IDENT_ATTRIBUTE, OBJECTS
from SOMcreator.exporter.som_json import property_set
import SOMcreator
from SOMcreator.exporter.som_json import core

if TYPE_CHECKING:
    from SOMcreator import Project
    from SOMcreator.datastructure.som_json import ObjectDict, MainDict


### Import ###

def _load_object(proj: SOMcreator.Project, object_dict: ObjectDict, identifier: str) -> SOMcreator.Object:
    name, description, optional, parent, filter_matrix = core.get_basics(proj, object_dict, identifier)
    ifc_mapping = object_dict[IFC_MAPPINGS]
    if isinstance(ifc_mapping, list):
        ifc_mapping = set(ifc_mapping)

    abbreviation = object_dict.get(ABBREVIATION)

    obj = SOMcreator.Object(name=name, ident_attrib=None, uuid=identifier, ifc_mapping=ifc_mapping,
                         description=description, optional=optional, abbreviation=abbreviation, project=proj,
                         filter_matrix=filter_matrix)
    property_sets_dict = object_dict[PROPERTY_SETS]
    for ident, pset_dict in property_sets_dict.items():
        property_set.load(proj, pset_dict, ident, obj)
    ident_attrib_id = object_dict[IDENT_ATTRIBUTE]
    if ident_attrib_id is not None:
        ident_attrib = SOMcreator.exporter.som_json.attribute_uuid_dict[ident_attrib_id]
        obj.ident_attrib = ident_attrib
    SOMcreator.exporter.som_json.parent_dict[obj] = parent
    SOMcreator.exporter.som_json.object_uuid_dict[identifier] = obj

def load(proj: Project, main_dict: dict):
    objects_dict: dict[str, ObjectDict] = main_dict.get(OBJECTS)
    core.remove_part_of_dict(OBJECTS)

    objects_dict = dict() if core.check_dict(objects_dict, OBJECTS) else objects_dict

    for uuid_ident, entity_dict in objects_dict.items():
        _load_object(proj, entity_dict, uuid_ident)

### Export ###
def _write_object(element: SOMcreator.Object) -> ObjectDict:
    object_dict: ObjectDict = dict()
    core.write_basics(object_dict, element)

    if isinstance(element.ifc_mapping, set):
        object_dict[IFC_MAPPINGS] = list(element.ifc_mapping)
    else:
        object_dict[IFC_MAPPINGS] = list(element.ifc_mapping)

    psets_dict = dict()
    for pset in element.get_property_sets(filter=False):
        psets_dict[pset.uuid] = property_set.write_entry(pset)

    object_dict[PROPERTY_SETS] = psets_dict
    object_dict[ABBREVIATION] = element.abbreviation

    if isinstance(element.ident_attrib, SOMcreator.Attribute):
        object_dict[IDENT_ATTRIBUTE] = element.ident_attrib.uuid
    else:
        object_dict[IDENT_ATTRIBUTE] = element.ident_attrib

    return object_dict


def write(proj: Project, main_dict: MainDict):
    main_dict[OBJECTS] = dict()
    for obj in sorted(proj.get_objects(filter=False), key=lambda o: o.uuid):
        main_dict[OBJECTS][obj.uuid] = _write_object(obj)
