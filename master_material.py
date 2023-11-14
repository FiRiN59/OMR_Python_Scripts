import unreal
import asset_utils

# Assume we are working within the Editor's context
@unreal.uclass()
class EditorUtility(unreal.GlobalEditorUtilityBase):
    pass

# Main
def main():
    create_master_material("M_Master")

# Create Master Material
def create_master_material(name):
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    matLib = unreal.MaterialEditingLibrary
    assetLib = unreal.EditorAssetLibrary

    matAssetPath = f"/Game/Materials/{name}"
    matInstAssetPath = f"/Game/Materials/{name}_Inst"
    asset_utils.delete_asset_if_exists(matAssetPath)
    asset_utils.delete_asset_if_exists(matInstAssetPath)

    mat = assetTools.create_asset(name, "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())

    baseColor = matLib.create_material_expression(mat, unreal.MaterialExpressionTextureSampleParameter, -384, -200)
    baseColor.set_editor_property("ParameterName", "Base Color")
    matLib.connect_material_property(baseColor, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)

    specular = matLib.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -384, 400)
    specular.set_editor_property("ParameterName", "Specular")
    matLib.connect_material_property(specular, "", unreal.MaterialProperty.MP_SPECULAR)

    normal = matLib.create_material_expression(mat, unreal.MaterialExpressionTextureSampleParameter, -384, 500)
    normal.set_editor_property("ParameterName", "Normal")
    matLib.connect_material_property(normal, "RGB", unreal.MaterialProperty.MP_NORMAL)

    orm = matLib.create_material_expression(mat, unreal.MaterialExpressionTextureSampleParameter, -384, 100)
    orm.set_editor_property("ParameterName", "ORM")
    matLib.connect_material_property(orm, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
    matLib.connect_material_property(orm, "G", unreal.MaterialProperty.MP_ROUGHNESS)
    matLib.connect_material_property(orm, "B", unreal.MaterialProperty.MP_METALLIC)

    matInstance = assetTools.create_asset(f"{name}_Inst", "/Game/Materials", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    matInstance.set_editor_property("Parent", mat)

    assetLib.save_asset(matAssetPath)
    assetLib.save_asset(matInstAssetPath)

# Main
if __name__ == '__main__':
    main()