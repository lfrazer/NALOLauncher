# NALOLauncher
Automated Launcher for Natural Locomotion (VR tool)
Updated to support new NALO version with dark mode UI as of the end of 2020

# Setup
Install packages: pyautogui opencv-python psutil 
using pip.  
Make sure to setup paths and your monitor ordering in config.json
Disable auto-minimize option in NALO as the script can now perform this action

## Example command line (Blade & Sorcery)
"python.exe" nalostart.py --gameimage bladesorcery_select.png --scroll 0 --lefthanded 0 --proglaunch "E:\Games\SteamLibrary\steamapps\common\Blade & Sorcery\BladeAndSorcery.exe
