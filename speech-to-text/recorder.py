import pathlib
import wave

import pyaudio
import speechToTextpy


class Recorder:
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

    stream = None
    recording = False

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.p.terminate()
        self.wav_file.close()

        with wave.open(self.path, 'r') as wf:
            file_duration = round(wf.getnframes() / wf.getframerate())

        return speechToTextpy.main(self.path, file_duration)

    def record(self):
        """Record audio and pass it to the speech recognition code"""

        def callback(in_data, frame_count, time_info, status):
            """Writing audio data in file"""
            self.wav_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)

        self.stream = self.p.open(rate=self.SAMPLE_RATE,
                                  channels=self.CHANNELS,
                                  format=self.FORMAT,
                                  input=True,
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
