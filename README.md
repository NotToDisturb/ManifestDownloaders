## ManifestDownloaders
ManifestDownloaders is a tool that allows easily downloading VALORANT paks 
using either [ManifestDownloader](https://github.com/Morilli/ManifestDownloader) or [rman](https://github.com/moonshadow565/rman)

## Package usage
#### Installation

`pip install git+https://github.com/NotToDisturb/ManifestDownloaders.git#egg=ManifestDownloaders`

The following tools are also required:
1. [ManifestDownloader](https://github.com/Morilli/ManifestDownloader)
1. [rman](https://github.com/moonshadow565/rman)

<br>
   
#### Documentation

- [`ManifestDownloaders`](#manifestdownloadersnbsp)
- [`<ManifestDownloaders instance>.md_download`](#manifestdownloader-instancemd_download)
- [`<ManifestDownloaders instance>.rman_download`](#manifestdownloader-instancerman_download)

<br>

> ##### `ManifestDownloaders()`&nbsp;
> 
> Creates an instace of ManifestDownloaders, loading the config. 
> Check the [Config file](#config-file) section and the [ConfigLoader repo](https://github.com/NotToDisturb/ConfigLoader)
> to learn more about how the config file works.

<br>

> ##### `<ManifestDownloader instance>.md_download(`
> &nbsp;&nbsp;&nbsp;&nbsp;`manifest: str, filter_paks: str,`<br>
> &nbsp;&nbsp;&nbsp;&nbsp;`output_path: str = None, archive: bool = False`<br>
> `)`
>
> Downloads the files matching `filter_paks` from `manifest`, which can be a URL, a path or a manifest id, using ManifestDownloader.
> - If `output_path` is provided the `output_path` in the config is overriden
> - If true, `archive` also copies the JSON to an archival path.
>   See more in the [Archiving](#Archiving) section.

<br>

> ##### `<ManifestDownloader instance>.rman_download(`
> &nbsp;&nbsp;&nbsp;&nbsp;`manifest: str, filter_paks: str,`<br>
> &nbsp;&nbsp;&nbsp;&nbsp;`output_path: str = None, archive: bool = False`<br>
> `)`
>
> Downloads the files matching `filter_paks` from `manifest`, which can be a URL, a path or a manifest id, using rman.dl. 
> This downloader is usually faster.
> - If `output_path` is provided the `output_path` in the config is overriden
> - If true, `archive` also copies the JSON to an archival path.
>   See more in the [Archiving](#Archiving) section.

<br><br>
#### Config file
ManifestDownloaders uses a configuration file to know where the needed tools and other paths are:

|Path              |Validation type|Description|
|------------------|---------------|-----------|
|**md_path**       |File           |Path to the ManifestDownloader executable.|
|**rman_path**     |File           |Path to the rman-dl executable.|
|**manifest_path**:|Not empty path |Path where the manifest file will be downloaded. Check out the available [manifest path keywords](#manifest-path-keywords).|
|**output_path**   |Folder         |Path the paks will be downloaded to.|

<br>

#### Manifest path keywords

|Keyword        |Description|
|---------------|-----------|
|`{manifest}`   |Replaced by the id of the manifest or name of the manifest file|

<br>

#### Example usage
Here is an example of how to use ManifestDownloaders:
```
from manifestdownloaders import ManifestDownloaders

downloader = ManifestDownloader()
downloader.rman_download("853077BEBD9F7A51", "en_US_Text")
```
The first time this script is run, it will exit after generating `manifests_config.json`.
Subsequent runs will continue exiting until the [configuration file](#config-file) is filled out correctly.
Once it is, the script will execute properly and the downloaded paks will be in the output path (`output_path` in the config). 

#### Archiving
ManifestDownloaders features an archival feature that allows the user to automatically archive 
every manifest file downloaded. The first time a script that uses ManifestsDownloader
is run with `archive=True`, a new config file will be generated within the installation path 
of ManifestDownloaders (shown by the script upon generation).

That configuration can be identical to the one in your project folder, but in order to not overwrite manifests, 
it is recommended that the filename of the path in `manifest_path` be `{manifest}.manifest`

## Standalone usage
It is also possible to use ManifestDownloaders as a standalone script:

1. Download the [latest release](https://github.com/NotToDisturb/ManifestDownloaders/releases/latest)
1. Extract the zip file
1. Open a console inside the extracted folder
1. Install the required packages using `pip install -r requirements.txt`
1. Run the script using `python manifestdownloaders.py`

In the first execution, the config file is created and needs to be filled out.
Check out [Installation](#installation) for the tools required and 
[Config file](#config-file) for more details on how to fill out the config.<br>
Running the script after filling out the config will prompt you for the type of downloader to use,
manifest to use and pak filter to apply.

## Credits
Morilli [Go](https://github.com/Morilli/) <br>
moonshadow [Go](https://github.com/moonshadow565/)