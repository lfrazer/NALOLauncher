import os
import subprocess
import pyautogui
import time
import sys
import json
import chilimangoes
import ctypes
import ctypes.wintypes
import argparse
import psutil
import winreg
import nalostart

#flags for win32 proc creation aren't available in "subprocess" yet in Python 3.6 unfortunately
CREATE_NEW_CONSOLE = 0x00000010
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200


def isprocrunning(procname) -> bool:
    procs_tokill = []

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info["name"] == procname:
            return True
    
    return False


def startsteam():
    # grab steam path from registry
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
    except:
        hkey = None
        print(sys.exc_info())

    try:
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        steam_path = None
        print(sys.exc_info())
    
    if steam_path is not None:
        steam_exe_path = steam_path[0] + "\\steam.exe"
        proc_args = ['cmd', '/c', 'start', steam_exe_path]
        #subprocess.run(proc_args)
        subprocess.Popen(proc_args, creationflags=CREATE_NEW_CONSOLE | CREATE_NEW_PROCESS_GROUP)
        #os.system(steam_exe_path)

def startvivewireless():
    wifi_util_path = "C:\\Program Files\\VIVE Wireless\\ConnectionUtility\\HtcConnectionUtility.exe"
    proc_args = ['cmd', '/c', 'start', wifi_util_path, "/force"]
    #subprocess.run(proc_args)
    subprocess.Popen(proc_args, creationflags=CREATE_NEW_CONSOLE | CREATE_NEW_PROCESS_GROUP)
    #os.system(wifi_util_path)

if __name__ == "__main__":
    ns = nalostart.NALOStart()

    pyautogui.screenshot = chilimangoes.grab_screen
    pyautogui.pyscreeze.screenshot = chilimangoes.grab_screen
    pyautogui.Size = lambda x, y: chilimangoes.screen_size

    if isprocrunning("steam.exe"):
        startsteam()
        time.sleep(0.3)
        ns.clickbutton("steam_menu.PNG")
        ns.clickbutton("steam_menu_exit_button.PNG", 0.5)

    vive_wireless_proc = "HtcConnectionUtility.exe"
    if isprocrunning(vive_wireless_proc):
        nalostart.killprocbyname(vive_wireless_proc)

    if isprocrunning("vrserver.exe"):
        nalostart.killprocbyname("vrserver.exe")

    #startsteam()
    #startvivewireless()
    time.sleep(1.0)






