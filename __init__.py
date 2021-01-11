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

# When main is already in local, we know this is not the initial import...
if "main" in locals():    
    importlib.reload(main)
    importlib.reload(utils)
    importlib.reload(tools)
    
    
from . import main
from . import utils
from . import tools

classes =   (
    main.AnimScrubber,
    utils.GenericOperators,
    tools.Tools,
    )
        
# store keymaps here to access after registration
addon_fkeymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)
    kmi = km.keymap_items.new('animscrubber.main', 'LEFTMOUSE', 'PRESS', alt=True)  
    addon_fkeymaps.append(km)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_fkeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del addon_fkeymaps[:]
        
if __name__ == "__main__":
    register()