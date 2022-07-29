import os
import platform
import socket
import uuid


def get_ip() -> str:
    """Returns the local lan ip of the device"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('10.254.254.254', 1))  # try to connect to a random irresponsive ip
    ip = str(sock.getsockname()[0])  # use the connection to get lan ip
    sock.close()
    return ip


def get_mac_addr() -> str:
    """Returns the mac address of the device"""
    mac_hex = hex(uuid.getnode())[2:]  # get macaddress in hexadecimal format exclude 0x
    mac_addr = ":".join([mac_hex[i:i+2] for i in range(0, len(mac_hex), 2)]
                        )  # convert the hex to standard mac address format
    return mac_addr


def get_info() -> dict:
    """Returns a dictionary containing all the information about the device"""
    data = {}
    data["system"] = platform.system()
    data["version"] = platform.version()
    data["release"] = platform.release()
    data["username"] = os.getlogin()
    data["architechture"] = platform.machine()
    data["processor"] = platform.processor()
    data["ip"] = get_ip()
    data["mac-address"] = get_mac_addr()
    return data
