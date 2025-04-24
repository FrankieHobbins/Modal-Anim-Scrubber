import bpy


class Tools(bpy.types.Operator):
    bl_idname = "animscrubber.tools"
    bl_label = "small tools"
    bl_options = {'REGISTER', 'UNDO'}

    def find_opposite_bone(self, selbone):
        centrebone = False
        bone_name = selbone.name
        bone_name_lower = bone_name.lower()

        # Define patterns and their replacements
        patterns = [
            (".l", ".r"),
            (".r", ".l"),
            ("_l_", "_r_"),
            ("_r_", "_l_"),
            ("_l", "_r"),
            ("_r", "_l"),
            ("l.", "r."),
            ("r.", "l."),
        ]

        oppobone = bone_name  # Default to original name

        for pattern, replacement in patterns:
            if pattern in bone_name_lower:
                index = bone_name_lower.find(pattern)
                oppobone = bone_name[:index] + replacement + bone_name[index + len(pattern):]
                break
        else:
            # Handle cases where the name ends with 'l' or 'r'
            if bone_name_lower.endswith("l"):
                oppobone = bone_name[:-1] + "R"
            elif bone_name_lower.endswith("r"):
                oppobone = bone_name[:-1] + "L"
            else:
                centrebone = True

        # Verify if the opposite bone exists
        pose_bones = bpy.context.selected_objects[0].pose.bones
        if not any(b.name.lower() == oppobone.lower() for b in pose_bones):
            print("Possible error (or not) with", selbone.name)
            oppobone = selbone.name
            centrebone = True

        print("Selected bone:", selbone.name)
        print("Opposite bone:", oppobone)
        return [oppobone, centrebone]

    def recalculate_bone_paths(self):
        lastframe = bpy.context.scene.frame_end
        if bpy.context.selected_pose_bones:
            bpy.ops.pose.paths_clear()
            if bpy.context.preferences.addons["AnimScrubber"].preferences.recalculate_curves:
                headOrTail = "TAILS"
                if bpy.context.preferences.addons["AnimScrubber"].preferences.recalculate_curves_at_head:
                    headOrTail = "HEADS"
            #bpy.ops.pose.paths_calculate(start_frame=0, end_frame=lastframe + 1, bake_location=headOrTail)
            bpy.ops.pose.paths_calculate(display_type='RANGE', range='SCENE', bake_location=headOrTail)
        return