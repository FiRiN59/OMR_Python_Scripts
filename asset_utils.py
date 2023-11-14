import unreal

# Delete Asset If Exists
def delete_asset_if_exists(asset_path):
    assetLib = unreal.EditorAssetLibrary

    if assetLib.does_asset_exist(asset_path) and assetLib.delete_asset(asset_path):
        print(f"Asset '{asset_path}' deleted.")