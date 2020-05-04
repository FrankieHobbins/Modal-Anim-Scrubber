import bpy


class Tools(bpy.types.Operator):
    bl_idname = "animscrubber.tools"
    bl_label = "small tools"
    bl_options = {'REGISTER', 'UNDO'}

    def find_opposite_bone(self, selbone):
        centrebone = False
        if "_R" in selbone.name:
            oppobone = str(selbone.name).replace("_R", "_L")
        elif "_L" in selbone.name:
            oppobone = str(selbone.name).replace("_L", "_R")
        elif ".L" in selbone.name:
            oppobone = str(selbone.name).replace(".L", ".R")
        elif ".R" in selbone.name:
            oppobone = str(selbone.name).replace(".R", ".L")
        else:
            oppobone = selbone.name
            centrebone = True
        print("selected bone", selbone.name)
        print("opposite bone", oppobone)
        return [oppobone, centrebone]

    def recalculate_bone_paths(self):
        lastframe = bpy.context.scene.frame_end
        bpy.ops.pose.paths_clear()
        
        if bpy.context.selected_pose_bones:
            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=lastframe, bake_location='HEADS')                    

        return
        
        
