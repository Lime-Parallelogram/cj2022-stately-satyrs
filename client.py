# ---------------------------------------------------------------------#
# File: /client.py
# Project: https://github.com/Lime-Parallelogram/cj2022-stately-satyrs
# Created Date: Saturday, July 23rd 2022, 9:57:26 pm
# Description: System that sends microphone audio over websockets
# Author: Will Hall
# Copyright (c) 2022 Lime Parallelogram
# -----
# Last Modified: Mon Jul 25 2022
# Modified By: Will Hall
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-07-25	WH	Records audio from microphone and sends it via a queue over websocket
# ---------------------------------------------------------------------#
# Import modules
import asyncio
import queue
import sys
import json

import sounddevice as sd
import websockets
import user_info_util as util

# Program settings
BUFFER_SIZE = 80  # Max length of outgoing_queue
BLOCK_SIZE = 4096  # Number of bytes per websocket message
SAMPLE_RATE = 12000
CHANNELS = 1  # Audio recording channels
DEVICE = "default"
TIMEOUT = (1/SAMPLE_RATE)*BLOCK_SIZE

outgoing_queue = queue.Queue(maxsize=BUFFER_SIZE)


async def record_buffer(websocket):
    """Capture microphone audio into buffer queue"""
    event = asyncio.Event()

    def callback(indata, frame_count, time_info, status):
        # Add captured sample to outgoing queue
        outgoing_queue.put(bytes(indata), timeout=TIMEOUT)
        print("Sample added", outgoing_queue.qsize())

    # Start capturing input data using sounddevice library
    stream = sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, callback=callback, dtype="float32",
                               device=DEVICE, channels=CHANNELS)
    with stream:
        timeout_multiplier = 1  # Timeout multiplier used to adjust rate at which que is dispatched

        await asyncio.sleep(TIMEOUT*5)  # Wait for the queue size to build up to at least 5

        while outgoing_queue.qsize() > 0:
            print("Sent data. Queue size is now:", outgoing_queue.qsize())

            # Update timeout multiplier to attempt to keep record queue constant length
            if outgoing_queue.qsize() > 20:
                timeout_multiplier -= 0.001
            elif outgoing_queue.qsize() < 15:
                timeout_multiplier += 0.001

            await asyncio.sleep(TIMEOUT*timeout_multiplier)  # Delay to keep queue outgoing consistent with incoming
            data = outgoing_queue.get()
            await websocket.send(data)
            await websocket.recv()  # OK is sent by server

        print("send queue empty")
        await event.wait()  # Wait until recording is finished


async def send_user_info(websocket):
    """Sends the user data collected from the client to the server in the form of a json string """
    user_info = json.dumps(util.get_info())
    await websocket.send(user_info)


async def main():
    """Main event loop runs client"""
    async with websockets.connect("ws://0.0.0.0:8765") as websocket:
        await send_user_info(websocket)
        await record_buffer(websocket)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')
