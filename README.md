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

# License

This work is licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)

# Known issues

* Using verbose can significanly slow down your playback on slower machines
* Midi files get load into memory completely, if you have little available be wary of large midi files.
* Since the pwm device is monotone, channels with polytone audio will not sound proper. There is no way to do anything about this, seek monotone channels.
* Only pwmchip0 can be used at this time, the FF Ad5M only has one.
