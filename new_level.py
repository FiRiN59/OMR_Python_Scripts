import unreal
import argparse

# Assume we are working within the Editor's context
@unreal.uclass()
class EditorUtility(unreal.GlobalEditorUtilityBase):
    pass

# Main
def main():
    parser = argparse.ArgumentParser(description="Creates new level with basic setup.")
    parser.add_argument('--name', type=str, default="NewLevel", help='Level name')
    
    args = parser.parse_args()

    create_level(args.name)

# Create Level
def create_level(name):
    levelSubSys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    levelLibrary = unreal.EditorLevelLibrary
    assetLibrary = unreal.EditorAssetLibrary

    # New Level
    levelSubSys.new_level(f"/Game/Levels/{name}/LVL_{name}")

    # Lighting

    location = unreal.Vector(0, 0, 1000)
    folder_path = "Lighting"

    light = levelLibrary.spawn_actor_from_class(unreal.DirectionalLight, location)
    light.set_folder_path(folder_path)

    sky = levelLibrary.spawn_actor_from_class(unreal.SkyAtmosphere, location)
    sky.set_folder_path(folder_path)

    ppv: unreal.PostProcessVolume = levelLibrary.spawn_actor_from_class(unreal.PostProcessVolume, location)
    ppv.set_folder_path(folder_path)
    ppv.unbound = True # Affect whole scene

    # Disable autoexposure for more control
    # NOTE: This just sets the values, you still need to activate these properties in the editor
    # TODO: Figure out if this can be done from Python
    ppv.settings.auto_exposure_method = unreal.AutoExposureMethod.AEM_MANUAL
    ppv.settings.auto_exposure_apply_physical_camera_exposure = False
    #ppv.settings.set_editor_property("AutoExposureMethod", unreal.AutoExposureMethod.AEM_MANUAL, unreal.PropertyAccessChangeNotifyMode.ALWAYS)

    # Terrain

    location = unreal.Vector(0, 0, 0)

    navMesh = levelLibrary.spawn_actor_from_class(unreal.NavMeshBoundsVolume, location)
    navMesh.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)

    terrainGeneratorAsset = assetLibrary.load_asset("/Script/Engine.Blueprint'/Game/LevelUtils/TerrainGenerator/BP_TerrainGenerator.BP_TerrainGenerator'")
    terrainGenerator = levelLibrary.spawn_actor_from_object(terrainGeneratorAsset, location)
    terrainGenerator.set_editor_property("NavMesh", navMesh)

    # Player Start
    location = unreal.Vector(0, 0, 92)
    levelLibrary.spawn_actor_from_class(unreal.PlayerStart, location)

    # Save Level
    levelSubSys.save_current_level()

# Main
if __name__ == '__main__':
    main()