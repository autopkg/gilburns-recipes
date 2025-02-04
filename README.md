# Installomator Custom Processors

This repository provides two custom AutoPkg processors designed to handle Installomator labels and verify downloaded files:

- **LabelResolver.py** - Resolves Installomator labels into necessary download details.
- **LabelVerifier.py** - Verifies the Team ID of downloaded macOS packages or applications.

## Processors

### LabelResolver.py
Resolves Installomator labels to obtain the download URL, expected Team ID, file type, and other details.

#### Input Variables:
- `label_name` (required) - Installomator label to resolve.
- `local_label_path` (optional) - Path to local directory containing Installomator label files.

#### Output Variables:
- `name` - Application name.
- `downloadURL` - URL for downloading the application.
- `expectedTeamID` - Team ID for verification.
- `blockingProcesses` - List of processes that must be closed before installation.
- `type` - File type (dmg, pkg, zip, etc.).
- `file_extension` - Correct file extension for the downloaded file.
- `pathname` - Full path to the downloaded file.

### LabelVerifier.py
Verifies the Apple Team ID of a downloaded file using `spctl`.

#### Input Variables:
- `downloaded_file_path` (required) - Path to the downloaded file.
- `expectedTeamID` (required) - The expected Apple Team ID.
- `DISABLE_TEAMID_VERIFICATION` (optional) - If set to `True`, skips Team ID verification.

#### Output Variables:
- None (raises an error if verification fails).

## Example Recipes
Each recipe corresponds to a specific **Installomator label type**, ensuring the necessary processors and logic are included to handle that particular download format correctly:

- **Installomator.dmg.download.recipe** - Handles `.dmg` downloads.
- **Installomator.pkg.download.recipe** - Handles `.pkg` downloads.
- **Installomator.pkgInDmg.download.recipe** - Handles `.pkg` files inside a `.dmg`.
- **Installomator.pkgInZip.download.recipe** - Handles `.pkg` files inside a `.zip`.
- **Installomator.zip.download.recipe** - Handles `.zip` downloads that contain `.app` files.
- **Installomator.appInDmgInZip.download.recipe** - Handles `.zip` downloads that contain a `.dmg`, which then contains an `.app`.
- **Installomator.tbz.download.recipe** - Handles `.tbz` compressed application files.

## Usage
1. Add the repo contain the example recipes and Processors to your AutoPkg search paths.
1. Use the example recipes as a reference for your custom AutoPkg workflows or override them to use as a basis for your own needs.

## Stub Recipe
A single stub recipe is used to expose both processors to AutoPkg:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Description</key>
    <string>Stub recipe to expose the Installomator processors.</string>
    <key>Identifier</key>
    <string>com.github.gilburns.recipes.SharedProcessors</string>
    <key>MinimumVersion</key>
    <string>2.0</string>
</dict>
</plist>
```

To reference the processors in a recipe:

```xml
<key>Processor</key>
<string>com.github.gilburns.recipes.SharedProcessors/LabelResolver</string>
```

```xml
<key>Processor</key>
<string>com.github.gilburns.recipes.SharedProcessors/LabelVerifier</string>
```

## Contributors
Special thanks to [Elliot Jordan](https://github.com/homebysix) for assistance working out some of the issues I was having getting these fully functional.

If you have ideas on how to refine these processors, or want to submit PRs to refine these processors for AutoPkg workflows, please contribute!

---

Let me know if any improvements or clarifications are needed! 🚀

