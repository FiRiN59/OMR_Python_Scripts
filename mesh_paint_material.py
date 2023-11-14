import unreal
import asset_utils

# Assume we are working within the Editor's context
@unreal.uclass()
class EditorUtility(unreal.GlobalEditorUtilityBase):
    pass

# Main
def main():
    create_mesh_paint_material_material("M_MeshPaint")

# Create Mesh Paint Material
def create_mesh_paint_material_material(name):
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    matLib = unreal.MaterialEditingLibrary
    assetLib = unreal.EditorAssetLibrary

    matAssetPath = f"/Game/Materials/{name}"
    matInstAssetPath = f"/Game/Materials/{name}_Inst"
    asset_utils.delete_asset_if_exists(matAssetPath)
    asset_utils.delete_asset_if_exists(matInstAssetPath)

    mat = assetTools.create_asset(name, "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())

    # Texture Parameters
    base_colors = []
    normals = []
    orms = []

    # Node Postion Paramenters
    NodePositionX = -3000
    NodePositionY = -300
    NodeOffsetX = 200
    NodeOffsetY = 250

    # Vertex Color Nodes
    (VertexColorNode_Color, VertexColorNode_Normal, VertexColorNode_R_Occlusion, VertexColorNode_G_Roughness, VertexColorNode_B_Metallic) = [
        create_vertex_color_node(mat, desc, NodePositionX, NodePositionY + NodeOffsetY * index) 
        for index, desc in enumerate(["Base_Color", "Normal", "R_Occlusion", "G_Roughness", "B_Metallic"]) 
    ]

    NodePositionX += NodeOffsetX

    # One Minus Nodes
    (OneMinusNode_Color, OneMinusNode_Normal, OneMinusNode_R, OneMinusNode_G, OneMinusNode_B) = [
        create_one_minus_node(mat, NodePositionX, NodePositionY + NodeOffsetY * i)
        for i in range(5)
    ]

    NodePositionX += NodeOffsetX

    # BaseColor, Normal, and ORM Texture Parameters
    for i in range(5):
        # Texture Parameters
        (BaseColorParam, NormalParam, ORMParam) = [
            create_texture_parameter_node(mat, name, NodePositionX + NodeOffsetX * 1.5 * index, NodePositionY + NodeOffsetY * i)
            for index, name in enumerate(["BaseColor_{}".format(i + 1), "Normal_{}".format(i + 1), "ORM_{}".format(i + 1)])
        ]

        # Sampler Types
        NormalParam.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
        ORMParam.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)

        # Save in the arrays
        base_colors.append(BaseColorParam)
        normals.append(NormalParam)
        orms.append(ORMParam)

    NodePositionX += NodeOffsetX * 1.5 * 3

    # Lerp Nodes
    base_color_lerps = []
    normal_lerps = []
    orm_r_lerps = []
    orm_g_lerps = []
    orm_b_lerps = []

    for i in range(5):
        (base_color_lerp, normal_lerp, orm_r_lerp, orm_g_lerp, orm_b_lerp) = [
            create_lerp_node(mat, NodePositionX + NodeOffsetX * i, NodePositionY + NodeOffsetY * index)
            for index in range(5)
        ]

        base_color_lerps.append(base_color_lerp)
        normal_lerps.append(normal_lerp)
        orm_r_lerps.append(orm_r_lerp)
        orm_g_lerps.append(orm_g_lerp)
        orm_b_lerps.append(orm_b_lerp)

    # Base Color Connections
    for i in range(5):
        matLib.connect_material_expressions(base_colors[i], "", base_color_lerps[i], "B")

    matLib.connect_material_expressions(base_colors[4], "", base_color_lerps[0], "A")
    matLib.connect_material_expressions(OneMinusNode_Color, "", base_color_lerps[0], "Alpha")

    matLib.connect_material_expressions(VertexColorNode_Color, "A", OneMinusNode_Color, "")
    
    for index, channel in enumerate(["R", "G", "B", "A"]):
        matLib.connect_material_expressions(VertexColorNode_Color, channel, base_color_lerps[index + 1], "Alpha")

    for i in range(4):
        matLib.connect_material_expressions(base_color_lerps[i], "", base_color_lerps[i + 1], "A")

    matLib.connect_material_property(base_color_lerps[4], "", unreal.MaterialProperty.MP_BASE_COLOR)

    # Material Instance
    matInstance = assetTools.create_asset(f"{name}_Inst", "/Game/Materials", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    matInstance.set_editor_property("Parent", mat)

    # Save Assets
    assetLib.save_asset(matAssetPath)
    assetLib.save_asset(matInstAssetPath)

def create_vertex_color_node(material, description, pos_x, pos_y):
    node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionVertexColor.static_class(), pos_x, pos_y)
    node.set_editor_property("Desc", description)
    return node

def create_one_minus_node(material, pos_x, pos_y):
    node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionOneMinus.static_class(), pos_x, pos_y)
    return node

def create_texture_parameter_node(material, name, pos_x, pos_y):
    node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionTextureSampleParameter2D.static_class(), pos_x, pos_y)
    node.set_editor_property("ParameterName", unreal.Name(name))
    node.set_editor_property("sampler_source", unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)
    return node

def create_lerp_node(material, pos_x, pos_y):
    node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionLinearInterpolate.static_class(), pos_x, pos_y)
    return node

# Main
if __name__ == '__main__':
    main()