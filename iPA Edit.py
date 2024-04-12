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

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def unzip_ipa(ipa_path):
    clear_terminal()
    #file_name_no_ipa = os.path.basename(ipa_path)[:-4]
    zip_path = ipa_path.replace(".ipa", ".zip")

    if os.path.exists(args.i):
        os.rename(args.i, zip_path)
        print("[*] iPA file successfully renamed to .Zip")
        time.sleep(1)
    else:
        sys.exit("[!] .iPA file could not be found. Try again...")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.extractall(os.path.dirname(zip_path))

    payload_path = os.path.join(os.path.dirname(zip_path), "Payload")

    for item in os.listdir(payload_path):
        if item.endswith(".app"):
            app_folder = item
            break

    if app_folder is None:
        sys.exit("[!] app folder not found. Try it again and check your iPA...")

    app_path = os.path.join(payload_path, app_folder)
    return app_path, zip_path, payload_path

parser = argparse.ArgumentParser(description="iPA Edit is a Python script for modifying iPA files. It allows you to easily change various attributes of an IPA such as the bundle ID, app name, app icon, inject tweaks, and more.")
parser.add_argument("-i", metavar="input", type=str, required=True,
                    help="the .ipa/.deb to patch")
parser.add_argument("-o", metavar="output", type=str, required=False,
                    help="the name of the patched .ipa/.deb that will be created. recommended to specify not only the output folder but also the name of the output file, e.g. /home/ipa/mymodiPA.ipa")
args = parser.parse_args()

if args.i:
    app_path, file_name_no_ipa, zip_path, payload_path = unzip_ipa(args.i)
