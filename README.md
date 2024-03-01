# FlashForge Adventurer 5M Audio library

Can be used to play midi files and frequencies on the speaker of the FlashForge Adventurer 5M (pro).
Can also be used to play on other linux devices which use a simple PWM driver as audio device.

Note: midi files online are a mess, you might have to seek a while. Try finding the channel with piano or other keytype instrument, usually works best.

Usage:

```
$ audio --help
usage: FF AD5M Audio 'player' [-h] [-f FREQUENCY] [-d DURATION] [-c CHANNEL] [-m MIDIFILE] [-p PWM] [-v] [--nopwm]
                              {midi,freq,disable}

This program can either play a midi file, single track, single note, single chanel or a frequency for a specific duration

positional arguments:
  {midi,freq,disable}   Either midi or freq

options:
  -h, --help            show this help message and exit
  -f FREQUENCY, --frequency FREQUENCY
                        Frequency
  -d DURATION, --duration DURATION
                        Duration of frequency
  -c CHANNEL, --channel CHANNEL
                        Channel of track to play
  -m MIDIFILE, --midifile MIDIFILE
                        Midi filename
  -p PWM, --pwm PWM     pwm device to use
  -v, --verbose         Be verbose (might slow down playback in case of heavy pitch changes)
  --nopwm               Disable PWM driver, used for testing midi file reading

See https://github.com/xblax/flashforge_adm5_klipper_mod and https://github.com/consp/flashforge_adm5_audio
```

Play a midi file:
```
$ audio midi -m level1.mid -c 6 -p 6 -v
audio midi -m level1.mid -c 1 -p 6 -v
Opening pwm  6
Loading level1.mid ...
Looking for track 1
Copyright  © 1993, id Software
Copyright  © 1994, Microsoft
Tempo change: 560 1000000 0
Note ON: 40
Note ON: 36
Note ON: 40
Note ON: 41
Note ON: 40
Rest:  0.04285714285714286
Note OFF: 40
Rest:  0.049999999999999996
Note OFF: 40
Rest:  0.02857142857142857
Note OFF: 36
Rest:  0.014285714285714285
Note ON: 40
Rest:  0.007142857142857143
Note OFF: 40
Rest:  0.007142857142857143
Note OFF: 41
Rest:  0.12142857142857143
...
```

Play a frequency for a duration:
```
$ audio freq -f 440 -d 1
< 440hz will sound for 1 second >
```

Disable pwm chanel
```
$ audio disable
```


# In code

If you want to use the simple pwm device in python:

```
$ python3
>>> from audio import PWMAudio
>>> p = PWMAudio(0, 6) # chip, pwm number
>>> p.set(1000) # set frequency to 1000hz
>>> p.enable() # enable
>>> p.disable() # disable (e.g. when your ears start bleeding)
```

# License

This work is licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)

# Known issues

* Using verbose can significanly slow down your playback on slower machines
* Midi files get load into memory completely, if you have little available be wary of large midi files.
* Since the pwm device is monotone, channels with polytone audio will not sound proper. There is no way to do anything about this, seek monotone channels.
* Only pwmchip0 can be used at this time, the FF Ad5M only has one.
