import os 
import sys
import zipfile 
import plistlib 
import shutil
import pickle
import subprocess
import time
import json
import patoolib
import requests
import shlex

payload_name = "Payload.zip" 
filename = 'variable.pkl'
data_file_path = "list_data.json"
sideload_detection_paths = 'sideload_detection_paths.pkl'


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def download_file(url, directory=None, new_filename="sideloadbypass1"):
    print("Please wait. Sideload detections are downloading...")
    if directory is None:
        directory = os.getcwd()

    directory = os.path.join(directory, "sideloadbypasses")
    os.makedirs(directory, exist_ok=True)
    filename = new_filename
    file_path = os.path.join(directory, filename)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    new_file_path = f"{file_path}.dylib"
    os.rename(file_path, new_file_path)
    clear_terminal()
    print(f"{filename}.dylib downloaded sucessfully and saved in {directory}")
    return new_file_path


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
        sys.exit()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_path))

    payload_path = os.path.join(os.path.dirname(zip_path), "Payload")

    app_folder = None
    for item in os.listdir(payload_path):
        if item.endswith(".app"):
            app_folder = item
            break

    if app_folder is None:
        print("App folder not found. Try it again...")
        sys.exit()

    app_path = os.path.join(payload_path, app_folder)
    return app_path, file_name_no_ipa, zip_path, payload_path

                                                                                #zip iPA

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
    shutil.rmtree(payload_path)
    os.remove(zip_path)

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
print("[10] export .dylib(s) of an iPA")
print("[11] change .dylib dependency")
print("[12] add your cracker name to a iPA (hidden)")
print("[13] sign and upload every iPA in a folder (paid/free certificate)")
print("[14] .deb to .iPA (can create an .iPA from a .deb")

option = int(input("Choose an option: \n"))
clear_terminal() 

if option == 0:
    url = input("enter a direct download URL: ")
    clear_terminal()
    filename = input("enter a name for the downloaded file:")
    clear_terminal()

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    downloaded_size = 0

    with open(filename, "wb") as f:
        for data in response.iter_content(block_size):
            downloaded_size += len(data)
            f.write(data)
            progress = downloaded_size / total_size * 100
            print(f"Download progres: {progress:.2f}%", end="\r")

    if total_size != 0 and downloaded_size != total_size:
        print("failed to download.")
    else:
        print(f"{filename} was downloaded successfully.")

if option == 1: 

    ipa_path = input("Please enter the path to the IPA file:\n")
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
    print("Patching.... Please wait. It may take a while depending on the file size")

    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 

    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("The Bundle ID was changed successfully.")

    #shutil.rmtree()

if option == 2: 

    ipa_path = input("Please enter the path to the IPA file:\n")
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
    print("Patching.... Please wait. It may take a while depending on the file size")

    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 

    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("The App Name was changed successfully.")

if option == 3:

    ipa_path = input("Please enter the path to the IPA file:\n")
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
    print("Patching.... Please wait. It may take a while depending on the file size") 

    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 

    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)

    print("The App Version was changed successfully.")

if option == 4:
    ipa_path = input("Please enter the path to the IPA file:\n")
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
    print("Patching.... Please wait. It may take a while depending on the file size") 

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

if option == 5:

    ipa_path = input("Please enter the path to the IPA file:\n")
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
    print("Patching.... Please wait. It may take a while depending on the file size") 

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
    program = "azule"
    try:
        result = subprocess.run([program, "-h"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            try:
                with open(filename, 'rb') as f:
                    satella_jailed_folder = pickle.load(f)
            except FileNotFoundError:
                satella_jailed_folder = input("Enter the folder where Satella Jailed was downloaded: \n")
                clear_terminal()
                with open(filename, 'wb') as f:
                    pickle.dump(satella_jailed_folder, f)
                print("Created permanent variable for your Satella path.\n")
                time.sleep(4)
                clear_terminal()

            ipa_path = input("Enter the path of the .iPA you want to inject Satella to: \n")
            clear_terminal()
            shutil.copy(ipa_path, satella_jailed_folder)
            os.chdir(satella_jailed_folder)
            patchsh_path = satella_jailed_folder + "/patch.sh"
            print("Patching.... Please wait. It may take a while depending on the file size\n")
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
        else:
            print("Azule is not installed! Install it first. https://github.com/Al4ise/Azule")
    except FileNotFoundError:
        print("Azule is not installed! Install it first. https://github.com/Al4ise/Azule")


if option == 7:
    program = "azule"
    try:
        result = subprocess.run([program, "-h"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            try:
                with open('sideload_detection_paths.pkl', 'rb') as f:
                    sideload_detection_paths = pickle.load(f)
            except FileNotFoundError:
                url1 = "https://github.com/binnichtaktiv/iPA-Edit/raw/main/bypasses/Sideloadbypass1.dylib"
                sideload_bypass1 = download_file(url1, new_filename="sideloadbypass1")

                url2 = "https://github.com/binnichtaktiv/iPA-Edit/raw/main/bypasses/Sideloadbypass2.dylib"
                sideload_bypass2 = download_file(url2, new_filename="sideloadbypass2")

                url3 = "https://github.com/binnichtaktiv/iPA-Edit/raw/main/bypasses/SideloadSpoofer-08.dylib"
                sideloadly_bypass = download_file(url3, new_filename="sideloadlybypass")

                sideload_detection_paths = {'sideload_bypass1': sideload_bypass1,
                                            'sideload_bypass2': sideload_bypass2,
                                            'sideloadly_bypass': sideloadly_bypass}
                with open('sideload_detection_paths.pkl', 'wb') as f:
                    pickle.dump(sideload_detection_paths, f)

                clear_terminal()
                print("Permanently saved the paths to the sideload detection bypass .dylibs so you don't have to enter them everytime..")
                time.sleep(3)
                clear_terminal()

            sideload_bypass1 = sideload_detection_paths.get('sideload_bypass1')
            sideload_bypass2 = sideload_detection_paths.get('sideload_bypass2')
            sideloadly_bypass = sideload_detection_paths.get('sideloadly_bypass')

            sideload_detection_bypass_ipa = input("Enter the path to the iPA where you want to bypass the sideload detection:\n")
            clear_terminal()
            sideload_detection_bypass_ipa_output = input("Enter an output path:\n")
            clear_terminal()
            sideload_detection_bypass_ipa_output_name = input("Enter a name for the patched iPA:\n")
            clear_terminal()

            bypass_selection = int(input("Which bypass do you want to use?\n[1] Sideloadbypass1 & Sideloadbypass2 \n[2] SideloadDetection-05/6\n[3] Sideloadbypass1 & Sideloadbypass2 & Sideloadly Bypass\n"))
            clear_terminal()

            if bypass_selection == 1:
                azule_cmd_prep = sideload_bypass1 + " " + sideload_bypass2
                azule_cmd = f"azule -o '{sideload_detection_bypass_ipa_output}' -i '{sideload_detection_bypass_ipa}' -f {azule_cmd_prep} -z -n {sideload_detection_bypass_ipa_output_name}"
                subprocess.run(azule_cmd, shell=True, check=True)
                clear_terminal()
                print("Modified .iPA should be here:" + sideload_detection_bypass_ipa_output)

            elif bypass_selection == 2:
                azule_cmd = f"azule -o '{sideload_detection_bypass_ipa_output}' -i '{sideload_detection_bypass_ipa}' -f {sideloadly_bypass} -z -n {sideload_detection_bypass_ipa_output_name}"
                subprocess.run(azule_cmd, shell=True, check=True)
                clear_terminal()
                print("Modified .iPA should be here: " + sideload_detection_bypass_ipa_output)

            elif bypass_selection == 3: 
                azule_cmd_prep = sideload_bypass1 + " " + sideload_bypass2 + " " + sideloadly_bypass
                azule_cmd = f"azule -o '{sideload_detection_bypass_ipa_output}' -i '{sideload_detection_bypass_ipa}' -f {azule_cmd_prep} -z -n {sideload_detection_bypass_ipa_output_name}"
                subprocess.run(azule_cmd, shell=True, check=True)
                clear_terminal()
                print("Modified .iPA should be here: " + sideload_detection_bypass_ipa_output)

            else:
                print("Not a valid option... Try again")
                sys.exit()
        else:
            print("Azule is not installed! Install it first. https://github.com/Al4ise/Azule")
    except FileNotFoundError:
        print("Azule is not installed! Install it first. https://github.com/Al4ise/Azule")

if option == 8:
    program = "azule"
    try:
        result = subprocess.run([program, "-h"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            azule_ipa_input = input("Enter the path to the iPA you want to inject debs into: \n")
            clear_terminal()
            if os.path.isfile(azule_ipa_input):
                print(".iPA file exists.\n\n")
                time.sleep(4)
                clear_terminal()
            else:
                print("Couldnt find .iPA file. Try again.")
                sys.exit()

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

            subprocess.run(terminal_command, shell=True, check=True)
            clear_terminal()
            print("Modified .iPA should be here:" + azule_ipa_output)
        else:
            print("Azule is not installed! Install it first. https://github.com/Al4ise/Azule")
    except FileNotFoundError:
        print("Azule is not installed! Install it first. https://github.com/Al4ise/Azule")


if option == 9:
    data_file_path = "azulelist_data.json"
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
            sys.exit()

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
    output_path_azulelist = input("Enter a output path: \n")
    clear_terminal()

    debs_paths_str = ' '.join(item['debs_path'])
    command = f"azule -o '{output_path_azulelist}' -i '{ipa_path_for_azulelist}' -f {debs_paths_str} -z -n {new_ipa_name}"
    os.system(command)
    print("App was patched successfully.")

if option == 10:


    ipa_path = input("Please enter the path to the IPA file:\n")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)

    dylib_files = []
    for root, _, files in os.walk(app_path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))

    if not dylib_files:
        print("Error: No .dylib files found in the IPA file.")
        sys.exit()

    print('found .dylibs:')
    for index, file in enumerate(dylib_files, start=1):
        print(f'{index}: {os.path.basename(file)}')

    #clear_terminal()
    selected_files = input('Enter the numbers of the files to be exported separated by commas:')
    clear_terminal()
    selected_indices = [int(num.strip()) - 1 for num in selected_files.split(',')]
    selected_dylib_files = [dylib_files[index] for index in selected_indices]

    export_path = input('Enter a output path\n: ')
    clear_terminal()
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    for file in selected_dylib_files:
        shutil.copy(file, export_path)

    print('Exported .dylibs successfully')        

if option == 11:

    file_path = input("Enter path to .dylib: ")

    if file_path.endswith(".deb"):
        print("You have to extract the .deb! Extract it and try with the .dylib again")
        sys.exit()

    if file_path.endswith(".dylib"):
        clear_terminal()
        dep_option = int(input("What do you want to change? \n [1] @rpath/CydiaSubstrate.framework/CydiaSubstrate \n [2] other dependency \n"))

        if dep_option == 1:
            clear_terminal()
            old_word = "@rpath/CydiaSubstrate.framework/CydiaSubstrate"

            with open(file_path, 'rb') as file:
                content = file.read()

            index = content.find(old_word.encode())

            while index != -1:
                new_word = input("Enter new value for '{}' : ".format(old_word))
                content = content[:index] + new_word.encode() + content[index+len(old_word.encode()):]
                index = content.find(old_word.encode(), index + len(new_word.encode()))

                with open(file_path, 'wb') as file:
                    file.write(content)
            clear_terminal()
            print("Changed dependency successfully.")
        else:
            clear_terminal()
            old_word = input("Enter the path of the dependency you want to change\n Example: '@executable_path/tweak.dylib' \n")
            with open(file_path, 'rb') as file:
                content = file.read()

            index = content.find(old_word.encode())
            clear_terminal()
            new_word = input("Enter new value for '{}' : ".format(old_word))

            while index != -1:

                content = content[:index] + new_word.encode() + content[index+len(old_word.encode()):]
                index = content.find(old_word.encode(), index + len(new_word.encode()))

                with open(file_path, 'wb') as file:
                    file.write(content)
            clear_terminal()
            print("Changed dependency successfully.")

    else:
        print("This is not a .dylib file! Try again")
        sys.exit()

if option == 12:
    ipa_path = input("Please enter the path to the IPA file:\n")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)

    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 

    cracked_by = input("Please enter your cracker name: \n")
    clear_terminal()
    pl['cracked_by'] = cracked_by

    print("Patching.... Please wait. It may take a while depending on the file size")
    clear_terminal()

    with open(info_plist_path, 'wb') as fp: 
        plistlib.dump(pl, fp) 

    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("Cracker name entry added")


if option == 13:

    zsign_path = input("Enter the path to the zsign executable:\n")
    p12_path = input("Enter the path to the .p12 file:\n")
    mobileprovision_path = input("Enter the path to the .mobileprovision file:\n")
    password = input("Enter the password for the .p12 file:\n")
    directory_path = input("Enter the directory containing the .ipa files:\n")
    compression_level = 9

    signed_directory = os.path.join(directory_path, 'signed')
    if not os.path.exists(signed_directory):
        os.makedirs(signed_directory)

    files = os.listdir(directory_path)

    ipa_files = [f for f in files if f.endswith('.ipa')]

    for ipa_file in ipa_files:
        ipa_path = os.path.join(directory_path, ipa_file)
        output_file_name = os.path.splitext(ipa_file)[0] + '_signed.ipa'
        output_path = os.path.join(signed_directory, output_file_name)

        command = f'{zsign_path} -k "{p12_path}" -m "{mobileprovision_path}" -p "{password}" -o "{output_path}" -z {compression_level} "{ipa_path}"'

        subprocess.run(command, shell=True)

    print("All .ipa files have been processed!")


if option == 14:

    deb_to_ipa = input("Enter the .deb path:\n")
    clear_terminal()
    output_dir = input("Enter an output path for your new iPA:\n")
    clear_terminal()
    deb_tmp = os.path.join(output_dir, "deb_tmp")
    print("Patching.... Please wait. It may take a while depending on the file size")

    if not os.path.exists(deb_tmp):
        os.makedirs(deb_tmp)

    file_path = deb_to_ipa.strip()

    patoolib.extract_archive(file_path, outdir=deb_tmp, verbosity=-1)
    data_tar_file = None

    for file in os.listdir(deb_tmp):
        if file.startswith("data.tar"):
            data_tar_file = os.path.join(deb_tmp, file)
            break

    if data_tar_file:
        patoolib.extract_archive(data_tar_file, outdir=deb_tmp, verbosity=-1)
        os.remove(data_tar_file)

    clear_terminal()

    apps_folder = os.path.join(deb_tmp, "Applications")
    if os.path.exists(apps_folder) and os.path.isdir(apps_folder):
        found_app_folder = False

        for folder_name in os.listdir(apps_folder):
            if folder_name.endswith('.app'):
                found_app_folder = True
                app_name = folder_name[:-4]                
                app_folder_path = os.path.join(apps_folder, folder_name)
                zip_filename = app_folder_path + '.zip'

                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(app_folder_path):
                        for file in files:
                            absolute_file_path = os.path.join(root, file)
                            zipf.write(absolute_file_path, os.path.relpath(absolute_file_path, apps_folder))

                os.replace(zip_filename, os.path.join(output_dir, app_name + '.ipa'))
                shutil.rmtree(deb_tmp)
                clear_terminal()
                print(f"'{folder_name}' has been zipped as '{app_name}.ipa' in the directory '{output_dir}'")

        if not found_app_folder:
            print("No '.app' folder found in the specified directory.")

    else:
        print("The specified path does not exist or is not a directory.")



if option >= 15:
    print("Not a valid option. Try again.")
    sys.exit()
