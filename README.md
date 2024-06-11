# RelaunchOfficial
For Education Purpose 

# Support with setting 960*540 DPI 160

Tool for reconnect roblox game running on emulator (**MuMu**) when crashing or found some error with anycode  except 268 cause you are hoping very fast then temp ban from roblox.

This project will provide full of python code.

    Prerequisite
    1. Python
    2. Pyinstaller (for compile file to exe) 
    3. Lib (Run command below will tell you what lib you need to install using "pip install")
  
  For running this project use this command

    py .\adb.py

## Config file

    {"gameId":"17017769292","privateLink1":"","privateLink2":"","time":10,"checkAxUI":120,"autoClose":{"enabled":"False","time":10,"Time in minute":{}},"joinFriend":{"enabled":"False","userId":12345678,"emulator index that will be first server Instance ":{},"serverStart":"","serverLast":""},"emulator":{"mode":"1","1 = all 2 = StartEmu1 3 = startEmu2":{},"startEmu1":"1","endEmu1":"1","startEmu2":"10","endEmu2":"19"},"AD":{"checkKaitun":"False"},"captureScreenToDiscord":{"enabled":"False","nameOfComputer":"Main","webhook":"","time":15}}

**gameId** - game id that contain in url in roblox url

    https://www.roblox.com/games/8737899170/HACKER-Pet-Simulator-99
    gameId is 8737899170

**privateLink** - instance link from private server link

    https://www.roblox.com/games/8737899170/Pet-Simulator-99?privateServerLinkCode=1234567890
    privateLink is 1234567890
    
**checkAxUI** - time (sec) for recheck Arceus X Ui already running or not if not will close client then open again

**autoClose** - for close roblox game every xx min

**joinFriend** - Place userId of your friend to join

**emulator** - Recommend to use mode = 1 for running all instance mode =2/mode =3 are manual input index of instance to run.

PS : Mode = 2 will use privateLink1 for join if you put vip instance // Mode = 3 will use privateLink2

**AD** - Support bot for anime defender UI

**captureScreenToDiscord** - Capture image of you computer and send to discord webhook

## Compile File
Compile file to exe for using on other computer that didn't install python and lib

    pyinstaller.exe --onefile --name "Relaunch" .\adb.py

## Folder of Image
This project using cv2 for check specific image that contain in large image or not

**Error Folder**
This folder contain all image of error from roblox and emu if you get stuck with any screen you can use snipping tool for cut image from folder **screenshots/** and save to this folder for using when found again

**UI Folder**
This folder contain ui of executor of Roblox for check executor running correct or not , If not will relaunch game again (no need to wait 20 min before idle code coming), And like error folder if in the future have any executor use can using snipping tool for cut image from folder **screenshots/** and save here for checking

**

## USE AT YOU OWN RISK CAUSE THIS IS 3RD PROGRAM

**

If you didn't want to compile you can download here : [PixelDrain](https://pixeldrain.com/u/Hp517xFP)

Virus total
File : [Virustotal](https://www.virustotal.com/gui/file/0cef0fe37e887743d641f093e698b73d48337d59c6ccc169da94d125b3746e93/detection)
File in PixelDrain : [Virustotal](https://www.virustotal.com/gui/url/58bdcae632c6428c626c220c27210045861e6cd4b1f42a6f02eea516353d8678?nocache=1)
