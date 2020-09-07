
import os, re, struct
GameSaveLocation = os.environ["userprofile"] + "\AppData\Local\FBS\Saved\SaveGames"
GameSaveIndexes = []
GameSaveFile = ""
MenuTitleBar = "============================================================\n"
MenuTitle = "Fishing: Barents Sea - Game Save Editor v1.0-alpha\nWritten By: David Wroten\n"

def SelectGameSave():
    global GameSaveFile
    os.system('cls')
    print(MenuTitleBar + MenuTitle + MenuTitleBar)
    print("Please select a game save to modify:\n")
    GameSaves = os.walk(GameSaveLocation)
    index = 0
    for (path, dirs, files) in GameSaves:
        for file in files:
            if re.match("Game[0-9]*\.sav", file):
                index = index + 1
                print(str(index) + ". "+ file)
                GameSaveIndexes.append(file)
    print("x. Exit")
    
    selection = input("\n Enter Selection: ")
    if selection == "x":
        quit()
    elif int(selection) > len(GameSaveIndexes):
        SelectGameSave()
    
    
    GameSaveFile = str(GameSaveLocation) + "\\" + str(GameSaveIndexes[(int(selection) - 1)])
    print(GameSaveFile)
    MainMenu()


def MainMenu():
    global GameSaveFile
    os.system('cls')
    print(MenuTitleBar + MenuTitle + MenuTitleBar)
    print("Current GameSaveFile: " + GameSaveFile + "\n")
    print("------------------------------------------------------------")
    print("Please select an attribute you would like to modify below")
    print("------------------------------------------------------------\n")
    print("1. CurrencyAvailable (This value is the current funds you have in game)")
    print("2. DistanceTraveledInKm (This value can be modified to unlock boating certifications)")
    
    print("s. Select another game save file")
    print("x. Exit")
    
    selection = input("\n\n Enter Selection: ")
    if selection == "1":
        key = "CurrencyAvailable"
        positionalOffset = 45
    elif selection == "2":
        key = "DistanceTraveledInKm"
        positionalOffset = 48
    elif selection == "s":
        SelectGameSave()
    elif selection == "x":
        quit()
    else:
        MainMenu()
        
    KeyValue = ReadBinary(key, positionalOffset)
    keyUpdate = input("\nCurrent Value: " + KeyValue + "\nNew Value (Must be 32 bit int): ")
    UpdateBinary(key, positionalOffset, keyUpdate)

def ReadBinary(key, positionalOffset):
    #Clear console screen
    os.system('cls')
    
    #Output operation
    print("\nOpening " + GameSaveFile)
    #Open game save file for reading.
    binaryData = open(GameSaveFile, "r+b")
    
    #Read the binary data and store it to be traversed.
    print("Reading...\n")
    Data = binaryData.read()
    
    #Locate the key in whiich we would like to modify the bytes. 
    AttributeLocation = Data.index(str.encode(key))
    
    #Set the pointer to the index of the key + positionalOffset bytes.
    binaryData.seek(AttributeLocation + positionalOffset)
    
    #Read the 4 float point bytes and close the file stream.
    KeyBytes = binaryData.read(4)
    print(MenuTitleBar + "Key Found!\n" + "\n" + key + ":" + " hex: " + str(hex(struct.unpack('<I', KeyBytes)[0])) + " bytes: " + str(KeyBytes) + "\n" + MenuTitleBar)
    binaryData.close()
    
    #Finally return the result
    return str(struct.unpack('f', KeyBytes)[0]).replace('.0','')
    
    binaryData.seek(AttributeLocation + 45)
    print(struct.unpack('<f', binaryData.read(4))[0])
    binaryData.seek(AttributeLocation + 45)
    print(bytes(struct.pack('<f', float('2000000000'))))
    #print(bytes(struct.unpack('<I', struct.pack('<f', float('2000000000')))[0]))
    
    
def UpdateBinary(key, positionalOffset, update):
    #Clear console screen
    os.system('cls')
    
    #Output operation
    print("\nOpening " + GameSaveFile)
    #Open game save file for reading.
    binaryData = open(GameSaveFile, "r+b")
    
    #Read the binary data and store it to be traversed.
    print("Preparing to replace bytes...\n")
    Data = binaryData.read()
    
    #Locate the key in whiich we would like to modify the bytes. 
    AttributeLocation = Data.index(str.encode(key))
    
    #Set the pointer to the index of the key + positionalOffset bytes.
    binaryData.seek(AttributeLocation + positionalOffset)
    
    #Write the 4 float point bytes and close the file stream.
    KeyBytes = binaryData.write(bytes(struct.pack('<f', float(update))))
    print("The following bytes have been written: " + str(bytes(struct.pack('<f', float(update)))) + ", hex: " + str(hex(struct.unpack('<I', bytes(struct.pack('<f', float(update))))[0])))
    input("\nPress any key to return to the main menu.")
    binaryData.close()
    
    #Bytes have been writen, return to menu
    MainMenu()

SelectGameSave()

