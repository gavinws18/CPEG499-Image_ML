ELEG/CPEG-498/499 Image_ML Senior Design Project

Gavin Schrader, Paul Zaloga, JT Farro

This Python program was designed to detect text in a foreign language, and then translate the detected text into a desired language.

The following components were used:

-Raspberry Pi
-PiCam
-Touch Screen 
-Power Supply
-Heat Sink

The following libraries were used:

-tkinter
-googletrans
-pytesseract
-opencv
-PIL
-sys
-io
-picamera

It is recommended to use the default mode as some of the other modes still have some bugs to work out.
Block Text and Single line mode work fairly well however.

How to use the program:

Upon starting the program you are presented with 5 different modes: Default, Block Text, Single Line, Single Word, and Column Text. These different modes
all use a different page segmentation mode. Default works well with a variety of text while the other modes are more specific to those forms of text.
After choosing a mode you will be give a choice of target languages in the top row. If the target language is latin based, choose the "latin based" option.
Otherwise select the language you are targeting. After selecting a target language you will then select a destination language below. This is the language the
input will be translated to. 

For example if I want to translate Spanish text to English I would select "latin based" as the target language, and "English" as the destination language.
If I want to translate Russian text to French, I would select "Russian" as the target language and "French" as the destination language.

After choosing both languages, capture mode will start.

The program will capture a new image approximately every second and display the results to the text box along with a confidence value.
This process is repeated constantly with the new output being added to the text box every iteration.

The "reset" button can be used at any time to go back to the language select menu.
The "stop" button can be used at any time to shut down the program.
The "pause" button currently has no functionality.

Current Target Language Options:

-latin based
-arabic
-russian
-hindi (untested)
-chinese simplified (needs fixing)
-japanese (untested)

Current Destination Language Options:

-english
-spanish
-french
-german
-italian
-portugese
-arabic
-russian
-hindi
-chinese simplified
-japanese
