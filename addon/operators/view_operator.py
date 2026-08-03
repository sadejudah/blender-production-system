import bpy


class BPS_OT_OpenBlueprintView(bpy.types.Operator):
    """Open a specific orthographic blueprint view."""

    bl_idname = "bps.open_blueprint_view"
    bl_label = "Open Blueprint View"
    bl_description = "Switch the 3D Viewport to a character blueprint view"

    view_axis: bpy.props.EnumProperty(
        name="View",
        items=(
            ("FRONT", "Front", "Open the front orthographic view"),
            ("RIGHT", "Side", "Open the right-side orthographic view"),
            ("BACK", "Back", "Open the back orthographic view"),
        ),
        default="FRONT",
    )

    def execute(self, context):
        view_area = None
        window_region = None

        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                view_area = area

                for region in area.regions:
                    if region.type == "WINDOW":
                        window_region = region
                        break

                if window_region:
                    break

        if view_area is None or window_region is None:
            self.report(
                {"ERROR"},
                "No 3D Viewport was found.",
            )
            return {"CANCELLED"}

        with context.temp_override(
            area=view_area,
            region=window_region,
        ):
            bpy.ops.view3d.view_axis(
                type=self.view_axis,
                align_active=False,
            )

            bpy.ops.view3d.view_selected(
                use_all_regions=False,
            )

        return {"FINISHED"}


classes = (
    BPS_OT_OpenBlueprintView,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
