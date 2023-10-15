import random
import unreal

actor_class = unreal.StaticMeshActor.static_class()
static_mesh = unreal.load_asset("/Script/Engine.StaticMesh'/Game/DeepElderCaves/Meshes/Props/SM_TreasureChest_C_01.SM_TreasureChest_C_01'")

for i in range(50):
    location = unreal.Vector(random.uniform(-2000, 2000), random.uniform(-2000, 2000), 0)
    rotation = unreal.Rotator(0, 0, random.uniform(0, 360))
    new_actor:unreal.StaticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
    new_actor.static_mesh_component.set_static_mesh(static_mesh)
    new_actor.tags.append("Chest")
    new_actor.tags.append("PCG Exclude")
    new_actor.set_folder_path("Chests")