import pathlib
import wave

import pyaudio

import speechToTextpy


class Recorder:
    """Records audio and calls speech recognition on it."""
    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()
        self.default_device_info = self.p.get_default_input_device_info()
        self.p.terminate()

        self.path = pathlib.Path.cwd()/'record.wav'
        self.path = self.path.as_posix()

        self.SAMPLE_RATE = int(self.default_device_info["defaultSampleRate"])
        self.DEVICE_INDEX = int(self.default_device_info["index"])
        self.CHANNELS = 1
        self.BLOCK_SIZE = 4096
        self.FORMAT = pyaudio.paInt16

        self.stream = None
        self.recording = False

    def stop_recording(self):
        """Calls speech recognition code."""

        self.recording = False
        self.stream.stop_stream()
        self.p.terminate()
        self.wav_file.close()

        with wave.open(self.path, 'r') as wf:
            file_duration = round(wf.getnframes() / wf.getframerate())

        text = speechToTextpy.main(self.path, file_duration)
        return text

    def record(self):
        """Records audio"""
        self.p = pyaudio.PyAudio()

        self.wav_file = wave.open("record.wav", "wb")
        self.wav_file.setnchannels(self.CHANNELS)
        self.wav_file.setframerate(self.SAMPLE_RATE)
        self.wav_file.setsampwidth(2)

        def callback(in_data, frame_count, time_info, status):
            """Writing audio data in file"""
            self.wav_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)

        self.stream = self.p.open(rate=self.SAMPLE_RATE,
                                  channels=self.CHANNELS,
                                  format=self.FORMAT,
                                  input=True,
                                  input_device_index=self.DEVICE_INDEX,
                                  frames_per_buffer=self.BLOCK_SIZE,
                                  stream_callback=callback
                                  )
        self.recording = True
        while self.recording:
            try:
                self.stream.start_stream()
            except KeyboardInterrupt:
                self.stop_recording()
                break
