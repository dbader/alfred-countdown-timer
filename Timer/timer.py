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
    interval = parse_time()
    minutes = interval / 60
    seconds = interval % 60

    label = ' '.join(sys.argv[2:])
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


def parse_time():
    """Parse and return the desired countdown duration in seconds from
    the commandline.
    """
    try:
        duration = sys.argv[1]
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


def swizzle(*args):
    """
    Decorator to override an ObjC selector's implementation with a
    custom implementation ("method swizzling").

    Use like this:

    @swizzle(NSOriginalClass, 'selectorName')
    def swizzled_selectorName(self, original):
        --> `self` points to the instance
        --> `original` is the original implementation

    Originally from http://klep.name/programming/python/

    (The link was dead on 2013-05-22 but the Google Cache version works:
    http://goo.gl/ABGvJ)
    """
    cls, SEL = args

    def decorator(func):
        old_IMP = cls.instanceMethodForSelector_(SEL)

        def wrapper(self, *args, **kwargs):
            return func(self, old_IMP, *args, **kwargs)

        new_IMP = objc.selector(wrapper, selector=old_IMP.selector,
                                signature=old_IMP.signature)
        objc.classAddMethod(cls, SEL, new_IMP)
        return wrapper

    return decorator


@swizzle(objc.lookUpClass('NSBundle'), 'bundleIdentifier')
def swizzled_bundleIdentifier(self, original):
    """Swizzle [NSBundle bundleIdentifier] to make NSUserNotifications
    work.

    To post NSUserNotifications OS X requires the binary to be packaged
    as an application bundle. To circumvent this restriction, as it would
    be difficult (impossible?) to implement in an Alfred Extension,
    we modify `bundleIdentifier` to return a fake bundle identifier.

    This method currently returns the bundle identifier of the Finder.
    Because of that the notification displays the Finder's icon. This
    isn't really ideal but at least it makes notifications work again.

    Original idea for this approach by Norio Numura:
        https://github.com/norio-nomura/usernotification
    """
    return 'com.apple.finder'


def notify(title, subtitle=None):
    """Display a NSUserNotification on Mac OS X >= 10.8"""
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
    if not NSUserNotification or not NSUserNotificationCenter:
        print('no nsusernotification')
        return

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(str(title))
    if subtitle:
        notification.setSubtitle_(str(subtitle))

    notification_center = NSUserNotificationCenter.defaultUserNotificationCenter()
    notification_center.deliverNotification_(notification)


def play_sound(filename):
    """Play the given sound file using the `afplay` command line utility."""
    subprocess.Popen(['afplay', filename])


if __name__ == '__main__':
    main()
