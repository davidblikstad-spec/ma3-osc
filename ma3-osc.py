#!/usr/bin/env python3
"""Send a grandMA3 command-line command via OSC.

Usage:
    ma3-osc.py "Go+ Exec 202"
    ma3-osc.py --host 192.168.10.163 --port 53000 "Fixture 1 At 75"

Desk setup (Menu -> In & Out -> OSC, active line):
    Enable Input = Yes, Receive Command = Yes, prefix blank.
Sends OSC address /cmd with a single string argument.
"""
import argparse
import socket
import sys


def osc_string(s: str) -> bytes:
    b = s.encode() + b"\x00"
    b += b"\x00" * ((4 - len(b) % 4) % 4)
    return b


def osc_message(addr: str, arg: str) -> bytes:
    return osc_string(addr) + osc_string(",s") + osc_string(arg)


def main() -> int:
    p = argparse.ArgumentParser(description="Send a grandMA3 command via OSC /cmd")
    p.add_argument("command", help='grandMA3 command line, e.g. "Go+ Exec 202"')
    p.add_argument("--host", default="192.168.10.163", help="desk IP (default: 192.168.10.163)")
    p.add_argument("--port", type=int, default=53000, help="OSC input port (default: 53000)")
    p.add_argument("--address", default="/cmd", help="OSC address (default: /cmd; blank prefix)")
    args = p.parse_args()

    pkt = osc_message(args.address, args.command)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.sendto(pkt, (args.host, args.port))
    finally:
        s.close()
    print(f"Sent -> {args.host}:{args.port} | {args.address} ,s | {args.command!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
