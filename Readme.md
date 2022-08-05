# Scan2Folder

## Enabling the Scan-to-Folder button on HP MFP printers

This is a **PytQt5** desktop app for rapidly scanning documents by using the Scan-to-Folder button on HP Multi Function Printers (MFP)
especially CM Devices.

This app uses the **Sane** backend to get all parameters needed.

It also provides image enhancement features.

>*Note: in this version only the first scanner is used*


**NEW:** OCR processing and PDF-Document creation from your scanns.

After you finished scanning, you can start an OCR-process
The OCR-Process will do the following steps:

1. Deskew each page
2. Crop the image
3. Check text orientation
4. Start ocr
5. Create searchable PDF

You can define the crop size in the configuration dialog

>*Note: In this version A4 page size for 300dpi is predifned.*
If you want to change this, you can do it in ocrtools.py



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


### Installation

Install packages needed with:

>`sudo pip3 install -r deps/dependency.txt`

#### For OCR

Install tesseract-ocr 4 with your language **and**  with Orientation & Script detection


### Binary

In the *bin* directory a `spec` file for `pyinstaller` is provided

Calling `#> pyinstaller scan2folder.spec` creates a single executable binary for your environment

Have a look at the [pyinstaller doc](https://pyinstaller.readthedocs.io) for more information

### New Features

* spec file for creating stand alone binaries
* Image name is cleared when stopped a scan session
* Image name has now auto complete, to avoid overwrite existing files

### Issues

* The script is tested only with a HP CM1312 device
* Only one (the first) scanner is usable
* If the LED does not become green after the device is switched on, may be your device is not supported
* If the LED becomes green and the button keeps yellow, the scanner is locked by another device/thread

### Thanks to

Nicolas Bernaerts who inspired me with his [script](http://www.bernaerts-nicolas.fr/linux/74-ubuntu/264-ubuntu-hp-mfp-scanner-scantofolder)
