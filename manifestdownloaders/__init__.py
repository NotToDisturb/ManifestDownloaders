import os
import shutil

from configloader import ConfigLoader
from versionutils import extract_manifest_id
from urllib.request import urlretrieve

MANIFEST_CONFIG = "manifests_config.json"
validators = {
    "manifest_downloader_path": ConfigLoader.validate_file,
    "rman_path": ConfigLoader.validate_file,
    "output_path": ConfigLoader.validate_folder,
    "manifests_path": ConfigLoader.validate_folder
}


class ManifestDownloader:
    def __init__(self):
        self.config = ConfigLoader(MANIFEST_CONFIG, validators)

    def __get_manifest_from_archive(self, manifest: str):
        manifest_file = self.config["manifests_path"] + manifest
        if os.path.isfile(manifest):
            return manifest_file
        if os.path.isfile(manifest + ".manifest"):
            return manifest + ".manifest"

    def __get_manifest(self, manifest: str) -> str:
        archived_path = self.__get_manifest_from_archive(manifest)
        if archived_path:
            return archived_path

        if os.path.isfile(manifest):
            manifest_name, manifest_dir = ManifestDownloader.__separate_path(manifest)
            if manifest_dir != self.config["manifests_path"]:
                shutil.copy(manifest, self.config["manifests_path"] + manifest_name)
            return manifest

        manifest_name = extract_manifest_id(manifest) + ".manifest"
        manifest_url = f"https://valorant.secure.dyn.riotcdn.net/channels/public/releases/{manifest_name}"
        urlretrieve(manifest_url, self.config["manifests_path"] + manifest_name)
        return self.config["manifests_path"] + manifest_name

    def md_download(self, manifest: str, filter_paks: str, output_path: str = None):
        manifest_path = self.__get_manifest(manifest)
        bundle = "https://valorant.secure.dyn.riotcdn.net/channels/public/bundles/"
        command_line = f"{self.config['manifest_downloader_path']} " \
                       f"{manifest_path} " \
                       f"--bundle \"{bundle}\" " \
                       f"--filter \"{filter_paks}\" " \
                       f"--output {output_path if output_path else self.config['output_path']}"
        os.system(command_line)

    def rman_download(self, manifest: str, filter_paks: str, output_path: str = None):
        manifest_path = self.__get_manifest(manifest)
        bundle = "http://valorant.secure.dyn.riotcdn.net/channels/public/"
        command_line = f"{self.config['rman_path']} " \
                       f"{manifest_path} " \
                       f"{output_path if output_path else self.config['output_path']} " \
                       f"--cdn \"{bundle}\" " \
                       f"--filter-path \"{filter_paks}\""
        os.system(command_line)

    @staticmethod
    def __separate_path(path):
        filename = os.path.basename(path)
        base_dir = os.path.dirname(path)
        return filename, base_dir


def __main():
    downloader = ManifestDownloader()
    downloader_to_function = {
        "md": ManifestDownloader.md_download,
        "rman": ManifestDownloader.rman_download
    }

    download_type = True
    while download_type:
        downloader_type = input("Choose a downloader (md/rman): ")
        downloader_func = downloader_to_function.get(downloader_type, ManifestDownloader.rman_download)
        download_manifest = True
        while download_manifest:
            print("\n")
            manifest = input("Choose a manifest: ")
            download_pak = True
            while download_pak:
                pak_filter = input("Choose a filter: ")
                downloader_func(downloader, manifest, pak_filter)
                download_pak = input("Download another pak in this manifest: ")
                download_pak = True if download_pak.lower() == "y" or download_pak.lower() == "yes" else False
            download_manifest = input("Download from another manifest: ")
            download_manifest = True if download_manifest.lower() == "y" or download_manifest.lower() == "yes" else False
        download_type = input("Download using another downloader: ")
        download_type = True if download_type.lower() == "y" or download_type.lower() == "yes" else False


if __name__ == "__main__":
    __main()
