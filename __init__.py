bl_info = {
    "name": "Anim Scrubber With Modal",
    "description": "An anim scrubber with lots of modal tools",
    "author": "Frankie Hobbins",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "wiki_url": "my github url here",
    "tracker_url": "my github url here/issues",
    "category": "Animation"
}

import bpy
import importlib

# Reload modules if already imported (for development purposes)
if "main" in locals():
    importlib.reload(main)
    importlib.reload(utils)
    importlib.reload(tools)

from . import main
from . import utils
from . import tools

# Add-on preferences class (minimal)
class AnimScrubberPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    recalculate_curves: bpy.props.BoolProperty(
        name="Recalculate Animation Curves",
        description="Enable or disable curve recalculation",
        default=True
    )

    recalculate_curves_at_head: bpy.props.BoolProperty(
        name="Recalculate Animation Curves At Head",
        description="Curve recalculation at Head instead of Tail",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "recalculate_curves")
        layout.prop(self, "recalculate_curves_at_head")

# Classes to register/unregister
classes = (
    AnimScrubberPreferences,  # Register preferences class
    main.AnimScrubber,
    utils.GenericOperators,
    tools.Tools,
)

# Store keymaps here to access after registration
addon_fkeymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('animscrubber.main', 'LEFTMOUSE', 'PRESS', alt=True)
    addon_fkeymaps.append(km)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    # Handle the keymap
    wm = bpy.context.window_manager
    for km in addon_fkeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del addon_fkeymaps[:]

if __name__ == "__main__":
    register()
