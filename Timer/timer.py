#!/usr/bin/env python3

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

import json
import os
import subprocess
import sys
import time


def main(argv):
    interval = parse_time(argv)
    minutes = interval / 60
    seconds = interval % 60

    label = ' '.join(argv[1:])
    title = 'Timer started' + (': %s' % label.capitalize() if label else '.')

    if minutes and seconds:
        notify(title, "I'll notify you in %i:%.2i." % (minutes, seconds))
        passed_time = '%i:%.2i have passed.' % (minutes, seconds)
    elif minutes:
        notify(title, "I'll notify you in %i %s." % (minutes,
               'minute' if minutes == 1 else 'minutes'))
        passed_time = '%i %s passed.' % (minutes,
                      'minute has' if minutes == 1 else 'minutes have')
    else:
        notify(title, "I'll notify you in %i seconds." % seconds)
        passed_time = '%i seconds have passed.' % seconds

    time.sleep(interval)
    notify("Time's up" + (': %s' % label.capitalize() if label else '.'),
           passed_time)
    play_sound('alarm.m4a')


def parse_time(argv):
    """Parse and return the desired countdown duration in seconds from
    the commandline.
    """
    try:
        duration = argv[0]
        if ':' in duration:
            # Minutes and seconds, e.g. "5:30"
            minutes, seconds = duration.split(':')
            return int(minutes) * 60 + int(seconds)
        else:
            # Just minutes, e.g. "1.5"
            return int(float(duration) * 60)
    except:
        show_usage()
        sys.exit(1)


def show_usage():
    notify('Timer usage', 'timer [minutes] [optional: title]')


def notify(title, text=None):
    subprocess.Popen([
        'osascript', 
        '-e', 
        f'''tell application id "com.runningwithcrayons.Alfred" to run trigger "notification" in workflow "org.dbader.alfred.timer" with argument "{title}|||{text}"'''
    ])


def play_sound(filename):
    """Play the given sound file using the `afplay` command line utility."""
    subprocess.Popen(['afplay', filename])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv = sys.argv[1].split()
    else:
        argv = []
    main(argv)
