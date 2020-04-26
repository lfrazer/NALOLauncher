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


class NALOStart:

    nalo_folder = "G:\\Games\\SteamLibrary\\steamapps\\common\\Natural Locomotion\\"
    nalo_exe = ""
    nalo_settings = ""

    #try:
    #   while True:

    # set this to true only if your monitors are in a strange order (for example, #2 is to the left of #1)
    disordered_monitors = True

    def initpaths(self):
        self.nalo_exe = self.nalo_folder + "naturallocomotion.exe"
        self.nalo_settings = self.nalo_folder + "settings.json"

    def startNALO(self):
        #os.system(nalo_exe)
        proc_args = [self.nalo_exe]
        subprocess.Popen(proc_args)

    def setNALOHandedConfig(self, left_handed_flag):
        fp = open(nalo_settings, "r")
        settings = json.load(fp)
        fp.close()

        if left_handed_flag:
            settings["left_handed"] = "yes"
        else:
            settings["left_handed"] = "no"
        
        fp = open(nalo_settings, "w")
        json.dump(settings, fp)
        fp.close()

        return

    def clickbutton(self, imgpath):
        startpos = None
        while startpos is None:
            try:
                startpos = pyautogui.locateOnScreen(imgpath, minSearchTime=30, grayscale=True, confidence=0.45)
                if(startpos is None):
                    print("Failed to detect img: " + imgpath)
            except:
                print("Unexpected error:", sys.exc_info()[0])

        print("Clicking image: " + imgpath + " startpos=" + str(startpos) )
        startpos_center = pyautogui.center(startpos)
        print("Image center: " + str(startpos_center))

        clickx = int(startpos_center.x)
        clicky = int(startpos_center.y)
        if (disordered_monitors):
            clickx = clickx - (int(chilimangoes.screen_size[0]) / 2)

        ctypes.windll.user32.SetCursorPos( clickx, clicky)
        time.sleep(0.25)
        pyautogui.click()

if __name__ == "__main__":

    ns = NALOStart() 
    ns.initpaths()
    ns.startNALO()

    pyautogui.screenshot = chilimangoes.grab_screen
    pyautogui.pyscreeze.screenshot = chilimangoes.grab_screen
    pyautogui.Size = lambda x, y: chilimangoes.screen_size

    # wait a bit for NALO to initalize
    time.sleep(2.0)

    ns.clickbutton("skyrimvr_select.png")
    ns.clickbutton("start_profile.png")



