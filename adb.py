import subprocess
import re

# Function to count running instances by exact name
def count_running_instances(program_name):
    # Get a list of all running processes
    result = subprocess.run(['tasklist'], capture_output=True, text=True)

    # Remove leading/trailing whitespace and split into lines
    process_lines = result.stdout.strip().split('\n')

    # Create a regular expression to match the exact program name
    pattern = re.compile(rf'^{program_name}\b', re.IGNORECASE)

    # Count exact matches for the program name
    count = sum(1 for line in process_lines if pattern.search(line))
    return count

# Check running instances
program_name = 'Relaunch.exe'
max_instances = 4
running_count = count_running_instances(program_name)

# Exiting if too many instances are running
if running_count > max_instances:
    print(f"Warning: Too many instances of {program_name} running: {running_count}. Exiting.")
    # Optionally close all instances before exiting
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == program_name.lower():
            proc.kill()  # Be careful with process termination
    exit(1)

import time
import os
import requests
from ppadb.client import Client as AdbClient
from PIL import Image
from PIL import ImageGrab
from io import BytesIO
import json
import cv2

if running_count > 2:
    name_of_config = "config/config2.json"
else:
    name_of_config = "config/config1.json"

with open(name_of_config, "r") as file:
    config = json.load(file)

# Access configuration parameters
gameId = config["gameId"]
autoClose = config["autoClose"]["enabled"]

if autoClose == "True":
    autoClose = True
else:
    autoClose = False

autoCloseTime = config["autoClose"]["time"] * 60
privateLink = config["privateLink1"]
CHECK_INTERVAL = config.get('time', 5)
emulator_mode = config['emulator']['mode']
joinFriend = config['joinFriend']['enabled']
USERID = config['joinFriend']['userId']

# Anime Defender
AD = config['AD']['checkKaitun']
if AD == "True":
    AD = True
    print("Client Enable Check AD Kaitun")
else:
    AD = False

# Constants
PACKAGE_NAME = "com.roblox.client"
TARGET_ACTIVITY = ".ActivityNativeMain"
CHECK_INTERVAL = config['time']  # Time between checks in seconds
SCREENSHOT_PATH_DEVICE = "/sdcard/screenshot.png"  # Screenshot path on the device
LOCAL_SCREENSHOT_PATH = "./screenshots/"
NAME_SCREENSHOT = "screenshot.png"
IMG_FOLDER = "./img/Error"
IMG_UI_FOLDER = "./img/Ui"
image_text_cache = {}
image_ui_cache = {}
TIME_RUNNING = 0
STATE_CLOSE = False
LOGININSTANCE = f"roblox://placeid={gameId}"
LOGINVIP = f"roblox://placeid={gameId}&linkCode={privateLink}"
JOINFRIEND =  f"roblox://userId={USERID}&joinAttemptOrigin=JoinUser"
STATE_JOINING = "VIP"

#for check ui
checkAxUITime = config["checkAxUI"]
json_file = 'config/image.json'
robloxui = cv2.imread('img/robloxui.png', cv2.IMREAD_GRAYSCALE)
guiadk = cv2.imread('img/Ad/guiadk.png', cv2.IMREAD_GRAYSCALE)

# for discord web
enabledDiscord = config['captureScreenToDiscord']['enabled']
nameOfComputer = config['captureScreenToDiscord']['nameOfComputer']
webhook = config['captureScreenToDiscord']['webhook']
timeDiscord = config['captureScreenToDiscord']['time']

if webhook == "" or enabledDiscord == "False":
    enabledDiscord = False
else:
    enabledDiscord = True

if privateLink == "" : 
    STATE_JOINING = "NORMAL"

if joinFriend == "True":
    STATE_JOINING = "FRIEND"

def capture_screen():
    # Capture the screen
    screenshot = ImageGrab.grab()
    resized_screenshot = screenshot.resize((1024, 768))
    return screenshot

def send_to_discord(image, custom_text):
    # Convert image to bytes
    image_buffer = BytesIO()
    image.save(image_buffer, format='PNG')
    image_buffer.seek(0)

    # Create payload for Discord webhook
    payload = {
        'username': 'RelaunchCaptureBot',
        'content': custom_text
    }

    # Send the image and payload to Discord webhook
    files = {'file': ('screenshot.png', image_buffer, 'image/png')}
    response = requests.post(webhook, data=payload, files=files)

def hookDiscord():
    if enabledDiscord:
        try:
            screenshot = capture_screen()
            custom_text = f"Computer {nameOfComputer} : captured at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            send_to_discord(screenshot , custom_text)
        except Exception as e:
            print( f"Computer {nameOfComputer} : Something wrong when cpature and send screen")

# Functions
def is_app_running(adb_device, package_name):
    try:
        processes = adb_device.shell("ps -A")
        return package_name in processes
    except Exception as e:
        return False

def launch_app(adb_device , case):
    try:
        if STATE_JOINING == "NORMAL":
            command = f"am start -a android.intent.action.VIEW -d '{LOGININSTANCE}'"
        elif STATE_JOINING == "VIP":
            command = f"am start -a android.intent.action.VIEW -d '{LOGINVIP}'"
        elif STATE_JOINING == "FRIEND":
            command = f"am start -a android.intent.action.VIEW -d '{JOINFRIEND}'"
        adb_device.shell(command)
    except Exception as e:
        print(f"Device {adb_device.serial}: Client Offline")
        return False

def stop_app(adb_device, package_name):
    try:
        command = f"am force-stop {package_name}"
        adb_device.shell(command)
    except Exception as e:
        return False

def is_activity_in_foreground(adb_device, package_name, target_activity):
    try:
        activity_info = adb_device.shell("dumpsys activity activities | grep ResumedActivity")
        return f"{package_name}/{target_activity}" in activity_info
    except Exception as e:
        return False 

def is_activity_splash(adb_device, package_name):
    try:
        activity_info = adb_device.shell("dumpsys activity activities | grep ResumedActivity")
        return f"{package_name}/.ActivitySplash" in activity_info
    except Exception as e:
        return False

def capture_screenshot(adb_device):
    try:
        adb_device.shell(f"screencap -p {SCREENSHOT_PATH_DEVICE}")
        adb_device.pull(SCREENSHOT_PATH_DEVICE, f"{LOCAL_SCREENSHOT_PATH}{adb_device.serial.split(":")[1]}{NAME_SCREENSHOT}")
    except Exception as e:
        return False

# Function to populate the cache with OCR text
def populate_image_text_cache(image_folder):
    global image_text_cache
    for img_file in os.listdir(image_folder):
        reference_image_path = os.path.join(image_folder, img_file)
        reference_text = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)  # Normalize text
        image_text_cache[img_file] = reference_text

def populate_image_ui_cache(image_folder):
    global image_ui_cache
    for img_file in os.listdir(image_folder):
        reference_image_path = os.path.join(image_folder, img_file)
        reference_text = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)  # Normalize text
        image_ui_cache[img_file] = reference_text

# Function to compare text with cached OCR data
def compare_text_with_cache(target_image_path):
    matches = []
    for img_file, reference_text in image_text_cache.items():
        if search_image(reference_text , target_image_path):
            matches.append(img_file)
            break
    return matches

# Function to reconnect to a specific ADB device
def adb_reconnect(device_serial):
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        device = client.device(device_serial)
        
        if device:
            device.disconnect()
            device.connect()
            return True
        else:
            print(f"Device {device_serial} not found.")
            return False
    except Exception as e:
        print(f"Failed to reconnect to device {device_serial}: {e}")
        return False

def search_image(query_image_path , target_image_path):
        query_image = query_image_path
        target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)

        # Perform template matching
        result = cv2.matchTemplate(target_image, query_image, cv2.TM_CCOEFF_NORMED)

        # Define a threshold
        threshold = 0.8  # Adjust this value based on your needs

        # Find locations in the result that exceed the threshold
        locations = cv2.minMaxLoc(result)
        max_val = locations[1]

        # Check if the maximum value exceeds the threshold
        if max_val >= threshold:
                return True
        else:
                return False

def has_20_seconds_passed(file_name, json_file , flag):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            if file_name in data:
                logged_time = data[file_name]
                current_time = time.time()
                if (current_time - logged_time) >= checkAxUITime or flag:
                    # Remove the entry from the JSON file
                    del data[file_name]
                    with open(json_file, 'w') as f:
                        json.dump(data, f, indent=4)
                    return True
                else:
                    return False
            else:
                return False
    except FileNotFoundError:
        return False

def log_unprocessed_file(file_name, json_file):
    data = {}
    current_time = time.time()
    
    # Read existing data if the JSON file exists
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        pass

    # Add or update the entry
    data[file_name] = current_time

    # Write data back to the JSON file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def check_exist(file_name, json_file):
        try:
                with open(json_file, 'r') as f:
                        data = json.load(f)
                        if file_name not in data:
                                log_unprocessed_file(file_name, json_file)
        except FileNotFoundError:
                # Log the unprocessed file if the JSON file does not exist
                log_unprocessed_file(file_name, json_file)

def checkAxUIRunning(adb_device,target_image_path):
    if search_image(robloxui,target_image_path):
            state = False
            for img_file, reference_text in image_ui_cache.items():
                xxx = search_image(reference_text,target_image_path)
                if xxx:
                    state = True
                    break

            if not state:
                    print(f"Device {adb_device.serial}: Executor UI didn't popup. Recheck..")
                    check_exist(target_image_path, json_file)
                    if has_20_seconds_passed(target_image_path, json_file,False):
                            return False
            else:
                has_20_seconds_passed(target_image_path, json_file,True)
                if AD:
                    return checkGuiAdk(adb_device,target_image_path)

    return True

def checkGuiAdk(adb_device,target_image_path):
    nameCheckGuiAdk = f"{target_image_path}adk"
    if not search_image(guiadk,target_image_path):
        print(f"Device {adb_device.serial}: ADK didn't popup. Recheck..")
        check_exist(nameCheckGuiAdk, json_file)
        if has_20_seconds_passed(nameCheckGuiAdk, json_file,False):
            return False
    else:
        has_20_seconds_passed(nameCheckGuiAdk, json_file,True)
    
    return True

def running_process(adb_device):
    try:
        if not is_app_running(adb_device, PACKAGE_NAME):
            print(f"Device {adb_device.serial}: Client is not running. Joining {STATE_JOINING}")
            launch_app(adb_device, STATE_JOINING)
        else:
            print(f"Device {adb_device.serial}: Client is running.")
            if is_activity_in_foreground(adb_device, PACKAGE_NAME, TARGET_ACTIVITY):
                capture_screenshot(adb_device)
                captured_text = f"{LOCAL_SCREENSHOT_PATH}{adb_device.serial.split(":")[1]}{NAME_SCREENSHOT}"
                matches = compare_text_with_cache(captured_text)

                if matches:
                    print(f"Device {adb_device.serial}: Close Client:", matches)
                    stop_app(adb_device, PACKAGE_NAME)
                    launch_app(adb_device, STATE_JOINING)
                elif not checkAxUIRunning(adb_device,f"{LOCAL_SCREENSHOT_PATH}{adb_device.serial.split(":")[1]}{NAME_SCREENSHOT}"):
                    print(f"Device {adb_device.serial}: AX UI is not running on {checkAxUITime} second. Close Client")
                    stop_app(adb_device, PACKAGE_NAME)
                    launch_app(adb_device, STATE_JOINING)
            else:
                if not is_activity_splash(adb_device, PACKAGE_NAME):
                    print(f"Device {adb_device.serial}: Activity is not in the foreground.")
                    stop_app(adb_device, PACKAGE_NAME)
                    launch_app(adb_device, STATE_JOINING)
    except RuntimeError as e:
        print(f"Device {adb_device.serial}: Offline")
        successful_reconnect = adb_reconnect(adb_device.serial)

        if successful_reconnect:
            # Reinitialize the devices list if necessary
            try:
                devices = adb_client.devices()[start_index:end_index + 1]
            except Exception as e:
                return True
        else:
            print(f"Device {adb_device.serial}: Could not reconnect.")

if emulator_mode == '2':
    start_index = int(config['emulator']['startEmu1'])
    end_index = int(config['emulator']['endEmu1'])
    if privateLink  != "":
        privateLink = config["privateLink1"]
elif emulator_mode == '3':
    start_index = int(config['emulator']['startEmu2'])
    end_index = int(config['emulator']['endEmu2'])
    if privateLink  != "":
        privateLink = config["privateLink2"]
else:
    # If mode is not '2' or '3', default to the whole list
    start_index = 0
    end_index = 9999
# ADB Client
adb_client = AdbClient(host="127.0.0.1", port=5037)
devices = adb_client.devices()
if not devices:
    raise RuntimeError("No devices connected. Check ADB setup and device connection.")

devices = devices[start_index:end_index + 1]

populate_image_text_cache(IMG_FOLDER)
populate_image_ui_cache(IMG_UI_FOLDER)

start_time = time.time()
discord_hook_time = start_time
hookDiscord()

try:
    # Main monitoring loop
    while True:

        elapsed_time = time.time() - start_time
        elapsed_time_discord_hook = time.time() - discord_hook_time
        if enabledDiscord and elapsed_time_discord_hook > timeDiscord*60:
            discord_hook_time = time.time()
            hookDiscord()

        if autoClose and elapsed_time > autoCloseTime:
            start_time = time.time()
            for adb_device in devices:
                try:
                    stop_app(adb_device, PACKAGE_NAME)
                    print(f"Device {adb_device.serial}: Restart Client after {autoCloseTime/60} Minute.")
                except Exception as e:
                    print(f"Device {adb_device.serial}: Offline")
                time.sleep(CHECK_INTERVAL)

        for adb_device in devices:               
            running_process(adb_device)
            time.sleep(CHECK_INTERVAL)  # Wait before checking again
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")