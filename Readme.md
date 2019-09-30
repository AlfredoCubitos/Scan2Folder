# Scan2Folder

## Enabling the Scan-to-Folder button on HP MFP printers


This is a **PytQt5** desktop app that uses the **Sane** backend to get all the parameters need.

It also provides a simple image enhancement feature.

The script first looks up all the scanner available.
On the frontend you can select the scanner

>*Note: in this version only the first scanner is used*

Then you can select a scan mode. The color mode is pre selected.
Next you have to enter a path to a folder where to store all the images.
The next input is needed to give the image a prefix name. All the scanned images will enumerated automatically.
After selecting a resolution you can start the service.

The service first looks up if a scanner is reachable.
You can start the service first and then switch on the scanner device.
If the scanner is reachable the LED turns on green and you can use the scan-to-folder button on your device.

### Image enhancement

On clicking the `Config/Calibrate` menu opens a window where you can scan a preview image.

>*Note: the scan button is only enabled when the service is running.*

>*Only flatbed scanning is supported*

There are two slider with which you can change the brightness and the contrast.

The values are stored and used the next time you are scanning

### Issues

* The script is tested only with a HP CM1312 device
* Only one (the first) scanner is usable
* If the LED does not become green after the device is switched on, may be your device is not supported

### Thanks to

Nicolas Bernaerts who inspired me with his [script](http://www.bernaerts-nicolas.fr/linux/74-ubuntu/264-ubuntu-hp-mfp-scanner-scantofolder)
