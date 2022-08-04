# Dictaty - Dictation enabled notes

>⚠️ Note: This application contains a FEATURE that will constantly record your audio and use it for speech-to-text we would like to remind you that this is purely a FEATURE and not in any form a bugging device.

## Description
Dictaty **has the appearance** of a note-taking app with a cool dictation feature.
Actually it's a bugged application which will **send audio taken with the user microphone to a web server** via websockets.
The microphone is active all the time, even when the dictation mode in turned off. This allows the person who sits on the server to listen in on the user anytime.
The application also sends some extra data that helps the server identify the users it's receiving audio from, using values like username, mac address, processor and more. The application aims to convince ignorant users that its audio related functionality is purely a feature; not a bugging device, hence how it links to the theme 'its not a bug, its a feature'.

## Installation
Clone the repository using git -> `git clone https://github.com/Lime-Parallelogram/cj2022-stately-satyrs`

Install dependencies -> `pip install -r dev-requirements.txt`

#### Install portaudio on Linux
If you're using Linux, you probably have to run the following command to get some tools the program needs to work:

`sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0`

## Usage
#### Run the server
To run the server, enter the command `python manage.py runserver` from the webapp folder

#### Server in Action
<img src="/readme_assets/server_idle.png" width=50% height=50%>

#### Server Listening in Action
<img src="/readme_assets/server_listening.png" width=50% height=50%>

#### Launch the application
Launch the application with `python main_gui.py`

#### Main GUI
<img src="/readme_assets/noteapp_gui.png" width=50% height=50%>

#### Information Popup
<img src="/readme_assets/noteapp_help.png" width=50% height=50%>


## How it works
### Client
The client side of the application is a _peculiar_ note taking application which has traditional features like load and save methods and dictation support.
#### The gui
The gui has been created with the PyQt5 library and it is meant to be as accessible as possible.
#### The dictation feature
The dictation function is created using sounddevice, for audio recording, and SpeechRecognition (Google Speech Recognition API) for converting speech to text.
#### Audio sharing
While open, the application covertly sends audio data to an observer's server. Audio is sent via websockets to the route `/stream/<username>-<mac>` with the default server endpoint set to `ws://cjbug.limeparallelogram.uk` however this is offline for security reasons. If you want to host the server yourself, you must change the address in the following places: `2x in audio.js`, `1x in bugClient.py` and also modify `ALLOWED_HOSTS` in the django `settings.py`. 

### Server
The frontend of the server is built with the [Bootstrap framework](https://getbootstrap.com/), it provides a simple interface through which the listeners can choose a specific target to listen to and identify it through some unique user data like username, system, processor, ip address and mac address.
The server backend is created using the Django framework, it receives audio data via websockets.  
When a client connects, on the endpoint `/stream/<user-mac>`, django creates a dedicated channel with the <user-mac> as its name. It will then begin re-broadcasting all binary audio data to this group. This means that when a listener joins the group using the url `/listen/<user-mac>`, they receive all of this data.  
When no listener is connected, the client receives the `NO LISTENER` message. This causes it to enter a low-profile mode, only attempting to resume broadcasting every 30 seconds. This helps reduce client bandwidth and maintain stealth.  
Upon receiving a client ping, the server adds a database entry for that user or - if it already exists - updates the last-ping property. Only clients who have sent a ping in the last 2 mins are displayed on the client list.
