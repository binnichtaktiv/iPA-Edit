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
parser.add_argument("-k",action="store_true",
                    help="keep source iPA")

args = parser.parse_args()

if os.path.exists(args.o):
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

def zip_ipa(ipa_path, app_path, payload_path):
    print("[*] generating iPA...")
    if args.o.endswith('.ipa'):
        args.o = args.o[:-4]
    shutil.make_archive(args.o, 'zip', payload_path)

    args.o = args.o + '.zip'
    output_name = args.o.replace('.zip', '.ipa')
    os.replace(args.o, output_name)
    if args.k:
        print("[*] source iPA will not be deleted")
        os.rename(zip_path, ipa_path)
    else:
        os.remove(zip_path)
    shutil.rmtree(payload_path)


if args.i:
    ipa_path = args.i
    app_path, zip_path, payload_path = unzip_ipa(ipa_path)

if args.n or args.b or args.v or args.k:

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
            img.resize((120, 120)).save(os.path.join(app_path, "changedicon@2x.png"), "PNG")
            img.resize((152, 152)).save(os.path.join(app_path, f"changedicon@2x~ipad.png"), "PNG")
        
        pl_content["CFBundleIcons"] = {
            "CFBundlePrimaryIcon": {
                "CFBundleIconFiles": [f"{icon_60x60}@2x"],
                "CFBundleIconName": icon
            }
        }

        pl_content["CFBundleIcons~ipad"] = {
            "CFBundlePrimaryIcon": {
                "CFBundleIconFiles": [f"{icon_60x60}@2x", f"{icon_76x76}@2x~ipad"],
                "CFBundleIconName": icon
            }
        }


    with open(plist_path, 'wb') as plist:
        plistlib.dump(pl_content, plist)



zip_ipa(ipa_path, app_path, payload_path)

