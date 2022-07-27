from http.client import RemoteDisconnected

import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300

unknow_value_errors = 0  # stores the number of times the sr.UnknownValueError occurred
remote_errors = 0  # tores the number of times the RemoteDisconnected error occurred


def recognize(audio, lang="en-US") -> str:
    """
    Calls google speech recognition API.

    Handles errors and tries different solutions.
    """
    print("working on it")
    global unknow_value_errors
    global remote_errors

    try:
        return recognizer.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        if unknow_value_errors == 0:  # tries with a different language
            recognizer.energy_threshold = 200
            unknow_value_errors += 1
            return recognize(audio, lang="en-GB")
        else:
            unknow_value_errors = 0  # reset to 0 for the next time the function will be called
            return "Didn't catch that"
    except sr.RequestError:
        return "Request error, verify your connection"
    except RemoteDisconnected:
        if remote_errors < 2:
            remote_errors += 1
            return recognize(audio)
        else:
            remote_errors = 0  # reset to 0 for the next time the function will be called
            return "Remote Disconnected, verify your connection"


def main(file_path, file_duration) -> str:
    """
    Returns the text result

    Prepares audio source before passing to the recognize function.
    """
    audio_file = sr.AudioFile(file_path)
    text = ""
    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 10.0

        if file_duration > 15:
            for time in range(int(file_duration/10)+1):
                # Dividing audio source into chunks.
                # Sending a long audio file to the API can return a RemoteDisconnected error.
                audio = recognizer.record(source, duration=10)
                text += recognize(audio)+"\n"
        else:
            audio = recognizer.listen(source)
            text += recognize(audio)+"\n"
    return text
