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
    scroll_clicks = -100

    # set this to true only if your monitors are in a strange order (for example, #2 is to the left of #1)
    disordered_monitors = True

    def __init__(self):
        configfile = "config.json"
        if os.path.isfile(configfile):
            fp = open(configfile, "r")
            config = json.load(fp)
            fp.close()

            self.nalo_folder = config["nalo_folder"]
            self.disordered_monitors = config["disordered_monitors"]
        else:
            print("Could not open config JSON file!")
        self.initpaths()

    def initpaths(self):
        # "steam://rungameid/798810"  (SteamID)
        self.nalo_exe = self.nalo_folder + "naturallocomotion.exe"  
        self.nalo_settings = self.nalo_folder + "settings.json"

    def startNALO(self):
        #os.startfile(self.nalo_exe)
        proc_args = ['cmd', '/c', 'start', 'steam://run/798810']
        subprocess.Popen(proc_args)

    def setNALOHandedConfig(self, left_handed_flag):
        if os.path.isfile(self.nalo_settings):
            fp = open(self.nalo_settings, "r")
            settings = json.load(fp)
            fp.close()

            if left_handed_flag:
                settings["left_handed"] = "yes"
            else:
                settings["left_handed"] = "no"
            
            fp = open(self.nalo_settings, "w")
            json.dump(settings, fp)
            fp.close()
        else:
            print("Left-handed config setup failed, could not find file: " + self.nalo_settings)
        return

    def movemouse(self, imgpath):
        startpos = None
        while startpos is None:
            #try:
            startpos = pyautogui.locateOnScreen(imgpath, minSearchTime=30, grayscale=True, confidence=0.6)
            if(startpos is None):
                print("Failed to detect img: " + imgpath)
            #except:
            #    print("Unexpected error:", sys.exc_info()[0])

        print("Clicking image: " + imgpath + " startpos=" + str(startpos) )
        startpos_center = pyautogui.center(startpos)
        print("Image center: " + str(startpos_center))

        clickx = int(startpos_center.x)
        clicky = int(startpos_center.y)
        if (self.disordered_monitors):
            clickx = clickx - (int(chilimangoes.screen_size[0]) / 2)

        ctypes.windll.user32.SetCursorPos( clickx, clicky)

    def clickbutton(self, imgpath):
        self.movemouse(imgpath)
        time.sleep(0.25)
        pyautogui.click()

    def startprofile(self, game_select, scroll_steps):
        
        # need to put the mouse over the game selection scroll UI before scrolling.. or it won't work
        if scroll_steps != 0:
            self.movemouse("bladesorcery_select.png")
            time.sleep(0.1)
            pyautogui.scroll(scroll_steps)
        
        time.sleep(0.25)
        self.clickbutton(game_select)
        self.clickbutton("start_profile.png")


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="NALO Launcher")
    argparser.add_argument("--gameimage", "-g", default="skyrimvr_select.png")
    argparser.add_argument("--scroll", "-s", type=int, default=-1)
    argparser.add_argument("--lefthanded", "-l", type=int, default=0)

    args = argparser.parse_args()
    print("Program Args: " + str(args))

    ns = NALOStart() 
    ns.setNALOHandedConfig( bool(args.lefthanded) )
    ns.startNALO()

    pyautogui.screenshot = chilimangoes.grab_screen
    pyautogui.pyscreeze.screenshot = chilimangoes.grab_screen
    pyautogui.Size = lambda x, y: chilimangoes.screen_size

    # wait a bit for NALO to initalize
    time.sleep(3.0)

    ns.startprofile(args.gameimage, args.scroll)



