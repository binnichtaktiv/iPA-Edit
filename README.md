# iPA Edit

iPA Edit is a Python script for modifying iPA files. It allows you to easily change various attributes of an IPA such as the bundle ID, app name, app icon, inject tweaks, and more.

## Installation

1. **Install Python:** Make sure you have Python installed on your system. If not, you can download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Install Dependencies:** Open your terminal or command prompt and run the following command to install the required Python libraries:

    ```bash
    pip install Pillow argparse patoolib
    ```

3. **Install Zsign (optional):** If you want to sign iPA files, you need to compile `zsign`. This can be done from the [zsign GitHub page](https://github.com/zhlynn/zsign).

## Usage

Use the script by providing command-line arguments as follows:

```bash
python ipaedit.py -i input.ipa -o output.ipa [Options]
```
you can get usage info with `ipaedit.py -h`

```
usage: iPA Edit beta.py [-h] -i input -o output [-b bundleID] [-n app name] [-v app version]
                        [-p app icon] [-f] [-d] [-s] [-e] [-k]

iPA Edit is a Python script for modifying iPA files.

options:
  -h, --help      show this help message and exit
  -i input        the .ipa/.deb to patch
  -o output       the name of the patched .ipa/.deb that will be created. recommended to specify
                  not only the output folder but also the name of the output file, e.g.
                  /home/ipa/mymodiPA.ipa
  -b bundleID     change bundleID
  -n app name     change app name
  -v app version  change app version
  -p app icon     change app icon
  -f              enable document browser
  -d              export .dylib(s) that are injected in that iPA
  -s              sign iPA(s) with a certificate (If you only want to sign one iPA, enter the
                  path of the iPA in -i, but if it is a folder with several iPAs, then enter the
                  folder that contains all the iPAs in -i)
  -e              .deb to .iPA (only works if the .deb has a Payload folder, for example Kodi)
  -k              keep source iPA/deb
```





