import os 
import zipfile 
import plistlib 
import shutil
import pickle
import subprocess
import time
 
payload_name = "Payload.zip" 
filename = 'variable.pkl'


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
        time.sleep(3)
    else:
        print("The .iPA file could not be found. Try again...")
        exit()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(zip_path))

    payload_path = os.path.join(os.path.dirname(zip_path), "Payload")
    print(payload_path)
    app_folder = os.listdir(payload_path)[0]
    app_path = os.path.join(payload_path, app_folder)
    return app_path, file_name_no_ipa, zip_path
                                                                                #zip iPA
def zip_ipa(ipa_path, app_path, file_name_no_ipa):
    zip_path = ipa_path.replace(".ipa", ".zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(app_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, file_path.replace(app_path, ""))

    os.rename(zip_path, file_name_no_ipa + ".ipa")

                                                                                            #start
                                                                                            
print("[1] change Bundle-ID") 
print("[2] change App-Name") 
print("[3] change App-Version") 
print("[4] change App-Icon")
print("[5] inject Satella Jailed")
print("[6] inject .debs/.dylibs")
 
option = int(input("choose an option: \n"))
clear_terminal() 
 
if option == 1: 
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path = unzip_ipa(ipa_path)
 
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_bundle_id = pl['CFBundleIdentifier'] 
    print("current Bundle-ID: ", old_bundle_id) 
 
    new_bundle_id = input("\nplease enter your new Bundle-ID: \n") 
    clear_terminal()
    pl['CFBundleIdentifier'] = new_bundle_id
    print("Patching.... Pls wait")
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
    
    zip_ipa(ipa_path, app_path, file_name_no_ipa)
    clear_terminal()
    print("The Bundle ID was changed successfully.")
 
if option == 2: 
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path = unzip_ipa(ipa_path)
    
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_display_name = pl['CFBundleDisplayName'] 
    print("current App-Name: ", old_display_name) 
 
    new_display_name = input("please enter your new App-Name: \n")
    clear_terminal() 
    pl['CFBundleDisplayName'] = new_display_name 
    print("Patching.... Pls wait")
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
         
    zip_ipa(ipa_path, app_path, file_name_no_ipa)
    clear_terminal()
    print("The App Name was changed successfully.")
    
if option == 3:
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path = unzip_ipa(ipa_path)

    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_version = pl['CFBundleShortVersionString'] 
    print("\ncurrent App-Version: ", old_version) 
 
    new_version = input("\nplease enter your new App-Version: \n")
    clear_terminal()
    pl['CFBundleShortVersionString'] = new_version
    print("Patching.... Pls wait") 
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
         
    zip_ipa(ipa_path, app_path, file_name_no_ipa)

    print("The App Version was changed successfully.")
    
if option == 4:
    
    ipa_path = input("Please enter the path to the IPA file:\n ")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path = unzip_ipa(ipa_path)
    
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
    print("The App Icon was changed successfully.")
    
if option == 5:

    try:
        with open(filename, 'rb') as f:
            satella_jailed_folder = pickle.load(f)
    except FileNotFoundError:
        satella_jailed_folder = input("enter the folder where Satella Jailed was downloaded: \n")
        clear_terminal()
        with open(filename, 'wb') as f:
            pickle.dump(satella_jailed_folder, f)
        print('created permanent variable for your Satella path.\n')
        time.sleep(4)
        clear_terminal()

    ipa_path = input("enter the path of the .iPA you want to inject Satella to: \n")
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
    
if option == 6:
        
    azule_ipa_input = input("enter the path to the iPA you want to inject debs into: \n")
    clear_terminal()
    if os.path.isfile(azule_ipa_input):
        print(".iPA file exists.\n\n")
        time.sleep(4)
        clear_terminal()
    else:
        print("couldnt find .iPA file. Try again.")
        exit()
        
    azule_ipa_output = input("enter the output path for your modified .iPA: \n")
    clear_terminal()
    azule_ipa_output_name = input("enter new name for the modified .iPA (without the .iPA at the end)\n")
    clear_terminal()
    file_paths = []
    while True:
        path = input("enter path of the deb you want to inject (type 'ready' if you are done) \n")
        if path == "done":
            break
        clear_terminal()
        file_paths.append(path)

    deb_paths = " ".join(file_paths)
    terminal_command = f"azule -o '{azule_ipa_output}' -i '{azule_ipa_input}' -f '{deb_paths}' -z -n '{azule_ipa_output_name}'"

    subprocess.run(terminal_command, shell=True)
    clear_terminal()
    print("modified .iPA should be here:" + azule_ipa_output)
    
if option > 6:
    print("not a valid option. Try again.")
    exit()