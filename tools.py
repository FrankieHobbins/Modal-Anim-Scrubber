import bpy


class Tools(bpy.types.Operator):
    bl_idname = "animscrubber.tools"
    bl_label = "small tools"
    bl_options = {'REGISTER', 'UNDO'}

    def find_opposite_bone(self, selbone):
        centrebone = False
        if selbone.name[-1:] == "L":
            oppobone = selbone.name[:-1] + "R"
        elif selbone.name[-1:] == "R":
            oppobone = selbone.name[:-1] + "L"
        elif ".L" in selbone.name:
            oppobone = str(selbone.name).replace(".L", ".R")
        elif ".R" in selbone.name:
            oppobone = str(selbone.name).replace(".R", ".L")
        elif "L." in selbone.name:
            oppobone = str(selbone.name).replace("L.", "R.")
        elif "R." in selbone.name:
            oppobone = str(selbone.name).replace("R.", "L.")
        elif "_R_" in selbone.name:
            oppobone = str(selbone.name).replace("_R_", "_L_")
        elif "_L_" in selbone.name:
            oppobone = str(selbone.name).replace("_L_", "_R_")
        elif "_R" in selbone.name:
            oppobone = str(selbone.name).replace("_R", "_L")
        elif "_L" in selbone.name:
            oppobone = str(selbone.name).replace("_L", "_R")
        else:
            oppobone = selbone.name
            centrebone = True

        print("selected bone", selbone.name)
        print("opposite bone", oppobone)
        return [oppobone, centrebone]

    def recalculate_bone_paths(self):
        lastframe = bpy.context.scene.frame_end
        if bpy.context.selected_pose_bones:
            bpy.ops.pose.paths_clear()
            bpy.ops.pose.paths_calculate(start_frame=0, end_frame=lastframe, bake_location='HEADS')

        return