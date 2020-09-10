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

    def movemouse(self, imgpath, num_attempts=5):
        startpos = None
        count = 0
        while startpos is None and count < num_attempts:
            #try:
            count += 1
            startpos = pyautogui.locateOnScreen(imgpath, minSearchTime=30, grayscale=True, confidence=0.6)
            if(startpos is None):
                print("Failed to detect img: " + imgpath)
            #except:
            #    print("Unexpected error:", sys.exc_info()[0])

        if startpos is None:
            return False

        print("Clicking image: " + imgpath + " startpos=" + str(startpos) )
        startpos_center = pyautogui.center(startpos)
        print("Image center: " + str(startpos_center))

        clickx = int(startpos_center.x)
        clicky = int(startpos_center.y)
        if (self.disordered_monitors):
            clickx = clickx - (int(chilimangoes.screen_size[0] / 2))

        ctypes.windll.user32.SetCursorPos( ctypes.c_long(clickx), ctypes.c_long(clicky) )
        return True

    def clickbutton(self, imgpath):
        moveres = self.movemouse(imgpath)
        if moveres:
            time.sleep(0.25)
            pyautogui.click()
        return moveres

    def startprofile(self, game_select, scroll_steps):
        
        # need to put the mouse over the game selection scroll UI before scrolling.. or it won't work
        if scroll_steps != 0:
            self.movemouse("bladesorcery_select.png")
            time.sleep(0.1)
            pyautogui.scroll(scroll_steps)
        
        time.sleep(0.25)
        self.clickbutton(game_select)
        return self.clickbutton("start_profile.png")

    def checkerr(self, errimg, num_attempts=1):
        startpos = None
        imgpath = errimg
        count = 0
        while startpos is None and count < num_attempts:
            #try:
            count += 1
            startpos = pyautogui.locateOnScreen(imgpath, minSearchTime=3, grayscale=True, confidence=0.6)
            if(startpos is None):
                print("Failed to detect img: " + imgpath)
            #except:
            #    print("Unexpected error:", sys.exc_info()[0])

        if startpos is None:
            return False
        
        return True


def killprocbyname(procname):
    procs_tokill = []

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info["name"] == procname:
            procs_tokill.append(proc)
            print("Found process [to be killed] running.. PID=" + str(proc.info["pid"]))

    for proc in procs_tokill:
        proc.terminate()


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(description="NALO Launcher")
    argparser.add_argument("--gameimage", "-g", default="skyrimvr_select.png")
    argparser.add_argument("--scroll", "-s", type=int, default=-1)
    argparser.add_argument("--lefthanded", "-l", type=int, default=0)
    argparser.add_argument("--proglaunch", "-p", default="")
    argparser.add_argument("--progarg", "-a", default="")
    argparser.add_argument("--steamerrcheck", "-e", default="steamvr_err.png")

    args = argparser.parse_args()
    print("Program Args: " + str(args))

    # try to kill NALO if its running
    killprocbyname("natural_locomotion_launcher.exe")
    killprocbyname("naturallocomotion.exe")

    ns = NALOStart() 
    ns.setNALOHandedConfig( bool(args.lefthanded) )
    ns.startNALO()

    pyautogui.screenshot = chilimangoes.grab_screen
    pyautogui.pyscreeze.screenshot = chilimangoes.grab_screen
    pyautogui.Size = lambda x, y: chilimangoes.screen_size

    # wait a bit for NALO to initalize
    time.sleep(3.0)

    # check for steam VR errors
    if(args.steamerrcheck != "" and ns.checkerr(args.steamerrcheck)):
        # restart steamvr and try again..?
        killprocbyname("natural_locomotion_launcher.exe")
        killprocbyname("naturallocomotion.exe")
        killprocbyname("steamvr.exe")
        print("SteamVR error.. trying to restart everything..")
        time.sleep(20.0)
        #input("Press any key to exit..")
        

    else:
        startres = ns.startprofile(args.gameimage, args.scroll)

        if startres and args.proglaunch != "":
            proglaunch_cmd = [args.proglaunch]
            if args.progarg != "":
                proglaunch_cmd.append(args.progarg)
            subprocess.Popen(proglaunch_cmd)



