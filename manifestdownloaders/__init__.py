import os
import shutil

from configloader import ConfigLoader
from versionutils import extract_manifest_id
from urllib.request import urlretrieve

PACKAGE_ROOT = os.path.join(__file__, "..")
MANIFESTS_CONFIG = "manifests_config.json"
validators = {
    "md_path": ConfigLoader.validate_file,
    "rman_path": ConfigLoader.validate_file,
    "manifest_path": ConfigLoader.validate_not_empty,
    "output_path": ConfigLoader.validate_folder
}


class ManifestDownloaders:
    def __init__(self):
        self.config = ConfigLoader(MANIFESTS_CONFIG, validators)

    def __apply_manifest_to_path(self, path: str, manifest: str) -> str:
        return path.replace("{manifest}", manifest)

    def __get_manifest_from_archive(self, manifest: str) -> str:
        archive_config = ConfigLoader(PACKAGE_ROOT + "\\" + MANIFESTS_CONFIG, validators)
        manifest_file = self.__apply_manifest_to_path(archive_config["manifest_path"], manifest)
        return manifest_file if os.path.isfile(manifest_file) else ""

    def __archive_manifest(self, manifest: str, manifest_path: str) -> str:
        archive_config = ConfigLoader(PACKAGE_ROOT + "\\" + MANIFESTS_CONFIG, validators)
        manifest_file = self.__apply_manifest_to_path(archive_config["manifest_path"], manifest)
        if os.path.abspath(manifest_path) != manifest_file:
            shutil.copy(manifest_path, manifest_file)
        return manifest_file

    def __get_manifest(self, manifest: str, archive: bool) -> str:
        manifest_id = extract_manifest_id(manifest)
        if os.path.isfile(manifest):
            return self.__archive_manifest(manifest_id, manifest) if archive else manifest

        archived_path = self.__get_manifest_from_archive(manifest_id)
        if archived_path != "":
            return archived_path

        manifest_url = f"https://valorant.secure.dyn.riotcdn.net/channels/public/releases/{manifest_id}.manifest"
        manifest_path = self.__apply_manifest_to_path(self.config["manifest_path"], manifest_id)
        urlretrieve(manifest_url, manifest_path)
        self.__archive_manifest(manifest, manifest_path)
        return manifest_path

    def md_download(self, manifest: str, filter_paks: str, output_path: str = None, archive: bool = False):
        manifest_path = self.__get_manifest(manifest, archive)
        bundle = "https://valorant.secure.dyn.riotcdn.net/channels/public/bundles/"
        command_line = f"{self.config['md_path']} " \
                       f"{manifest_path} " \
                       f"--bundle \"{bundle}\" " \
                       f"--filter \"{filter_paks}\" " \
                       f"--output {output_path if output_path else self.config['output_path']}"
        os.system(command_line)

    def rman_download(self, manifest: str, filter_paks: str, output_path: str = None, archive: bool = False):
        manifest_path = self.__get_manifest(manifest, archive)
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
    downloader = ManifestDownloaders()
    downloader_to_function = {
        "md": ManifestDownloaders.md_download,
        "rman": ManifestDownloaders.rman_download
    }

    download_type = True
    while download_type:
        downloader_type = input("Choose a downloader (md/rman): ")
        downloader_func = downloader_to_function.get(downloader_type, ManifestDownloaders.rman_download)
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
