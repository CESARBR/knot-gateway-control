#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause

import os
import sys
import signal
import lockfile
import logging
import argparse
import dbus
import dbus.service
import dbus.mainloop.glib
import gobject as GObject
import daemon

from control import Control

mainloop = None

logging.basicConfig(format='[%(levelname)s] %(funcName)s: %(message)s\n',
                    stream=sys.stderr, level=logging.INFO)

def quit_cb(signal_number, stack_frame):
    logging.info("Terminate with signal %d" % signal_number)
    mainloop.quit()

def main():
    global mainloop

    parser = argparse.ArgumentParser(description="KNoT DBUS-Control Daemon")
    parser.add_argument("-w", "--working-dir", metavar="<path>",
                        default="/usr/local/bin",
                        type=str,
                        help="Daemon working directory")
    parser.add_argument("-p", "--pid-filepath", metavar="<path/control>",
                        default="/tmp/control", type=str,
                        help="PID file path and name")
    parser.add_argument("-n", "--detach-process", action="store_false",
                        help="Detached process")
    args = parser.parse_args()

    context = daemon.DaemonContext(
        working_directory=args.working_dir,
        umask=0o002,
        detach_process=args.detach_process,
        pidfile=lockfile.FileLock(args.pid_filepath),
        signal_map={signal.SIGTERM: quit_cb, signal.SIGINT: quit_cb},
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    with context:
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        control = Control()
        control.start()

        mainloop = GObject.MainLoop()

        mainloop.run()

if __name__ == "__main__":
    main()
