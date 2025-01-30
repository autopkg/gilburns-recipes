import subprocess
import os
import re
from autopkglib import Processor, ProcessorError, DmgMounter

class LabelVerifier(DmgMounter):
    """Verifies the Team ID of a downloaded macOS package or application using spctl.
       If the downloaded file is a DMG, it will be mounted before verification."""

    description = "Checks if the downloaded file has the expected Team ID."

    input_variables = {
        "downloaded_file_path": {"required": True, "description": "Path to the downloaded file."},
        "expectedTeamID": {"required": True, "description": "The expected Apple Team ID for verification."}
    }

    output_variables = {}

    def find_verifiable_file(self, mount_point):
        """Finds a .pkg or .app inside the mounted DMG."""
        for root, dirs, files in os.walk(mount_point):
            for file in files:
                if file.endswith(".pkg"):
                    return os.path.join(root, file)
            for dir in dirs:
                if dir.endswith(".app"):
                    return os.path.join(root, dir)
        return None

    def main(self):
        file_path = self.env["downloaded_file_path"]
        expected_team_id = self.env["expectedTeamID"]
        is_dmg = file_path.endswith(".dmg")
        mount_point = None

        try:
            if is_dmg:
                self.output(f"Attempting to mount DMG: {file_path}")
                mount_point = self.mount(file_path)
                file_path = self.find_verifiable_file(mount_point)
                if not file_path:
                    raise ProcessorError("No verifiable file found inside DMG.")

            self.output(f"Checking Team ID for file: {file_path}")
            spctl_command = ["/usr/sbin/spctl", "--assess", "-vv", "--type=install" if file_path.endswith(".pkg") else "--type=execute", file_path]

            result = subprocess.run(spctl_command, capture_output=True, text=True)
            output = result.stdout + result.stderr
            self.output(f"Raw output from verification command:\n{output}")

            match = re.search(r'origin=Developer ID (?:Application|Installer): .* \((.*?)\)', output)
            actual_team_id = match.group(1) if match else "UNKNOWN"

            self.output(f"Expected Team ID: {expected_team_id}")
            self.output(f"Actual Team ID: {actual_team_id}")

            if actual_team_id != expected_team_id:
                raise ProcessorError(f"Team ID does not match! Expected: {expected_team_id}, Found: {actual_team_id}")

        finally:
            if mount_point:
                self.output(f"Attempting to unmount: {mount_point}")
                unmount_result = subprocess.run(["/usr/bin/hdiutil", "detach", mount_point], capture_output=True, text=True)
                if unmount_result.returncode != 0:
                    self.output(f"Warning: Failed to unmount {mount_point}. Error: {unmount_result.stderr}")
                else:
                    self.output(f"Successfully unmounted {mount_point}")
