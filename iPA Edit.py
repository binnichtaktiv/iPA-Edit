import os 
import zipfile 
import plistlib 
import shutil
 
payload_name = "Payload.zip" 

def make_zip():
    gh
 
def bundleID(): 
     
 
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: 
        zip_ref.extractall(os.path.dirname(zip_path)) 
 
    payload_path = os.path.join(os.path.dirname(zip_path), "Payload") 
    print(payload_path) 
    app_folder = os.listdir(payload_path)[0] 
    app_path = os.path.join(payload_path, app_folder) 
 
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_bundle_id = pl['CFBundleIdentifier'] 
    print("current Bundle-ID: ", old_bundle_id) 
 
    new_bundle_id = input("please enter your new Bundle-ID:") 
    pl['CFBundleIdentifier'] = new_bundle_id 
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
 
         
    shutil.make_archive(payload_path, "zip", root_dir=payload_path) 
         
    os.rename("Payload.zip", file_name) 
    os.remove(zip_path) 
    shutil.rmtree(payload_path) 
 
    print("The bundle ID was changed successfully.") 
 
def changeName(): 
 
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: 
        zip_ref.extractall(os.path.dirname(zip_path)) 
 
    payload_path = os.path.join(os.path.dirname(zip_path), "Payload") 
    print(payload_path) 
    app_folder = os.listdir(payload_path)[0] 
    app_path = os.path.join(payload_path, app_folder) 
 
    info_plist_path = os.path.join(app_path, "Info.plist") 
    with open(info_plist_path, 'rb') as fp: 
            pl = plistlib.load(fp) 
 
    old_display_name = pl['CFBundleDisplayName'] 
    print("current App-Name: ", old_display_name) 
 
    new_display_name = input("please enter your new App-Name: ") 
    pl['CFBundleDisplayName'] = new_display_name 
 
    with open(info_plist_path, 'wb') as fp: 
         plistlib.dump(pl, fp) 
 
         
    shutil.make_archive(payload_path, "zip", root_dir=payload_path) 
         
    os.rename("Payload.zip", file_name) 
    os.remove(zip_path) 
    shutil.rmtree(payload_path) 
 
    print("The App-Name was changed successfully.") 
 
def changeIcon(): 
     
    with zipfile.ZipFile(zip_path, 'r') as zip_ref: 
        zip_ref.extractall(os.path.dirname(zip_path)) 
 
    payload_path = os.path.join(os.path.dirname(zip_path), "Payload") 
    print(payload_path) 
    app_folder = os.listdir(payload_path)[0] 
    app_path = os.path.join(payload_path, app_folder) 
 
    directory = app_path # aktuellen ordner 
    for filename in os.listdir(directory): 
        if filename.startswith("AppIcon") and filename.endswith(".png"): 
            file_path = os.path.join(directory, filename) 
            try: 
                os.remove(file_path) 
                print(f"icon '{filename}' deleted successfully.") 
            except Exception as e: 
                print(f"Error deleting file '{filename}': {e}") 
                 
    icon_path = input("\n\nEnter the path to the .png you want to use as App-Icon:\n")
    
     
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
    
    output_path = input("\n\nenter the path where you want the edited .ipa:\n") 
 
    output_path = os.path.join(output_path) 
    with zipfile.ZipFile(os.path.join(output_path, "Payload.zip"), 'w', zipfile.ZIP_DEFLATED) as zip_file:  
       for root, dirs, files in os.walk(payload_path): 
           for file in files: 
               file_path = os.path.join(root, file) 
               zip_file.write(file_path, file_path.replace(payload_path, "Payload")) 
                
                
    user_new_ipa_name = input(f"\n\nenter a new name for your edited .ipa\noriginal .ipa name: {file_name}'\n") 
    os.rename(payload_path+".zip", user_new_ipa_name) 
    edited_file_path = os.path.join(output_path, user_new_ipa_name)
    os.replace(user_new_ipa_name, edited_file_path) 
 
     
    print("The App-Icon was changed successfully.") 
 
ipa_path = input("enter the path to your .ipa: ") 
 
file_name = os.path.basename(ipa_path) 
 
zip_path = ipa_path.replace(".ipa", ".zip") 
 
if os.path.exists(ipa_path): 
    os.rename(ipa_path, zip_path) 
    print(".ipa file successfully renamed to .zip.") 
else: 
    print("The .ipa file could not be found. Try again...") 
    exit() 
 
print("[1] change Bundle-ID") 
print("[2] change App-Name") 
print("[3] change App-Icon") 
 
option = int(input("choose an option: ")) 
 
if option == 1: 
    bundleID() 
 
if option == 2: 
     changeName() 
 
if option == 3:
    changeIcon()
    
