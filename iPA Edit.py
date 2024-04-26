import os 
import sys
import zipfile 
import plistlib 
import shutil
import subprocess
import time
import patoolib
import requests
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="iPA Edit is a Python script for modifying iPA files. It allows you to easily change various attributes of an IPA such as the bundle ID, app name, app icon, inject tweaks, and more.")
parser.add_argument("-i", metavar="input", type=str, required=True,
                    help="the .ipa/.deb to patch")
parser.add_argument("-o", metavar="output", type=str, required=True,
                    help="the name of the patched .ipa/.deb that will be created. recommended to specify not only the output folder but also the name of the output file, e.g. /home/ipa/mymodiPA.ipa")
parser.add_argument("-b", metavar="bundleID", type=str,
                    help="change bundleID")
parser.add_argument("-n", metavar="app name", type=str,
                    help="change app name")
parser.add_argument("-v", metavar="app version", type=str,
                    help="change app version")
parser.add_argument("-p", metavar="app icon", type=str,
                    help="change app icon")
parser.add_argument("-f",action="store_true",
                    help="enable document browser")
parser.add_argument("-d", action="store_true",
                    help="export .dylib(s) that are injected in that iPA")
parser.add_argument("-s", action="store_true",
                    help="sign iPA(s) with a certificate")
parser.add_argument("-k", action="store_true",
                    help="keep source iPA")

args = parser.parse_args()
    
if os.path.exists(args.o) and not args.d and not args.s:
    overwrite = input(f"[<] {args.o} already exists. overwrite? [Y/n] ").lower().strip()
    if overwrite in ("y", "yes", ""):
        del overwrite
    else:
        print("[>] quitting")
        sys.exit()

def unzip_ipa(ipa_path):
    print("[*] extracting iPA")
    zip_path = ipa_path.replace(".ipa", ".zip")

    if os.path.exists(ipa_path):
        os.rename(ipa_path, zip_path)
        time.sleep(1)
    else:
        sys.exit("[!] .iPA file could not be found. Try again...")

    with zipfile.ZipFile(zip_path, 'r') as payload:
        payload.extractall(os.path.dirname(zip_path))

    payload_path = os.path.join(os.path.dirname(zip_path), "Payload")

    for item in os.listdir(payload_path):
        if item.endswith(".app"):
            app_folder = item
            break

    if app_folder is None:
        sys.exit("[!] app folder not found. Try it again and check your iPA...")

    print("[*] extracted iPA")
    app_path = os.path.join(payload_path, app_folder)
    return app_path, zip_path, payload_path

def zip_ipa(ipa_path, payload_path):
    
    print("[*] generating iPA...")
    if args.o.endswith('.ipa'):
        args.o = args.o[:-4]
    shutil.make_archive(args.o, 'zip', os.path.dirname(payload_path), os.path.basename(payload_path))

    args.o = args.o + '.zip'
    output_name = args.o.replace('.zip', '.ipa')
    os.replace(args.o, output_name)
    if args.k:
        print("[*] source iPA will not be deleted")
        os.rename(zip_path, ipa_path)
    else:
        os.remove(zip_path)
    shutil.rmtree(payload_path)


if not args.s:
    ipa_path = args.i
    app_path, zip_path, payload_path = unzip_ipa(ipa_path)

if args.n or args.b or args.v or args.k or args.f:

    plist_path = os.path.join(app_path, 'Info.plist')
    with open(plist_path, 'rb') as plist:
        pl_content = plistlib.load(plist)

    if args.b:
        old_bundleID = pl_content['CFBundleIdentifier']
        print("[*] current bundleID:", old_bundleID)
        new_bundleID = args.b
        pl_content['CFBundleIdentifier'] = new_bundleID
        print("[*] changed bundleID to:", new_bundleID)

    if args.n:
        new_name = args.n
        if 'CFBundleDisplayName' in pl_content:
            app_name = pl_content['CFBundleDisplayName']
            print("[*] current App-Name:", app_name)
            pl_content['CFBundleDisplayName'] = new_name 
        else:
            app_name = pl_content.get('CFBundleName')
            print("[*] current App-Name:", app_name)
            pl_content['CFBundleName'] = new_name
        print("[*] changed app name to:", new_name)
    
    if args.v:
        new_version = args.v
        old_version = pl_content['CFBundleShortVersionString']
        print("[*] current app version:", old_version)
        pl_content['CFBundleShortVersionString'] = new_version
        print("[*] changed app version to:", new_version)
    
    if args.p:
        icon = "changedicon_"
        icon_60x60 = f"{icon}60x60"
        icon_76x76 = f"{icon}76x76"

        if not args.p.endswith(".png"):
            with Image.open(args.p) as img:
                img.save(args.p, "PNG")

        with Image.open(args.p) as img:
            img.resize((120, 120)).save(os.path.join(app_path, "changedicon_60x60@2x.png"), "PNG")
            img.resize((152, 152)).save(os.path.join(app_path, f"changedicon_76x76@2x~ipad.png"), "PNG")
        
        pl_content["CFBundleIcons"] = {
            "CFBundlePrimaryIcon": {
                "CFBundleIconFiles": [f"{icon_60x60}"],
                "CFBundleIconName": icon
            }
        }

        pl_content["CFBundleIcons~ipad"] = {
            "CFBundlePrimaryIcon": {
                "CFBundleIconFiles": [f"{icon_60x60}", f"{icon_76x76}"],
                "CFBundleIconName": icon
            }
        }
        print("[*] changed ap icon")
    
    if args.f:
        pl_content['LSSupportsOpeningDocumentsInPlace'] = True
        pl_content['UIFileSharingEnabled'] = True
        print("[*] enabled document browser")

    with open(plist_path, 'wb') as plist:
        plistlib.dump(pl_content, plist)

if args.d:
    dylib_files = []
    for root, _, files in os.walk(app_path):
        for file in files:
            if file.endswith('.dylib'):
                dylib_files.append(os.path.join(root, file))
    if not dylib_files:
        print("[!] no dylibs found")
        
    for index, file in enumerate(dylib_files, start=1):
        print(f'{index}: {os.path.basename(file)}')

    selected_files = input("[?] enter the numbers of the files to be exported separated by commas\nenter 'exit' to exit without exporting\n")

    if selected_files.strip().lower() == 'exit':
        os.rename(zip_path, ipa_path)
        shutil.rmtree(payload_path)
        sys.exit("[!] you decided to exit!\n[*] cleaned up temp files")

    selected_nums = [int(num.strip()) - 1 for num in selected_files.split(',')]
    selected_dylibs = [dylib_files[index] for index in selected_nums]
    if not os.path.exists(args.o):
        os.rename(zip_path, ipa_path)
        shutil.rmtree(payload_path)
        sys.exit("[!] please check your output folder! it doesn't seem to exist\n[*] cleaned up temp files")

    for file in selected_dylibs:
        shutil.copy(file, args.o)
    print("[*] exported .dylib(s) successfully")
    
    
if args.s:
    p12_path = ""
    mb_path = ""
    try:
        subprocess.run(["zsign"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        zsign_path = 'zsign'
    except FileNotFoundError:
        zsign_path = input("[?] enter zsign excutable path:\n")

    if not args.i.endswith(".ipa"):
        output_dir = os.path.join(args.o, 'signed_iPAs')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        dir_files = os.listdir(args.i)
        ipa_files = [i for i in dir_files if i.endswith('.ipa')]
                
        for file in os.listdir(args.i):
            if file.endswith(".p12"):
                p12_path = os.path.join(args.i, file)
            elif file.endswith(".mobileprovision"):
                mb_path = os.path.join(args.i, file)

    if p12_path and mb_path:
        use_cert = input(f"[?] .p12 and .mobileprovision file was found at: {args.i}. do you want to use this certificate? [Y/n] ").lower().strip()
        if use_cert in ("y", "yes", ""):
            print(f"[*] {mb_path} and {p12_path} will be used")
    else:
        p12_path = input("[?] enter .p12 file path:\n")
        mb_path = input("[?] enter .mobileprovision file path:\n")
        
    cert_pw = input("[?] enter certificate password:\n")
     
    if not args.i.endswith(".ipa"):       
        for ipa_file in ipa_files:
                ipa_path = os.path.join(args.i, ipa_file)
                ipa_name = os.path.basename(ipa_path)
                signed_ipa = output_dir + "/" + ipa_name
                cmd = f'"{zsign_path}" -k "{p12_path}" -m "{mb_path}" -p "{cert_pw}" -o "{signed_ipa}" -z 9 "{ipa_path}"'
                subprocess.run(cmd, shell=True)
    else:
        if not args.o.endswith(".ipa"):
            args.o += '.ipa'
        cmd = f'"{zsign_path}" -k "{p12_path}" -m "{mb_path}" -p "{cert_pw}" -o "{args.o}" -z 9 "{args.i}"'
        subprocess.run(cmd, shell=True)


if not args.d and not args.s:
    zip_ipa(ipa_path, payload_path)
elif not args.s:
    os.rename(zip_path, ipa_path)
    shutil.rmtree(payload_path)
    print("[*] deleted temp files")

    
