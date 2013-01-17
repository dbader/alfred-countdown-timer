#!/usr/bin/env python

"""
A simple countdown timer command for Alfred.app that
uses Mountain Lion User Notifications.

Copyright (c) 2013 Daniel Bader (http://dbader.org)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys
import time
import subprocess
import objc

def main():
    minutes = read_time()
    notify('Timer set to %i %s' % (minutes, 'minute' if minutes == 1 else 'minutes'))

    time.sleep(minutes * 60)

    notify("Time's up!", '%i %s passed.' % (minutes, 'minute has' if minutes == 1 else 'minutes have'))
    play_sound('alarm.m4a')

def read_time():
    """Parse and return the desired countdown time in minutes from the commandline."""
    try:
        time = sys.argv[1]
        if ':' in time:
            # Minutes and seconds, e.g. "5:30"
            minutes, seconds = time.split(':')
            return float( int(minutes) + int(seconds) / 60.0 )
        else:
            # Just minutes, e.g. "1.5"
            return float(time)
    except:
        show_usage()
        sys.exit(1)

def show_usage():
    notify('Timer usage', 'timer [minutes]')

def notify(title, subtitle=None):
    """Display a NSUserNotification on Mac OS X >= 10.8"""
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    if not NSUserNotification or not NSUserNotificationCenter:
        return

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    if subtitle:
        notification.setSubtitle_(str(subtitle))

    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

def play_sound(filename):
    subprocess.Popen(['afplay', filename])

if __name__ == '__main__':
    main()
