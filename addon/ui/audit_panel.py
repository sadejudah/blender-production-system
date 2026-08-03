import bpy


class BPS_PT_AuditPanel(bpy.types.Panel):
    """Main Blender Production System studio dashboard."""

    bl_idname = "BPS_PT_audit_panel"
    bl_label = "Blender Production System"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BPS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        score = int(scene.get("bps_last_score", 0))
        passes = int(scene.get("bps_last_passes", 0))
        failures = int(scene.get("bps_last_failures", 0))
        audit_has_run = bool(scene.get("bps_audit_has_run", False))

        # ---------------------------------------------------------
        # STUDIO HEADER
        # ---------------------------------------------------------

        header = layout.box()
        header.scale_y = 1.25

        title_row = header.row()
        title_row.alignment = "CENTER"
        title_row.label(
            text="BLENDER PRODUCTION SYSTEM",
            icon="HOME",
        )

        subtitle_row = header.row()
        subtitle_row.alignment = "CENTER"
        subtitle_row.label(text="Professional Production Studio")

        project_row = header.row()
        project_row.alignment = "CENTER"
        project_row.label(
            text="Kyro & Nyla's Learning Adventures",
            icon="RENDER_ANIMATION",
        )

        layout.separator()

        # ---------------------------------------------------------
        # PRODUCTION READINESS CARD
        # ---------------------------------------------------------

        readiness = layout.box()

        readiness_header = readiness.row()
        readiness_header.label(
            text="PRODUCTION READINESS",
            icon="CHECKMARK",
        )

        if audit_has_run:
            readiness.progress(
                factor=max(0.0, min(score / 100.0, 1.0)),
                type="BAR",
                text=f"{score}%",
            )

            if score == 100:
                status_text = "CERTIFIED — PRODUCTION READY"
                status_icon = "CHECKMARK"
            elif score >= 70:
                status_text = "CONDITIONAL PASS"
                status_icon = "INFO"
            else:
                status_text = "NOT PRODUCTION READY"
                status_icon = "ERROR"

            status_row = readiness.row()
            status_row.label(
                text=status_text,
                icon=status_icon,
            )

            summary = readiness.row(align=True)
            summary.label(
                text=f"Passed: {passes}",
                icon="CHECKMARK",
            )
            summary.label(
                text=f"Failed: {failures}",
                icon="ERROR",
            )

        else:
            readiness.label(
                text="Run an audit to calculate readiness.",
                icon="INFO",
            )

        audit_button = readiness.row()
        audit_button.scale_y = 1.5
        audit_button.operator(
            "bps.run_audit",
            text="RUN PRODUCTION AUDIT",
            icon="CHECKMARK",
        )

        layout.separator()

        # ---------------------------------------------------------
        # CREATE STUDIO
        # ---------------------------------------------------------

        create_card = layout.box()
        create_card.label(
            text="CREATE",
            icon="ADD",
        )

        create_grid = create_card.column(align=True)

        character_row = create_grid.row()
        character_row.enabled = False
        character_row.operator(
            "wm.call_menu",
            text="New Character — Coming Soon",
            icon="OUTLINER_OB_ARMATURE",
        )

        environment_row = create_grid.row()
        environment_row.enabled = False
        environment_row.operator(
            "wm.call_menu",
            text="New Environment — Coming Soon",
            icon="WORLD",
        )

        prop_row = create_grid.row()
        prop_row.enabled = False
        prop_row.operator(
            "wm.call_menu",
            text="New Prop — Coming Soon",
            icon="CUBE",
        )

        episode_row = create_grid.row()
        episode_row.enabled = False
        episode_row.operator(
            "wm.call_menu",
            text="New Episode — Coming Soon",
            icon="RENDER_ANIMATION",
        )

        layout.separator()

        # ---------------------------------------------------------
        # STUDIO MODULES
        # ---------------------------------------------------------

        modules = layout.box()
        modules.label(
            text="STUDIO MODULES",
            icon="FILE_FOLDER",
        )

        module_column = modules.column(align=True)

        character_studio = module_column.row()
        character_studio.enabled = False
        character_studio.label(
            text="Character Studio",
            icon="OUTLINER_OB_ARMATURE",
        )

        environment_studio = module_column.row()
        environment_studio.enabled = False
        environment_studio.label(
            text="Environment Studio",
            icon="WORLD",
        )

        project_builder = module_column.row()
        project_builder.enabled = False
        project_builder.label(
            text="Project Builder",
            icon="FILE_FOLDER",
        )

        asset_library = module_column.row()
        asset_library.enabled = False
        asset_library.label(
            text="Asset Library",
            icon="ASSET_MANAGER",
        )

        certification = module_column.row()
        certification.enabled = False
        certification.label(
            text="Certification Center",
            icon="CHECKMARK",
        )

        layout.separator()

        # ---------------------------------------------------------
        # FOOTER
        # ---------------------------------------------------------

        footer = layout.box()

        brand_row = footer.row()
        brand_row.alignment = "CENTER"
        brand_row.label(text="Sinoniyah Designs")

        version_row = footer.row()
        version_row.alignment = "CENTER"
        version_row.label(
            text="BPS Version 0.1.0 • Dashboard Preview",
            icon="INFO",
        )


classes = (
    BPS_PT_AuditPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)