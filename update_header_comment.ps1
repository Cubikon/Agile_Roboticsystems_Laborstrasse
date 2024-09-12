# Get the last commit date
$last_changed = git log -1 --format="%cd" --date=short

# Define the path to your Python script
$script_path = Join-Path $PSScriptRoot "GUI\Menu\ExperimentVorbereitung.py"

# Replace the __last_changed__ line in your Python script
(Get-Content $script_path) |
Foreach-Object {
    $_ -replace "^__last_changed__ = .*", "__last_changed__ = '$last_changed'"
} | Set-Content $script_path
