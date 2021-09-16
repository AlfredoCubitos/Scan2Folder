# Scan2Folder

## Enabling the Scan-to-Folder button on HP MFP printers

This is a **PytQt5** desktop app for rapdly scanning documents by using the Scan-to-Folder button on HP Multi Function Printers (MFP) 
especially CM Devices.

This app uses the **Sane** backend to get all parameters needed.

It also provides a simple image enhancement feature.

The script first looks up all the scanner available.
On the frontend you can select the scanner

>*Note: in this version only the first scanner is used*

### Usage

1. Ensure that your scanner is reachable
2. Start the app
3. Select a *ScanMode*
4. Select a path where you want to store your images
5. Enter an image prefix name. All the scanned images will enumerated automatically.
6. Choose a scan resolution
7. Press the *Start Service* button

If the scanner is reachable the LED turns on green and you can use the scan-to-folder button on your device.

### Image enhancement

On clicking the `Config/Calibrate` menu opens a window where you can scan a preview image.

>*Note: the scan button is only enabled when the service is running.*

>*Only flatbed scanning is supported*

There are two slider with which you can change the brightness and the contrast.

The values are stored and used the next time you are scanning

### Installation

Install packages needed with:

>`sudo pip3 install -r deps/dependency.txt`


### New Features

* Image name is cleared when stopped a scan session
* Image name has now autocomplete, to avoid overwrite existing files

### Issues

* The script is tested only with a HP CM1312 device
* Only one (the first) scanner is usable
* If the LED does not become green after the device is switched on, may be your device is not supported
* If the LED becomes green and the button keeps yellow, the scanner is locked by another device/thread

### Thanks to

Nicolas Bernaerts who inspired me with his [script](http://www.bernaerts-nicolas.fr/linux/74-ubuntu/264-ubuntu-hp-mfp-scanner-scantofolder)
