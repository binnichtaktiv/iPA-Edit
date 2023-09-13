# iPA Edit

iPA Edit is a Python script for modifying and resigning iOS IPA files. It allows you to easily change various attributes of an IPA such as the bundle ID, app name, app icon, inject tweaks, and more.

## Features

- Download IPAs directly via URL
- Change bundle ID
- Change app name
- Change app version
- Change app icon
- Inject Satella jailbreak  
- Inject sideload detection bypasses
- Simplified Azule IPA patching
- Update modded IPAs
- Export .dylib files from IPA
- Change .dylib dependencies
- Add hidden cracker name to IPA
- Sign and upload IPAs in bulk
- Convert .deb to .ipa

## Requirements

- Python 3
- Azule (for some functions)
- zsign (for bulk signing)

## Installation

1. Install Python 3 if not already installed

2. Clone this repository:

3. Install dependencies: ```pip3 install patool requests```

4. Install [Azule](https://github.com/Al4ise/Azule) for IPA patching functions

5. Install [zsign](https://github.com/zcutil/zsign) for bulk signing IPAs (not finished)

6. Run the script: ```python3 iPA Edit.py```


## Usage

Run the script and follow the prompts to choose the desired option. Most options will ask you to provide an IPA file path and make changes as needed.

- For downloading IPAs, provide a direct URL when prompted

- For bulk resigning, provide paths to certificate, mobileprovision, and a folder with IPAs  

- For Satella and bypass injection, have the necessary files downloaded already

- For Azule functions, ensure Azule is installed and in PATH

The script will output new files to the same folder as the input IPA by default. Provide custom output paths when prompted if needed.

Some options like app name, bundle ID, icon etc. directly modify the IPA plist. Others like Satella injection use Azule to rebuild a new IPA.
