import bpy
from . import utils
from . import tools


class AnimScrubber(bpy.types.Operator):
    bl_idname = "animscrubber.main"
    bl_label = "Scrub or Drag Keyframe"
    bl_options = {'REGISTER', 'UNDO'}
    
    """
    def __init__(self):
        print("-------anim.scrubber start------")        
    
    def __del__(self):
        print("-------anim.scrubber end-------")
    """
    Scale: bpy.props.FloatProperty(name="Sensitivity Scale", default=1)
    ScaleBySceneLength: bpy.props.BoolProperty(name="Adjust Sensitivity With Scene Length", default=False)
    StandardSceneLength: bpy.props.FloatProperty(name="Standard Scene Length", default=100)
    LengthScale: bpy.props.FloatProperty(name="Length Scale", default=1)

    def modal(self, context, event):
        self.valued = event.mouse_x / 10
        if event.type == 'MOUSEMOVE':
            # change current frame based on mouse
            utils.GenericOperators.change_frame(self)

        elif event.type == 'Z':
            # add motion paths and set scene first/last frame to match action
            utils.GenericOperators.set_range(self)
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'X':
            # delete keyframe under current frame
            utils.GenericOperators.delete_keyframe(self)
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'A':
            # move Position Bone this if for personal project
            utils.GenericOperators.personal_move_position_bone(self)
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'MIDDLEMOUSE' and event.value == "RELEASE":
            # create or move keyframe from start of this operator
            utils.GenericOperators.shift_keyframe(self)
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'RIGHTMOUSE':
            # create or duplicate keyframe from start of this operator
            utils.GenericOperators.clone_keyframe(self)
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'W':
            # copy from start to end
            utils.GenericOperators.first_frame_to_last(self)
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'R':
            # fix looping warning will break NLA
            tools.Tools.recalculate_bone_paths(self)
            return utils.GenericOperators.fix_loop(self)

        elif event.type == 'S':
            # copy and flip animation for selected bone
            tools.Tools.recalculate_bone_paths(self)
            return utils.GenericOperators.mirror_space(self)

        elif event.type == 'E':
            # Copy and flip animation for selected bone with time offset
            tools.Tools.recalculate_bone_paths(self)
            return utils.GenericOperators.mirror_time_and_space(self)

        elif event.type == 'WHEELUPMOUSE':
            # Create or Duplicate Keyframe base on starting position
            utils.GenericOperators.throw_key_generic(self, "DOWN")
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'WHEELDOWNMOUSE':
            # Create or Duplicate Keyframe base on startiong position
            utils.GenericOperators.throw_key_generic(self, "UP")
            tools.Tools.recalculate_bone_paths(self)

        elif event.type == 'LEFTMOUSE' and event.value == "RELEASE":
            # Confirm
            bpy.ops.screen.frame_offset()
            return {'FINISHED'}

        elif event.type in ('ESC'):
            # Cancel
            bpy.ops.screen.frame_offset()
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        # print("invoke")
        self.sframe = bpy.context.scene.frame_current
        self.value = event.mouse_x
        self.dampedvalue = event.mouse_x / 10
        self.looped = 0
        # self.execute(context) #if all executes are uncommented it runs every update
        self.a = bpy.context.object.name

        # saves matrix from current/start frame
        self.d = {}
        if bpy.context.selected_pose_bones != None:
            for i in range(len(bpy.context.selected_pose_bones)):
                # matrix needs copy or it remains linked
                self.d[bpy.context.selected_pose_bones[i].name] = bpy.context.selected_pose_bones[i].matrix.copy()        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
