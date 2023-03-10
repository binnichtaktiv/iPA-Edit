import os 
import zipfile 
import plistlib 
import shutil
import pickle
import subprocess
import time
import json
import requests
 
payload_name = "Payload.zip" 
filename = 'variable.pkl'
data_file_path = "list_data.json"
sideload_detection_paths = 'sideload_detection_paths.pkl'


def clear_terminal():
    if os.name == 'nt': # Windows
        os.system('cls')
    elif os.name == 'posix': # MacOS oder Linux
        os.system('clear')
        
                                                                                #unzip iPA
def unzip_ipa(ipa_path):
    clear_terminal()
    file_name_no_ipa = os.path.basename(ipa_path)[:-4]
    zip_path = ipa_path.replace(".ipa", ".zip")

    if os.path.exists(ipa_path):
        os.rename(ipa_path, zip_path)
        print("iPA file successfully renamed to .Zip")
        time.sleep(1)
        clear_terminal()
    else:
        print("The .iPA file could not be found. Try again...")
        exit()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_path))

    payload_path = os.path.join(os.path.dirname(zip_path), "Payload")
    app_folder = os.listdir(payload_path)[0]
    app_path = os.path.join(payload_path, app_folder)
    return app_path, file_name_no_ipa, zip_path, payload_path

def zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path):
    payload_path2 = payload_path
    
    if os.path.basename(payload_path2) == "Payload":
        output_path = payload_path2[:len(payload_path2)-len("/Payload")]
    else:
        output_path = os.path.dirname(payload_path2)
 
    output_path = os.path.join(output_path) 
    with zipfile.ZipFile(os.path.join(output_path, "Payload.zip"), 'w', zipfile.ZIP_DEFLATED) as zip_file:  
       for root, dirs, files in os.walk(payload_path): 
           for file in files: 
               file_path = os.path.join(root, file) 
               zip_file.write(file_path, file_path.replace(payload_path, "Payload")) 
                
    clear_terminal()           
    user_new_ipa_name = input(f"enter a new name for your edited .ipa (without the .ipa at the end) \noriginal .ipa name: {file_name_no_ipa}'\n") 
    clear_terminal()
    user_new_ipa_name = user_new_ipa_name.strip() + ".ipa"
    os.rename(os.path.join(output_path, "Payload.zip"), user_new_ipa_name) 
    edited_file_path = os.path.join(output_path, user_new_ipa_name)
    os.replace(user_new_ipa_name, edited_file_path)

                                                                                            #start
                                                                                            
print("\n[0] download iPAs via direct URL")
print("[1] change Bundle-ID") 
print("[2] change App-Name") 
print("[3] change App-Version") 
print("[4] change App-Icon & App-Name")
print("[5] change App Icon")
print("[6] inject Satella Jailed")
print("[7] inject Sideload Detection Bypass ")
print("[8] inject .debs/.dylibs")
print("[9] update modded apps")
 
option = int(input("Choose an option: \n"))
clear_terminal() 
 
if option == 1: 
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)
 
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_bundle_id = pl['CFBundleIdentifier'] 
    print("Current Bundle-ID: ", old_bundle_id) 
 
    new_bundle_id = input("\nPlease enter your new Bundle-ID: \n") 
    clear_terminal()
    pl['CFBundleIdentifier'] = new_bundle_id
    print("Patching.... Pls wait")
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
    
    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("The Bundle ID was changed successfully.")
 
if option == 2: 
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)
    
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_display_name = pl['CFBundleDisplayName'] 
    print("Current App-Name: ", old_display_name) 
 
    new_display_name = input("Please enter your new App-Name: \n")
    clear_terminal() 
    pl['CFBundleDisplayName'] = new_display_name 
    print("Patching.... Pls wait")
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
         
    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("The App Name was changed successfully.")
    
if option == 3:
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)

    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_version = pl['CFBundleShortVersionString'] 
    print("\nCurrent App-Version: ", old_version) 
 
    new_version = input("\nPlease enter your new App-Version: \n")
    clear_terminal()
    pl['CFBundleShortVersionString'] = new_version
    print("Patching.... Pls wait") 
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
         
    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)

    print("The App Version was changed successfully.")
    
if option == 5:
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)
    
    directory = app_path # aktuellen ordner 
    for filename in os.listdir(directory): 
        if filename.startswith("AppIcon") and filename.endswith(".png"): 
            file_path = os.path.join(directory, filename) 
            try: 
                os.remove(file_path)
                clear_terminal()
                print(f"\nIcon '{filename}' deleted successfully.") 
                clear_terminal()
            except Exception as e: 
                print(f"\nError deleting file '{filename}': {e}") 
                 
    icon_path = input("Enter the path to the .png you want to use as App-Icon:\n")
    clear_terminal()
    print("Patching.... Pls wait") 
     
    with open(icon_path, 'rb') as fp:
        png_content = fp.read()

    for size in [(20, 20), (29, 29), (40, 40)]:
        filename = f"AppIcon{size[0]}x{size[1]}.png"
        target_path = os.path.join(app_path, filename)
        with open(target_path, 'wb') as fp:
            fp.write(png_content)

    plist_path = os.path.join(app_path, "Info.plist")
    
    #edit plist
    
    with open(plist_path, 'rb') as fp:
        plist = plistlib.load(fp)

    for key in list(plist.keys()):
        if 'Icon' in key:
            del plist[key]
            
    plist['CFBundleIconFiles'] = ['AppIcon20x20', 'AppIcon29x29', 'AppIcon40x40']

    with open(plist_path, 'wb') as fp:
        plistlib.dump(plist, fp)
        
    zip_ipa(ipa_path, app_path, file_name_no_ipa)
    clear_terminal()
    print("App Icon was changed successfully.")
    
if option == 6:

    try:
        with open(filename, 'rb') as f:
            satella_jailed_folder = pickle.load(f)
    except FileNotFoundError:
        satella_jailed_folder = input("Enter the folder where Satella Jailed was downloaded: \n")
        clear_terminal()
        with open(filename, 'wb') as f:
            pickle.dump(satella_jailed_folder, f)
        print('Created permanent variable for your Satella path.\n')
        time.sleep(4)
        clear_terminal()

    ipa_path = input("Enter the path of the .iPA you want to inject Satella to: \n")
    clear_terminal()
    shutil.copy(ipa_path, satella_jailed_folder)
    os.chdir(satella_jailed_folder)
    patchsh_path = satella_jailed_folder + "/patch.sh"
    print("Patching.... Pls wait a few seconds\n")
    #subprocess.run("chmod +x " + patchsh_path)
    process = subprocess.Popen(['sh', 'patch.sh'], stdout=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    process.communicate()
    clear_terminal()
    print(".iPA file with Satella injected should be here: " + satella_jailed_folder)
    
if option == 8:
        
    azule_ipa_input = input("Enter the path to the iPA you want to inject debs into: \n")
    clear_terminal()
    if os.path.isfile(azule_ipa_input):
        print(".iPA file exists.\n\n")
        time.sleep(4)
        clear_terminal()
    else:
        print("Couldnt find .iPA file. Try again.")
        exit()
        
    azule_ipa_output = input("Enter the output path for your modified .iPA: \n")
    clear_terminal()
    azule_ipa_output_name = input("Enter new name for the modified .iPA (without the .iPA at the end)\n")
    clear_terminal()
    file_paths = []
    while True:
        path = input("Enter path of the deb you want to inject (type 'ready' if you are done) \n")
        if path == "done":
            break
        clear_terminal()
        file_paths.append(path)

    deb_paths = " ".join(file_paths)
    terminal_command = f"azule -o '{azule_ipa_output}' -i '{azule_ipa_input}' -f '{deb_paths}' -z -n '{azule_ipa_output_name}'"

    subprocess.run(terminal_command, shell=True)
    clear_terminal()
    print("Modified .iPA should be here:" + azule_ipa_output)
    
if option == 4:
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)
    
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_display_name = pl['CFBundleDisplayName'] 
    print("Current App-Name: ", old_display_name) 
 
    new_display_name = input("\nPlease enter your new App-Name: \n")
    clear_terminal() 
    pl['CFBundleDisplayName'] = new_display_name 
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp)
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
         
    directory = app_path  
    for filename in os.listdir(directory): 
        if filename.startswith("AppIcon") and filename.endswith(".png"): 
            file_path = os.path.join(directory, filename) 
            try: 
                os.remove(file_path)
                clear_terminal()
                print(f"\nIcon '{filename}' deleted successfully.") 
                clear_terminal()
            except Exception as e: 
                print(f"\nError deleting file '{filename}': {e}") 
                 
    icon_path = input("Enter the path to the .png you want to use as App-Icon:\n")
    clear_terminal()
    print("Patching.... Pls wait") 
     
    with open(icon_path, 'rb') as fp:
        png_content = fp.read()

    for size in [(20, 20), (29, 29), (40, 40)]:
        filename = f"AppIcon{size[0]}x{size[1]}.png"
        target_path = os.path.join(app_path, filename)
        with open(target_path, 'wb') as fp:
            fp.write(png_content)

    plist_path = os.path.join(app_path, "Info.plist")
    
    with open(plist_path, 'rb') as fp:
        plist = plistlib.load(fp)

    for key in list(plist.keys()):
        if 'Icon' in key:
            del plist[key]
            
    plist['CFBundleIconFiles'] = ['AppIcon20x20', 'AppIcon29x29', 'AppIcon40x40']

    with open(plist_path, 'wb') as fp:
        plistlib.dump(plist, fp)
        
    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("The App Icon was changed successfully.")
    
if option == 9:
    
    list_data = []
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as data_file:
            list_data = json.load(data_file)

    while True:
        action = input("What do you want to?\n [1] add a new app \n [2] remove an app \n [3] use an existing app \n [4] exit\n")
        clear_terminal()

        if action.lower() == "1":
            clear_terminal()
            name = input("Enter a name for the app you want to save the paths for: \n")
            clear_terminal()

            debs_paths = []
            while True:
                debs_path = input("Enter the deb path(s) for the new app, or type 'done' to finish: \n")
                if debs_path.lower() == "done":
                    clear_terminal()
                    break
                debs_paths.append(debs_path)
                clear_terminal()

            new_item = {
                "name": name,
                "debs_path": debs_paths,
            }
            list_data.append(new_item)
            with open(data_file_path, "w") as data_file:
                json.dump(list_data, data_file)

        elif action.lower() == "2":
            # Display list of items
            print("List of items:")
            for i, item in enumerate(list_data):
                print(f"{i}: {item['name']}")

            item_index = input("Enter the number of the app you want to remove: \n")
            clear_terminal()
            try:
                item_index = int(item_index)
                item = list_data[item_index]
                del list_data[item_index]
                print(f"App '{item['name']}' has been removed from the list.")
                clear_terminal()
            except:
                clear_terminal()
                print("Invalid input, please try again.")
                

            with open(data_file_path, "w") as data_file:
                json.dump(list_data, data_file)
                
        elif action.lower() == "4":
            exit()

        elif action.lower() == "3":
            print("List of items:")
            for i, item in enumerate(list_data):
                print(f"{i}: {item['name']}")

            item_index = input("Enter the number of the item you want to use: \n")
            clear_terminal()
            try:
                item_index = int(item_index)
                item = list_data[item_index]
                break
            except:
                clear_terminal()
                print("Invalid input, please try again.")

        else:
            clear_terminal()
            print("Invalid input, please try again.")

    ipa_path_for_azulelist = input("Enter the iPA path to the new iPA: \n")
    clear_terminal()
    new_ipa_name = input("Enter a name for the patched iPA: \n")
    clear_terminal()
    output_path_azulelist = input("Enter a output path: \n ")
    clear_terminal()

    debs_paths_str = ' '.join(item['debs_path'])
    command = f"azule -o '{output_path_azulelist}' -i '{ipa_path_for_azulelist}' -f {debs_paths_str} -z -n {new_ipa_name}"
    os.system(command)
    print("App was patched successfully.")

if option == 7:
    try:
        with open('sideload_detection_paths.pkl', 'rb') as f:
            sideload_detection_paths = pickle.load(f)

    except FileNotFoundError:
            
        sideload_bypass1 = input("Enter the path of 'Sideloadbypass1.dylib'\n")
        clear_terminal()
        sideload_bypass2 = input("Enter the path of 'Sideloadbypass2.dylib'\n")
        clear_terminal()
        sideloadly_bypass = input("Enter the path of 'SideloadDetection-05/6.dylib'\n")
        clear_terminal()
        sideload_detection_paths = {'sideload_bypass1': sideload_bypass1,
                                    'sideload_bypass2': sideload_bypass2,
                                    'sideloadly_bypass': sideloadly_bypass}
        with open('sideload_detection_paths.pkl', 'wb') as f:
            pickle.dump(sideload_detection_paths, f)    
                
            print("Permanently saved the paths to the sideload detection bypass .dylibs do you dont have to enter them everytime..")
            time.sleep(3)
            sideload_bypass1 = sideload_detection_paths.get('sideload_bypass1')
            sideload_bypass2 = sideload_detection_paths.get('sideload_bypass2')
            sideloadly_bypass = sideload_detection_paths.get('sideloadly_bypass')
        
    sideload_detection_bypass_ipa = input("Enter the path to the iPA where you want to bypass the sideload detection:\n")
    clear_terminal()
    sideload_detection_bypass_ipa_output = input("Enter a output path:\n")
    clear_terminal()
    sideload_detection_bypass_ipa_output_name = input("Enter a name for the patched iPA:\n")
    clear_terminal()
    
    bypass_selection = int(input("Which bypass do you want to use?\n[1] Sideloadbypass1 & Sideloadbypass2 \n[2] SideloadDetection-05/6\n"))
    clear_terminal()
    
    if bypass_selection == 1:
        azule_cmd_prep = sideload_bypass1 + " " + sideload_bypass2
        azule_cmd = f"azule -o '{sideload_detection_bypass_ipa_output}' -i '{sideload_detection_bypass_ipa}' -f {azule_cmd_prep} -z -n {sideload_detection_bypass_ipa_output_name}"
        subprocess.run(azule_cmd, shell=True)
        clear_terminal()
        print("modified .iPA should be here:" + sideload_detection_bypass_ipa_output)
        
    elif bypass_selection == 2:
        azule_cmd = f"azule -o '{sideload_detection_bypass_ipa_output}' -i '{sideload_detection_bypass_ipa}' -f {sideloadly_bypass} -z -n {sideload_detection_bypass_ipa_output_name}"
        subprocess.run(azule_cmd, shell=True)
        clear_terminal()
        print("modified .iPA should be here: " + sideload_detection_bypass_ipa_output)
        
    else:
        print("Not a valid option... Try again")
        exit()
        
if option == 0:
    url = input("enter a direct download URL: ")
    os.system('clear')
    filename = input("enter a name for the downloaded file:")
    os.system('clear')

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    downloaded_size = 0

    with open(filename, "wb") as f:
        for data in response.iter_content(block_size):
            downloaded_size += len(data)
            f.write(data)
            progress = downloaded_size / total_size * 100
            print(f"Download Fortschritt: {progress:.2f}%", end="\r")

    if total_size != 0 and downloaded_size != total_size:
        print("failed to download.")
    else:
        print(f"{filename} was downloaded successfully.")

    
    
    
if option > 9:
    print("Not a valid option. Try again.")
    exit()