from . import ui, prop, trigger, window
import som_gui

def register():
    som_gui.ProjectFilterProperties = prop.ProjectFilterProperties


def load_ui_triggers():
    trigger.connect()


def on_new_project():
    trigger.on_new_project()
