#---------------------------------------------------------------------#
# File: /client.py
# Project: https://github.com/Lime-Parallelogram/cj2022-stately-satyrs
# Created Date: Saturday, July 23rd 2022, 4:13:02 pm
# Description: Testing how we can record and send audio across sockets
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Sat Jul 23 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-07-23	WH	System can successfully record audio samples to and from a queue
#---------------------------------------------------------------------#
import sys
import queue
import threading

import sounddevice as sd

FILENAME = "test.wav"
BUFFER_SIZE = 80
BLOCK_SIZE = 1024
SAMPLE_RATE = 44100
CHANNELS = 1

q = queue.Queue(maxsize=BUFFER_SIZE)

def record_buffer():
    """
    Fill up a buffer queue with recorded sound
    """
    event = threading.Event()
    blx_buffered = 0

    def callback(indata, frame_count, time_info, status):
        nonlocal blx_buffered
        
        # Once the buffer is full, stop
        if blx_buffered == BUFFER_SIZE:
            event.set()
            raise sd.CallbackStop
        
        q.put_nowait(bytes(indata))
        print("Samples Recorded: ", q.qsize())
        blx_buffered += 1

    stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, callback=callback, dtype="float32", device="default",
                            channels=CHANNELS)
    with stream:
        event.wait()  # Wait until recording is finished

def play_buffer():
    def callback(outdata, frames, time, status):
        assert frames == BLOCK_SIZE
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = q.get_nowait()
            print("Remaining Samples to play: ", q.qsize())

        except queue.Empty as e:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort from e
            
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data

    event = threading.Event()
    stream = sd.RawOutputStream(
        samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE,
        device="default", channels=CHANNELS, dtype='float32',
        callback=callback, finished_callback=event.set)
    with stream:
        event.wait()  # Wait until playback is finished

record_buffer()
play_buffer()

# async def hello(uri):
    # async with connect(uri) as websocket:
        # await websocket.send(sound())
        # print(await websocket.recv())

# asyncio.run(hello("ws://localhost:8765"))