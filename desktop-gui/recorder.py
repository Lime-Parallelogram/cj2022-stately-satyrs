import os
import pathlib
import queue
import sys
import time

import sounddevice as sd
import soundfile as sf

import speechToTextpy


class Recorder:
    """Records audio and calls speech recognition on it."""

    def __init__(self) -> None:
        self.path = pathlib.Path.cwd()/'record.wav'
        self.path = self.path.as_posix()

        self.SAMPLE_RATE = 44100
        self.CHANNELS = 1
        self.BLOCK_SIZE = 4096
        self.SUBTYPE = "PCM_16"

        self.q = queue.Queue()
        self.recording = True

    def stop_recording(self):
        """Calls speech recognition code."""
        self.recording = False

        time.sleep(0.3)
        text = speechToTextpy.main(self.path, self.duration)
        os.remove(self.path)
        return text

    def record(self):
        """Records audio"""
        with sf.SoundFile(self.path, mode='x', samplerate=self.SAMPLE_RATE,
                          channels=self.CHANNELS, subtype=self.SUBTYPE) as file:
            with sd.InputStream(samplerate=self.SAMPLE_RATE, device=self.get_default(),
                                channels=self.CHANNELS, callback=self.callback):
                while self.recording:
                    file.write(self.q.get())

            self.duration = len(file) / self.SAMPLE_RATE

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)

        self.q.put(indata.copy())

    def get_default(self):
        """Get the name of the default microphone"""
        all_devices = sd.query_devices()
        default_mic = sd.default.device[0]
        device_name = all_devices[default_mic]["name"]
        return device_name
