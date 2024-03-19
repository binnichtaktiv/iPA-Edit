import os 
import sys
import zipfile 
import plistlib 
import shutil
import subprocess
import time
import patoolib
import requests

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

print("\n[0] download iPAs via direct URL")
print("[1] change Bundle-ID") 
print("[2] change App-Name") 
print("[3] change App-Version") 
print("[4] change App-Icon & App-Name")
print("[5] change App Icon")
print("[6] inject Satella Jailed")
print("[7] export .dylib(s) of an iPA")
print("[8] change .dylib dependency")
print("[9] add your cracker name to a iPA (hidden)")
print("[10] sign and upload every iPA in a folder (paid/free certificate)")
print("[11] .deb to .iPA (can create an .iPA from a .deb")
print("[12] enable file sharing")

option = input("Choose an option: \n")
if not option.isdigit() or not (0 <= int(option) <= 15):
    print("Invalid input. Try again.")
    sys.exit()
option = int(option)
clear_terminal() 

from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

if option == 0:
    url = input("Enter a direct download URL: ")
    clear_terminal()
    filename = input("Enter a name for the downloaded file: ")
    clear_terminal()

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    downloaded_size = 0

    with open(filename, "wb") as f, tqdm(
        desc=f"Downloading {filename}",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(block_size):
            downloaded_size += len(data)
            f.write(data)
            pbar.update(len(data))

    if total_size != 0 and downloaded_size != total_size:
        print("Failed to download.")
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

if option == 2: 

    ipa_path = input("Please enter the path to the IPA file:\n")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)

    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
        pl = plistlib.load(fp) 

    if 'CFBundleDisplayName' in pl:
        app_display_name = pl['CFBundleDisplayName']
    else:
        app_display_name = pl.get('CFBundleName')

    print("Current App-Name: ", app_display_name)

    new_display_name = input("Please enter your new App-Name: \n")
    clear_terminal() 
    if 'CFBundleDisplayName' in pl:
            pl['CFBundleDisplayName'] = new_display_name 
    else:
        pl['CFBundleName'] = new_display_name 

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
    print("The Bundle ID and App Icon were changed successfully.")

if option == 5:

    ipa_path = input("Please enter the path to the IPA file:\n")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)

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

    zip_ipa(ipa_path, app_path, file_name_no_ipa)
    clear_terminal()
    print("App Icon was changed successfully.")

filename = " "
import tempfile

if option == 6:
    temp_folder = tempfile.mkdtemp()
    filename = os.path.join(temp_folder, "SatellaJailed.dylib")
    satella_url = "https://github.com/Paisseon/SatellaJailed/raw/emt/SatellaJailed.dylib"
    response = requests.get(satella_url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    program = "pyzule"
    try:
        result = subprocess.run([program, "-h"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            satella_jailed_folder = temp_folder
            ipa_path = input("Enter the path of the .iPA you want to inject Satella to:\n")
            clear_terminal()
            ipa_fname = os.path.splitext(os.path.basename(ipa_path))[0]
            
            output_dir = input(f"Enter an output path for your new patched iPA:\n")
            real_output_dir = os.path.join(output_dir, ipa_fname + "_satella")
            
            clear_terminal()
            inj_satella = subprocess.run(["pyzule", "-o", real_output_dir, "-i", ipa_path, "-f", filename, "-c", "9"])
            print("Patching.... Please wait. It may take a while depending on the file size\n")
            clear_terminal()
            print(".iPA file with Satella injected should be here: " + output_dir)
        else:
            print("pyzule is not installed! Install it first. https://github.com/asdfzxcvbn/pyzule")
    except FileNotFoundError:
        print("pyzule is not installed! Install it first. https://github.com/asdfzxcvbn/pyzule")

    shutil.rmtree(temp_folder)


if option == 7:

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
        
        os.rename(zip_path, zip_path.replace(".zip", ".ipa"))
        
        if os.path.exists(payload_path):
            shutil.rmtree(payload_path)
        
        sys.exit()

    print('found .dylibs:')
    for index, file in enumerate(dylib_files, start=1):
        print(f'{index}: {os.path.basename(file)}')

    print("Enter 'exit' to exit without exporting.")
    selected_files = input('Enter the numbers of the files to be exported separated by commas:\n')

    if selected_files.strip().lower() == 'exit':
        
        os.rename(zip_path, zip_path.replace(".zip", ".ipa"))
        
        if os.path.exists(payload_path):
            shutil.rmtree(payload_path)
        
        sys.exit()

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
    
    os.rename(zip_path, zip_path.replace(".zip", ".ipa"))
    
    if os.path.exists(payload_path):
        shutil.rmtree(payload_path)


if option == 8:

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

if option == 9:
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


if option == 10:

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

        subprocess.run(command, shell=True, check=True)

    print("All .ipa files have been processed!")

if option == 11:
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

    apps_folder = os.path.join(deb_tmp, "Applications")
    if os.path.exists(apps_folder) and os.path.isdir(apps_folder):
        found_app_folder = False

        for folder_name in os.listdir(apps_folder):
            if folder_name.endswith('.app'):
                found_app_folder = True
                app_name = folder_name[:-4]                
                app_folder_path = os.path.join(apps_folder, folder_name)
                payload_folder_path = os.path.join(deb_tmp, "Payload")
                os.makedirs(payload_folder_path, exist_ok=True)
                shutil.copytree(app_folder_path, os.path.join(payload_folder_path, folder_name))
                zip_filename = payload_folder_path + '.zip'

                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(payload_folder_path):
                        for file in files:
                            absolute_file_path = os.path.join(root, file)
                            zipf.write(absolute_file_path, os.path.relpath(absolute_file_path, deb_tmp))

                os.replace(zip_filename, os.path.join(output_dir, app_name + '.ipa'))
                shutil.rmtree(deb_tmp)
                clear_terminal()
                print(f"'{folder_name}' has been zipped as '{app_name}.ipa' in the directory '{output_dir}'")

        if not found_app_folder:
            print("No '.app' folder found in the specified directory.")

    else:
        print("The specified path does not exist or is not a directory.")

        
if option == 12:
    
    ipa_path = input("Please enter the path to the IPA file:\n")
    clear_terminal()
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(ipa_path)

    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
        pl = plistlib.load(fp) 

    pl['LSSupportsOpeningDocumentsInPlace'] = True
    pl['UIFileSharingEnabled'] = True

    with open(info_plist_path, 'wb') as fp: 
        plistlib.dump(pl, fp) 

    zip_ipa(ipa_path, app_path, file_name_no_ipa, payload_path)
    clear_terminal()
    print("The App Name was changed successfully.")
