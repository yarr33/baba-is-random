#
# baba is you corrupter/randomizer.
#
# features:
# randomizing sprites              done
# randomizing colors               done
# randomizing palettes             done
# randomizing music                done
# randomizing sounds
# randomizing texts
# 

import subprocess
import sys
import imp
import time

try:
    imp.find_module("pillow")
    pass
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import shutil
import glob
import random
from copy import deepcopy as copy
from PIL import Image


paths = {"game"     : "",
         "modified" : ""}

gamePath , modifiedGamePath = "",""

language = "en"

lastOptions = {}
lastSpriteShuffling = {}

def readData():
    global lastOptions, lastSpriteShuffling
    try:
        data = open("last.txt", "r")
        readData = data.read().split(",")
        lastOptions = {"sprites" : tk.IntVar(),
                    "colors"  : tk.IntVar(),
                    "palettes": tk.IntVar(),
                    "music"   : tk.IntVar(),
                    "sfx"     : tk.IntVar(),
                    "text"    : tk.IntVar()}
        lastSpriteShuffling = {"text" : tk.IntVar(),
                                "tile" : tk.IntVar(),
                                "match": tk.IntVar()}
        paths["game"] = readData[0]
        paths["modified"] = readData[1]
        optionData = readData[2]
        lastOptions["sprites"].set(int(optionData[0]))
        lastOptions["colors"].set(int(optionData[1]))
        lastOptions["palettes"].set(int(optionData[2]))
        lastOptions["music"].set(int(optionData[3]))
        lastOptions["sfx"].set(int(optionData[4]))
        lastOptions["text"].set(int(optionData[5]))
        lastSpriteShuffling["text"].set(int(optionData[6]))
        lastSpriteShuffling["tile"].set(int(optionData[7]))
        lastSpriteShuffling["match"].set(int(optionData[8]))
        data.close()
    except:
        data = open("last.txt", "w")
        data.write(" , ,000000000")
        data.close()
        data = open("last.txt", "r")
        readData = data.read().split(",")
        lastOptions = {"sprites" : tk.IntVar(),
                    "colors"  : tk.IntVar(),
                    "palettes": tk.IntVar(),
                    "music"   : tk.IntVar(),
                    "sfx"     : tk.IntVar(),
                    "text"    : tk.IntVar()}
        lastSpriteShuffling = {"text" : tk.IntVar(),
                                "tile" : tk.IntVar(),
                                "match": tk.IntVar()}
        paths["game"] = readData[0]
        paths["modified"] = readData[1]
        optionData = readData[2]
        lastOptions["sprites"].set(int(optionData[0]))
        lastOptions["colors"].set(int(optionData[1]))
        lastOptions["palettes"].set(int(optionData[2]))
        lastOptions["music"].set(int(optionData[3]))
        lastOptions["sfx"].set(int(optionData[4]))
        lastOptions["text"].set(int(optionData[5]))
        lastSpriteShuffling["text"].set(int(optionData[6]))
        lastSpriteShuffling["tile"].set(int(optionData[7]))
        lastSpriteShuffling["match"].set(int(optionData[8]))
        data.close()

def saveData():
    data = open("last.txt", "w")
    data.write(paths["game"] +","+ paths["modified"] + "," +
                str(lastOptions["sprites"].get()) +
                str(lastOptions["colors"].get()) +
                str(lastOptions["palettes"].get()) +
                str(lastOptions["music"].get()) +
                str(lastOptions["sfx"].get()) +
                str(lastOptions["text"].get()) +
                str(lastSpriteShuffling["text"].get()) +
                str(lastSpriteShuffling["tile"].get()) +
                str(lastSpriteShuffling["match"].get()))
    data.close()

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except FileExistsError:
                pass
        else:
            shutil.copy2(s, d)

def getAllFiles(path, fileType):
    resultFiles = glob.glob(path + "/*." + fileType)
    return resultFiles

def deleteAllFiles(path, fileType):
    for file in getAllFiles(path, fileType):
        os.remove(file)

def nameByPath(path):
    return path.replace("\\","/").split("/")[-1]

def pathByPath(path):
    return "/".join(path.replace("\\","/").split("/")[:-1])

def shuffleSprites():
    sprites = getAllFiles(spritesPath, "png")
    spriteNumber = len(sprites)
    randomSprites = copy(sprites)
    spriteConvertions = {}
    index = 0
    for sprite in sprites:
        spriteName = nameByPath(sprite).split(".")[0]
        isGameSprite = spriteName[-2] == "_"
        isSpriteText = spriteName[:5] == "text_"

        proceed = True
        if(not spriteShuffling["tile"].get()):
            if not isSpriteText:
                proceed = False
        
        if(not spriteShuffling["text"].get()):
            if isSpriteText:
                proceed = False
        
        if(isGameSprite and proceed):
            if(spriteName[-1] == "1"):
                while True:
                    newSprite = randomSprites[random.randrange(len(randomSprites))]
                    newSpriteName = nameByPath(newSprite).split(".")[0]
                    isGameSprite = newSpriteName[-2] == "_"
                    isNewSpriteText = newSpriteName[:5] == "text_"

                    proceed = True
                    if(not spriteShuffling["tile"].get()):
                        if not isSpriteText:
                            proceed = False
                    if(not spriteShuffling["text"].get()):
                        if isSpriteText:
                            proceed = False
                    
                    if(isGameSprite and newSpriteName[-1] == "1" and proceed):
                        if(not spriteShuffling["match"].get()):
                            if(isNewSpriteText == isSpriteText):
                                break
                        else:
                            break
                randomSprites.remove(newSprite)
                if not (spriteName[:-2] in spriteConvertions):
                    spriteConvertions[spriteName[:-2]] = newSpriteName[:-2]
        elif(isGameSprite and not proceed):
            spriteConvertions[spriteName[:-2]] = spriteName[:-2]
            randomSprites.remove(sprite)

        index += 1
        updateProgressBar(index / spriteNumber * 100)

    index = 0
    for oldSprite in spriteConvertions:
        newSprite = spriteConvertions[oldSprite]
        for frame in range(3):
            oldSpritePath = spritesPath + "/" + newSprite + "_" + str(frame + 1) + ".png"
            newSpritePath = modifiedSpritesPath + "/" + oldSprite + "_" + str(frame + 1) + ".png"
            shutil.copyfile(oldSpritePath, newSpritePath)
            index += 1
            updateProgressBar(index / spriteNumber * 100)
        
def shuffleAudio():
    audioFiles = getAllFiles(audioPath, "ogg")
    audioFilesNumber = len(audioFiles)
    audioNames = []
    for audioFile in audioFiles:
        audioNames.append(nameByPath(audioFile))
    random.shuffle(audioNames)
    fileIndex = 0
    for audioFile in audioFiles:
        shutil.copy(audioFile, modifiedAudioPath + "/" + audioNames[fileIndex])
        fileIndex += 1
        updateProgressBar(fileIndex / audioFilesNumber)

def shufflePalettes():
    paletteFiles = getAllFiles(palettesPath, "png")
    paletteFilesNumber = len(paletteFiles)
    paletteNames = []
    for paletteFile in paletteFiles:
        paletteNames.append(nameByPath(paletteFile))
    random.shuffle(paletteNames)
    fileIndex = 0
    for paletteFile in paletteFiles:
        shutil.copy(paletteFile, modifiedPalettesPath + "/" + paletteNames[fileIndex])
        fileIndex += 1
        updateProgressBar(fileIndex / paletteFilesNumber * 100)

def shuffleColors():
    paletteFiles = getAllFiles(modifiedPalettesPath, "png")
    length = len(paletteFiles * 5 * 7)
    i = 0
    for paletteFile in paletteFiles:
        brightness = random.randrange(50, 100)
        palette = Image.open(paletteFile)
        pixels = palette.load()
        size = palette.size
        w = size[0]
        h = size[1]
        for x in range(w):
            for y in range(h):
                newColor = copy(pixels[x,y])
                newColor = (newColor[0] + random.randrange(-brightness, brightness),newColor[1] + random.randrange(-brightness, brightness),newColor[2] + random.randrange(-brightness, brightness))
                pixels[x,y] = newColor
                updateProgressBar(i / length * 100)
        palette.save(paletteFile)

mstr = tk.Tk()
mstr.geometry("600x600")
mstr.title("baba is random")

readData()

sprites = tk.IntVar()

options = lastOptions
spriteShuffling = lastSpriteShuffling

entry_widget_gamePath = None
entry_widget_newGamePath = None

def askPathGame():
    global gamePath
    gamePath = filedialog.askdirectory()
    if(gamePath != None):
        entry_widget_gamePath.delete(0, "end")
        entry_widget_gamePath.insert(0, gamePath)
        paths["game"] = gamePath

def askPathNewGame():
    global modifiedGamePath
    modifiedGamePath = filedialog.askdirectory()
    if(modifiedGamePath != None):
        entry_widget_newGamePath.delete(0, "end")
        entry_widget_newGamePath.insert(0,  modifiedGamePath)
        paths["modified"] = modifiedGamePath

def showHelp():
    for widget in mstr.winfo_children():
        widget.destroy()
    btn = tk.Button(mstr, text = "< back", command = showMenu)
    btn.place(x = 30, y = 10)
    label = tk.Label(mstr, text ="baba is help and info", font = "Arial 20 bold underline") 
    label.pack(side = tk.TOP, pady = 5)
    label = tk.Label(mstr, text ="""CREATING A NEW GAME
    to create a game, select 'create a new game' in the start menu. a new window will show up. 
    in that window you can select the options for the shuffling. then, you will need to select
    the game path and the modified game path. the game path is the folder where baba is you.exe
    located. the modified path is an empty folder where a new exe will appear. the paths that
    you selected will automatically appear in future uses. note: creating a new modified game
    in a folder of an already generated modified game will overwrite it.
    then, go to the modified game file and run the exe. enjoy.
    
CREATING A NEW GAME WITH THE LAST SETTINGS
    clicking on 'create a game with last settings' will instantly start generating a new
    game with the last settings and last shuffling options. if any error appears, please create
    a new game normally and fix the problem.

this version might still have bugs!
    """, font = "Arial 9", anchor = "e", justify = tk.LEFT) 
    label.place(x = 5, y = 50)

langSel = None

def showCreateNewGame(action = "new"):
    global langSel
    global entry_widget_gamePath
    global entry_widget_newGamePath
    for widget in mstr.winfo_children():
        widget.destroy()
    btn = tk.Button(mstr, text = "< back", command = showMenu)
    btn.place(x = 30, y = 10)
    
    label = tk.Label(mstr, text ="baba make game", font = "Arial 20 bold underline") 
    label.pack(side = tk.TOP, pady = 5)
    label = tk.Label(mstr, text ="options:", font = "Arial 10") 
    label.place(x = 5, y = 70)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle sprites",
                                    variable = options["sprites"])
    checkbutton_widget.select()
    checkbutton_widget.place(x = 10, y = 90)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle text sprites",
                                    variable = spriteShuffling["text"])
    checkbutton_widget.place(x = 25, y = 110)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle tiles sprites",
                                    variable = spriteShuffling["tile"])
    checkbutton_widget.place(x = 25, y = 130)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="mix between text and tile sprites",
                                    variable = spriteShuffling["match"])
    checkbutton_widget.place(x = 25, y = 150)

    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle music",
                                    variable = options["music"])
    checkbutton_widget.place(x = 10, y = 170)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle palettes",
                                    variable = options["palettes"])
    checkbutton_widget.place(x = 10, y = 190)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle palette colors",
                                    variable = options["colors"])
    checkbutton_widget.place(x = 10, y = 210)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle sound effects",
                                    variable = options["sfx"])
    checkbutton_widget.place(x = 10, y = 230)
    checkbutton_widget = tk.Checkbutton(mstr,
                                    text="shuffle texts",
                                    variable = options["text"])
    checkbutton_widget.place(x = 10, y = 250)

    langSel = ttk.Combobox(mstr, width = 5, values = ["en","ces","de","eo","es","fr","it","jpn","kr","nl","no","pl","pt","ptbr","tha","tr","vi","zhcn"])
    langSel.set('en')
    langSel.place(x = 100, y = 250)

    if(action == "new"):
        label = tk.Label(mstr, text ="paths:", font = "Arial 10") 
        label.place(x = 5, y = 300)

        label = tk.Label(mstr, text ="game path:", font = "Arial 10") 
        label.place(x = 10, y = 320)

        entry_widget_gamePath = tk.Entry(mstr)
        entry_widget_gamePath.insert(0, paths["game"])
        entry_widget_gamePath.place(x = 180, y = 320)

        btn = ttk.Button(mstr,  
                text ="browse...", 
                command = askPathGame) 
        btn.place(x = 310, y = 317)

        label = tk.Label(mstr, text ="modified game path:", font = "Arial 10") 
        label.place(x = 10, y = 350)

        entry_widget_newGamePath = tk.Entry(mstr)
        entry_widget_newGamePath.insert(0, paths["modified"])
        entry_widget_newGamePath.place(x = 180, y = 350)

        btn = ttk.Button(mstr,  
                text ="browse...", 
                command = askPathNewGame) 
        btn.place(x = 310, y = 347)

    btnDone = ttk.Button(mstr,  
            text ="done", 
            command = startProcessing) 
    btnDone.place(x = 310, y = 500)

def showMenu():
    for widget in mstr.winfo_children():
        widget.destroy()
    
    label = tk.Label(mstr, text ="baba is random", font = "Arial 20 bold underline") 
    label.pack(side = tk.TOP, pady = 5)

    label = tk.Label(mstr, text ="baba is you corrupter tool by yarr33. creates a new game\nbut with randomized assets!", font = "Arial 9 italic") 
    label.pack(side = tk.TOP, pady = 0) 

    label = tk.Label(mstr, text ="please choose an option:", font = "Arial 15 italic") 
    label.pack(side = tk.TOP, pady = 20) 
    btn = ttk.Button(mstr,  
                text ="create a new game",
                style = 'TButton',
                command = showCreateNewGame)
    btn.pack(pady = 2) 
    btn1 = ttk.Button(mstr,  
                text ="create a game with last settings",
                command = startInstantProcessing)
    btn1.pack(pady = 2) 
    btn2 = ttk.Button(mstr,  
                text ="help & information", 
                command = showHelp) 
    btn2.pack(pady = 2) 

def startInstantProcessing():
    startProcessing(True)

def startProcessing(instant = False):
    global lastOptions, lastSpriteShuffling, language
    if(instant):
        gamePath = paths["game"]
        modifiedGamePath = paths["modified"]
    else:
        gamePath = entry_widget_gamePath.get()
        modifiedGamePath = entry_widget_newGamePath.get()
        language = langSel.get()
    if(gamePath != modifiedGamePath):
        if(os.path.isdir(gamePath) and os.path.isdir(modifiedGamePath)):
            lastSpriteShuffling = spriteShuffling
            lastOptions = options
            saveData()
            mstr.destroy()
        else:
            messagebox.showwarning("error", "please enter valid paths.")
    else:
        messagebox.showwarning("error", "please enter different paths.")

mstr.protocol("WM_DELETE_WINDOW", quit)

style = ttk.Style()
style.configure('TButton', background = "#dbeeff", width = 40)

showMenu()

tk.mainloop()

progress = 0

progressWin = tk.Tk()
progressWin.title("baba is random")
progressWin.geometry("300x100")

progressLabel = tk.Label(progressWin, text="")
progressBar = ttk.Progressbar(progressWin,orient = tk.HORIZONTAL, length=300, mode='determinate')

progressLabel.pack()
progressBar.pack()

def updateProgressMessage(message):
    progressLabel['text'] = message

def updateProgressBar(value):
    progressBar['value'] = value
    progressWin.update_idletasks()

def unclose():
    pass

updateProgressMessage("starting...")
updateProgressBar(0)

progressWin.protocol("WM_DELETE_WINDOW", unclose)

gamePath = paths["game"]
modifiedGamePath = paths["modified"]

gameDataPath = gamePath + "/Data"
modifiedGameDataPath = modifiedGamePath + "/Data"

if (os.path.exists(modifiedGameDataPath)):
    shutil.rmtree(modifiedGameDataPath)

copytree(gamePath, modifiedGamePath)

subPath = "/".join(gamePath.split("/")[:-1])

spritesPath = gameDataPath + "/Sprites"
palettesPath = gameDataPath + "/Palettes"
audioPath = gameDataPath + "/Music"
languageFile = gameDataPath + "/Languages/lang_" + language + ".txt"
valuesFile = gameDataPath + "/values.lua"

modifiedSpritesPath = modifiedGameDataPath + "/Sprites"
modifiedPalettesPath = modifiedGameDataPath + "/Palettes"
modifiedAudioPath = modifiedGameDataPath + "/Music"
modifiedLanguageFile = modifiedGameDataPath + "/Languages/lang_" + language + ".txt"
modifiedValuesFile = modifiedGameDataPath + "/values.lua"

def process():
    if(options["sprites"].get()):
        updateProgressMessage("shuffling sprites")
        deleteAllFiles(modifiedSpritesPath, "png")
        shuffleSprites()

    if(options["music"].get()):
        updateProgressMessage("shuffling music")
        deleteAllFiles(modifiedAudioPath, "ogg")
        shuffleAudio()

    if(options["palettes"].get()):
        updateProgressMessage("shuffling palettes")
        deleteAllFiles(modifiedPalettesPath, "png")
        shufflePalettes()

    if(options["colors"].get()):
        updateProgressMessage("shuffling colors")
        shuffleColors()

    if(options["sfx"].get()):
        updateProgressMessage("shuffling sfx")
        soundsList = ["pop", "", "plop", "turn", "move_hi", "tele", "lock", "move", "burn", "done", "silent"]
        randomSoundsList = ["pop", "", "plop", "turn", "move_hi", "tele", "lock", "move", "burn", "done", "silent"]
        soundsListLength = len(soundsList)
        random.shuffle(randomSoundsList)
        valuesData = open(valuesFile, "r")
        valuesDataRead = valuesData.read()
        valuesData.close()
        i = 0
        for sound in soundsList:
            valuesDataRead = valuesDataRead.replace("name = \"" + sound + "\"", "name_new = \"" + randomSoundsList[i] + "\"")
            i+=1
            updateProgressBar(i / soundsListLength * 100)
        valuesDataRead = valuesDataRead.replace("name_new", "name")
        newValuesData = open(modifiedValuesFile, "w")
        newValuesData.write(valuesDataRead)
        newValuesData.close()

    if(options["text"].get()):
        updateProgressBar(0)
        updateProgressMessage("shuffling text")
        languageFileData = open(languageFile, "r")
        languageFileDataRead = languageFileData.readlines()
        languageFileData.close()
        lines = []
        keys = []
        values = []
        length = len(languageFileDataRead)
        i = 0
        for line in languageFileDataRead:
            if("=" in line):
                lines.append("")
                keys.append(line.split("=")[0])
                values.append(line.split("=")[1])
            else:
                lines.append(line)
                keys.append("")
            i += 1
            updateProgressBar(i / length * 100)
        random.shuffle(values)
        newLanguageData = ""
        i = 0
        key_i = 0
        for line in lines:
            key = keys[i]
            if(key == ""):
                newLanguageData += line
            else:
                value = values[key_i]
                newLanguageData += key + "=" + value
                key_i += 1
            newLanguageData += "\n"
            i+=1
            updateProgressBar(int(i / length * 100))
        newLanguageDataFile = open(modifiedLanguageFile, "w")
        newLanguageDataFile.write(newLanguageData)
        newLanguageDataFile.close()

    updateProgressMessage("done")
    time.sleep(1)
    progressWin.destroy()


progressWin.after(100, process)
progressWin.mainloop()

