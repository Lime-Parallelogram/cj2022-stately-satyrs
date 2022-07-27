import pyaudio
import wave
import pathlib
import speechToTextpy

p = pyaudio.PyAudio()
default_device_info = p.get_default_input_device_info()
path = pathlib.Path.cwd()/'record.wav'
path = path.as_posix()

SAMPLE_RATE = int(default_device_info["defaultSampleRate"])
CHANNELS = 1
BLOCK_SIZE = 4096
FORMAT = pyaudio.paInt16

wav_file = wave.open("record.wav", "wb")
wav_file.setnchannels(CHANNELS)
wav_file.setframerate(SAMPLE_RATE)
wav_file.setsampwidth(2)


def callback(in_data, frame_count, time_info, status):
    """Writing audio data in file"""
    wav_file.writeframes(in_data)
    return (in_data, pyaudio.paContinue)


stream = p.open(rate=SAMPLE_RATE,
                channels=CHANNELS,
                format=FORMAT,
                input=True,
                frames_per_buffer=BLOCK_SIZE,
                stream_callback=callback
                )

record = True
def start_recording():
    """Start recording"""
    while record:
        try:
            stream.start_stream()
        except KeyboardInterrupt:
            stream.stop_stream()
            p.terminate()
            wav_file.close()
            break
    stream.stop_stream()
    p.terminate()
    wav_file.close()
    with wave.open(path, 'r') as wf:
        file_duration = round(wf.getnframes() / float(wf.getframerate()))
    return speechToTextpy.main(path, file_duration)
