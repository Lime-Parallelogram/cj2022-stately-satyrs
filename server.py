# ---------------------------------------------------------------------#
# File: /server.py
# Project: https://github.com/Lime-Parallelogram/cj2022-stately-satyrs
# Created Date: Saturday, July 23rd 2022, 10:02:10 pm
# Description: Websocket server to receive and play audio
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Mon Jul 25 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-07-25	WH	Module receives data from a single client and plays it out loud directly from the queue
# ---------------------------------------------------------------------#
# Imports modules
import asyncio
import queue
import sys

import sounddevice as sd
import websockets

# Program settings
BUFFER_SIZE = 80  # Max length of outgoing_queue
BLOCK_SIZE = 4096  # Number of bytes per websocket message
SAMPLE_RATE = 12000
CHANNELS = 1  # Audio recording channels
DEVICE = "default"

playback_started = False  # Track whether the playback thread is active

incoming_queue = queue.Queue(maxsize=BUFFER_SIZE)


async def play_buffer():
    """Play audio from the incoming queue using the sounddevice module"""
    event = asyncio.Event()
    loop = asyncio.get_event_loop()

    def callback(outdata, frames, time, status):
        global playback_started
        assert frames == BLOCK_SIZE  # If the number of frames returned != BLOCK_SIZE flag an error

        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status

        try:
            data = incoming_queue.get_nowait()
            print("Remaining Samples to play: ", incoming_queue.qsize())
        except queue.Empty:
            # If the queue empties, stop the playback module for now. It can be re-started later
            playback_started = False
            loop.call_soon_threadsafe(event.set)
            raise sd.CallbackStop

        outdata[:] = data

    # Start output with sounddevice module
    stream = sd.RawOutputStream(
        samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE,
        device=DEVICE, channels=CHANNELS, dtype='float32',
        callback=callback, finished_callback=event.set)

    with stream:
        await event.wait()  # Wait until playback is finished


async def add_que(websocket):
    """Add incoming audio to playback queue"""
    global playback_started

    async for message in websocket:
        if type(message) == str:
            print(message)  # if data is in string format it will display and write data to a json file
            with open("data.json", "w+") as f:
                f.write(message)
        elif type(message) == bytes:
            incoming_queue.put_nowait(message)  # Add message content to playback queue
            print("New size: ", incoming_queue.qsize())

        # Start playback module
        if not playback_started and incoming_queue.qsize() > 10:
            playback_started = True
            print("Starting playback")

            asyncio.create_task(play_buffer())

        await websocket.send("OK")  # Send response to websocket


async def main():
    """Main Event loop"""
    print("Starting server")
    async with websockets.serve(add_que, "0.0.0.0", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())  # Start main event loop
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')
