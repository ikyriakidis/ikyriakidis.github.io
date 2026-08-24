#!/usr/bin/env python3
"""
Start and stop the local preview server.

    python serve.py start
    python serve.py stop
    python serve.py status

Normally driven through the Makefile (make run / make stop). This exists so
the commands behave the same from cmd, PowerShell or Git Bash: backgrounding
a process and finding it again differ per shell, so Python does it instead.
"""
import os
import re
import sys
import signal
import socket
import subprocess
import pathlib

ROOT = pathlib.Path(__file__).parent
PID_FILE = ROOT / ".server.pid"
PORT = 4000
URL = "http://localhost:%d" % PORT
WINDOWS = os.name == "nt"


def pid_alive(pid):
    """Is this pid a live process?

    os.kill(pid, 0) is the usual POSIX trick, but on Windows signal 0 is not a
    no-op probe: os.kill routes anything that is not a console event straight
    to TerminateProcess. Asking whether a process exists would try to kill it.
    """
    if WINDOWS:
        out = subprocess.run(["tasklist", "/FI", "PID eq %d" % pid],
                             capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def pid_on_port():
    """The pid listening on PORT, so an orphaned server can still be stopped."""
    try:
        if WINDOWS:
            out = subprocess.run(["netstat", "-ano", "-p", "TCP"],
                                 capture_output=True, text=True).stdout
            for line in out.splitlines():
                if ":%d " % PORT in line and "LISTENING" in line:
                    return int(line.split()[-1])
        else:
            out = subprocess.run(["lsof", "-ti", "tcp:%d" % PORT],
                                 capture_output=True, text=True).stdout
            if out.strip():
                return int(out.split()[0])
    except (OSError, ValueError):
        pass
    return None


def current_pid():
    """Pid from the file if it is still alive, otherwise whatever holds the port."""
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if pid_alive(pid):
                return pid
        except ValueError:
            pass
        PID_FILE.unlink(missing_ok=True)
    return pid_on_port()


def port_in_use():
    with socket.socket() as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", PORT)) == 0


def start():
    pid = current_pid()
    if pid:
        print("Already running (pid %d) at %s" % (pid, URL))
        return
    if port_in_use():
        sys.exit("Port %d is in use by something this script did not start." % PORT)

    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT),
         "--bind", "127.0.0.1", "--directory", str(ROOT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    PID_FILE.write_text(str(process.pid))
    print("Serving %s at %s (pid %d)" % (ROOT.name, URL, process.pid))
    print("Stop it with: make stop")


def stop():
    pid = current_pid()
    if not pid:
        print("Not running.")
        PID_FILE.unlink(missing_ok=True)
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        if WINDOWS:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                           capture_output=True)
        else:
            raise
    PID_FILE.unlink(missing_ok=True)
    print("Stopped (pid %d)." % pid)


def status():
    pid = current_pid()
    print("Running at %s (pid %d)" % (URL, pid) if pid else "Not running.")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    handler = {"start": start, "stop": stop, "status": status}.get(action)
    if not handler:
        sys.exit("Usage: serve.py start|stop|status")
    handler()
