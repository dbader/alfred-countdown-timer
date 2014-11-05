# [A countdown timer extension for Alfred.app](http://dbader.org/blog/alfred-timer-extension)
A simple countdown and pomodoro timer command for [Alfred.app](http://www.alfredapp.com/) that uses Mountain Lion User Notifications.

![Demo screenshot](https://raw.github.com/gismo141/alfred-countdown-timer/master/Resources/screenshot.png)

The extension is described in closer detail on my [blog](http://dbader.org/blog/alfred-timer-extension).

## Benefits
- Helps you make great tea.
- Solves your [Pomodoro](http://en.wikipedia.org/wiki/Pomodoro_Technique) needs.
- Uses Mountain Lion's User Notifications to tell you when time's up.
- Plays a non-intrusive alarm sound.
- Allows you to run multiple timers at the same time.
- Allows you to add an optional label to the timer, e.g. "Laundry is done!". Thanks to [Alexander Lehmann](http://rudairandamacha.blogspot.de) for the suggestion.
- Shows you how to write Alfred extensions in Python.

## Installation
Depending on whether you're running Alfred 1 or Alfred 2 you need different versions of the extension. Please also note that this extension / workflow *requires OS X Mountain Lion (10.8) or greater* to work.

### Alfred 2
- Download [Timer.alfredworkflow](https://github.com/dbader/alfred-countdown-timer/blob/master/Timer.alfredworkflow?raw=true)
- Double-click `Timer.alfredworkflow` to install the extension.

### Alfred 1
- Download [Timer.alfredextension](https://github.com/dbader/alfred-countdown-timer/blob/master/Timer.alfredextension?raw=true)
- Double-click `Timer.alfredextension` to install the extension.

To use this extension you need [Alfred.app](http://www.alfredapp.com/) for OS X and the [Alfred PowerPack](http://www.alfredapp.com/powerpack/).

## Usage

### General

- The general syntax is `timer [minutes] [optional:title]`
- `timer 5` sets a countdown timer that goes off after 5 minutes.
- `timer 0:30` or `timer 0.5` sets a timer that goes off after 30 seconds.
- `timer 40 Laundry is done!` adds an optional title to the timer.
- `timer` displays usage information.

### Pomodoro

The pomodoro-timer does:
- starts a standard timer for the **25 minutes work**
- starts a standard timer for the **5 minutes break** (right after the first finished)
 
To start a pomodoro-timer call `timerp` in Alfred.

![Example for pomodoro-timer](https://raw.github.com/gismo141/alfred-countdown-timer/master/Resources/alfred_call.png)

![Notification Center information for pomodoro-timer](https://raw.github.com/gismo141/alfred-countdown-timer/master/Resources/nc_start_info.png)

![Notification Center information when pomodoro-work-timer finishes](https://raw.github.com/gismo141/alfred-countdown-timer/master/Resources/nc_end_info.png)

![Notification Center information when pomodoro-break-timer finishes](https://raw.github.com/gismo141/alfred-countdown-timer/master/Resources/nc_break_over.png)

##Meta

Daniel Bader – [@dbader_org](https://twitter.com/dbader_org) – mail@dbader.org

Distributed under the MIT license. See ``LICENSE.txt`` for more information.

https://github.com/dbader/alfred-countdown-timer
