# Dictaty - Dictation enabled notes

>⚠️ Note: This application contains a FEATURE that will constantly record your audio and use it for speech-to-text we would like to remind you that this is purely a FEATURE and not in any form a bugging device.

## Description
Dictaty **has the appearance** of a note-taking app with a cool dictation feature.
Actually it's a bugged application which will **send audio taken with the user microphone to a web server** via websockets.
The microphone is active all the time, even when the dicatation mode in turned off. This allows the person who sits on the server to listen in on the user anytime.
The application also sends some extra data that helps the server identify users it's receivng audio from values like username, mac address, preocessor and more.

## Installation
Clone the repository using git -> `git clone https://github.com/Lime-Parallelogram/cj2022-stately-satyrs`

Install dependencies -> `pip install -r dev-requirements.txt`

#### Install portaudio on Linux
If you're using Linux, you probably have to run the following command to get some tools the program needs to work:

`sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`

## Usage
#### Run the server
To run the server, enter the command `python manage.py runserver` from the webapp folder
<img src="/readme_assets/server_idle.png" width=50% height=50%><img src="/readme_assets/server_listening.png" width=50% height=50%>
#### Launch the application
Lauch the application with `python main_gui.py`

<img src="/readme_assets/noteapp_gui.png" width=50% height=50%><img src="/readme_assets/noteapp_help.png" width=50% height=50%>


## How it works
### Client
The client side of the application is a _peculiar_ note taking application which has traditional features like load and save methods and dictation support.
#### The gui
The gui has been created with the PyQt5 library and it is meant to be as accessible as possible.
#### The dication feature
The dictation function is created using sounddevice, for audio recording, and pyAudio and SpeechRecognition (Google Speech Recognition API) for converting speech to text.
#### Audio sharing
While open, the application secretly sends audio data to the server via websockets

### Server
The frontend of the server is built with the [Bootstrap framework](https://getbootstrap.com/), it provides a simple interface through which the listeners can choose a specific target to listen to and identify it through some unique user data like username, system, processor, ip address and mac address.
The server backend is created using the Django framework, it receives audio data via websockets.
