#!/usr/local/autopkg/python

import subprocess
import json
import os
from autopkglib import Processor, ProcessorError

__all__ = ["LabelResolver"]

class LabelResolver(Processor):
    """Resolves Installomator labels into variables."""
    description = "Resolves an Installomator label and fetches downloadURL."
    input_variables = {
        "label_name": {"required": True, "description": "Installomator label to resolve."},
        "local_label_path": {"required": False, "description": "Path to local label files."}
    }
    output_variables = {
        "name": {"description": "Resolved application name."},
        "downloadURL": {"description": "Resolved download URL."},
        "expectedTeamID": {"description": "Resolved Team ID for verification."},
        "blockingProcesses": {"description": "List of processes that must be closed before installation."},
        "type": {"description": "File type of the download (dmg, pkg, zip, etc.)."},
        "file_extension": {"description": "Correct file extension for the downloaded file."},
        "pathname": {"description": "Full path to the downloaded file."},
        "filename": {"description": "Formatted filename for the downloaded file."}
    }

    def main(self):
        label_name = self.env.get("label_name")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        label_dir = os.path.join(script_dir, "labels")

        # Allow override of label path
        label_dir = self.env.get("local_label_path", label_dir)
        label_file_path = os.path.join(label_dir, f"{label_name}.sh")

        # Validate that the label file exists
        if not os.path.exists(label_file_path):
            raise ProcessorError(f"Label file not found: {label_file_path}")

        resolve_script_path = os.path.join(script_dir, "resolve_label.sh")

        if not os.path.exists(resolve_script_path):
            raise ProcessorError(f"resolve_label.sh not found at {resolve_script_path}")

        try:
            result = subprocess.run(
                ['zsh', resolve_script_path, label_file_path],
                capture_output=True, text=True, check=True
            )
            resolved_vars = json.loads(result.stdout)

            # Ensure required output variables are set
            if "name" in resolved_vars and "downloadURL" in resolved_vars and "expectedTeamID" in resolved_vars:
                self.env["name"] = resolved_vars["name"]
                self.env["downloadURL"] = resolved_vars["downloadURL"]
                self.env["expectedTeamID"] = resolved_vars["expectedTeamID"]
                self.env["blockingProcesses"] = resolved_vars.get("blockingProcesses", [])
                self.env["type"] = resolved_vars.get("type", "dmg")  # Default to dmg

                # Map Installomator types to actual file extensions
                file_extension_mapping = {
                    "dmg": ".dmg",
                    "zip": ".zip",
                    "tbz": ".tbz",
                    "appInDmgInZip": ".zip",  # Special case: needs additional processing later
                    "pkg": ".pkg",
                    "pkgInDmg": ".dmg",  # Contains a pkg inside
                    "pkgInZip": ".zip"   # Contains a pkg inside
                }

                self.env["file_extension"] = file_extension_mapping.get(self.env["type"], ".dmg")  # Default to dmg

                # Ensure "NAME" is properly set for AutoPkg processors
                self.env["NAME"] = self.env["name"]  # Fix for Unarchiver issue

                # Generate filename and pathname based on the resolved name and type
                filename = f"{self.env['name'].replace(' ', '_')}{self.env['file_extension']}"
                pathname = os.path.join(self.env.get("RECIPE_CACHE_DIR", "/tmp"), "downloads", filename)

                # **Explicitly strip unwanted quotes**
                self.env["filename"] = filename.replace('"', "").strip()
                self.env["pathname"] = pathname.replace('"', "").strip()

            else:
                raise ProcessorError("LabelResolver did not return all expected keys.")

        except subprocess.CalledProcessError as e:
            raise ProcessorError(f"Error resolving label: {e}")
        except json.JSONDecodeError:
            raise ProcessorError("Failed to parse JSON output from zsh script.")


if __name__ == '__main__':
    PROCESSOR = LabelResolver()
    PROCESSOR.execute_shell()
