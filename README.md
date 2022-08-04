# Dictaty - Dictation enabled notes

>⚠️ Note: This application contains a FEATURE that will constantly record your audio and use it for speech-to-text we would like to remind you that this is purely a FEATURE and not in any form a bugging device.

## Description
Dictaty **has the appearance** of a digital notebook with a cool dictation feature.
Actually it's a bugged application which will **send audio taken with the user microphone to a web server** via websockets.
The microphone is active all the time, even when the dicatation mode in turned off. This allows the person who sits on the server to listen in on the user anytime.
The application also sends some extra data that helps the server identify users it's receivng audio from values like username, mac address, preocessor and more.

## Installation
Clone the repository using git -> `git clone https://github.com/Lime-Parallelogram/cj2022-stately-satyrs`

Install dependencies -> `pip install requirements.txt`

#### Install portaudio on Linux
If you're using Linux, you probably have to run the following command to get some tools the program needs to work:

`sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`

## Usage
#### Run the server
To run the server, enter the command `python manage.py runserver` from the webapp folder
#### Launch the application
Lauch the application with `python main_gui.py`
