#!/bin/zsh

################################
# FUNCTIONS FUNCTIONS FUNCTIONS
################################

source "$(dirname "$0")/helper_functions.sh" # Load helper functions from a separate file

################################
# MAIN  MAIN  MAIN  MAIN  MAIN
################################

if [[ -z "$1" ]]; then
    echo "Label file path required"
    exit 1
fi

fullPathToLabel="$1"

# Ensure the label file exists
if [[ ! -f "$fullPathToLabel" ]]; then
    echo "Label file does not exist: $fullPathToLabel"
    exit 1
fi

label=$fullPathToLabel:t:r
pathOnly=$fullPathToLabel:h

# Suppress Installomator helper tools from running when labels are evaluated
INSTALL="force"

# Read contents of the label into a variable
labelFile=$(/bin/cat "${fullPathToLabel}")

# Run the case statement to evaluate the label and resolve variables
eval 'case "$label" in '"$labelFile"'; esac' >/dev/null 2>&1

# Required variables for AutoPkg
if [[ -z "$name" || -z "$downloadURL" || -z "$expectedTeamID" ]]; then
    echo "Error: Missing required variables in label: $label"
    exit 1
fi

# Ensure `blockingProcesses` is formatted correctly
if [[ -z "$blockingProcesses" ]]; then
    blockingProcesses="[]"
else
    # Convert Zsh array to a JSON array
    json_blockingProcesses=$(printf '"%s", ' "${blockingProcesses[@]}")
    blockingProcesses="[${json_blockingProcesses%, }]"
fi

# Ensure `type` is included in JSON (defaults to "dmg" if missing)
json_output=$(osascript -l JavaScript -e "
function run(argv) {
    return JSON.stringify({
        name: argv[0],
        downloadURL: argv[1],
        expectedTeamID: argv[2],
        blockingProcesses: JSON.parse(argv[3]),
        type: argv[4] || 'dmg'  // Default to dmg if not defined
    });
}
" "$name" "$downloadURL" "$expectedTeamID" "$blockingProcesses" "$type")


# Check if JXA returned an error
if [[ "$json_output" == ERROR* ]]; then
    echo "JXA JSON error: $json_output"
    exit 1
fi

# Output JSON
echo "$json_output"
