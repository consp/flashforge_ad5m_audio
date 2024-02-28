from MIDI import MIDIFile
from time import sleep
import signal
import sys
import threading
import argparse

DEBUG = False

pwm = None

# needed due to how it's played
class PWMAudio:
    chip = 0
    device = 0
    PWMCLASS = "/sys/class/pwm/pwmchip%d/pwm%d/%s"
    ENABLE = "enable"
    PERIOD = "period"
    DUTY_CYCLE = "duty_cycle"

    DC = 0.5  # fixed
    enabled = False

    def __init__(self, chip, device):
        self.chip = chip
        self.device = device
        self.disable()

    def pwmdevice(self, end):
        return self.PWMCLASS % (self.chip, self.device, end)

    def enable(self, enable=True):
        self.enabled = enable
        
        if self.period == 0:  # period needs to be set otherwise errors will be thrown
            self.set(1000)
        with open(self.pwmdevice(self.ENABLE), "wb") as f:
            f.write(b"1" if enable else b"0")
            f.flush

    def disable(self):
        self.enable(enable=False)

    @property
    def period(self):
        with open(self.pwmdevice(self.PERIOD), "rb") as f:
            return int(f.read())

    @period.setter
    def period(self, period):
        with open(self.pwmdevice(self.PERIOD), "wb") as f:
            f.write(b"%d" % period)
            f.flush()

    @property
    def duty_cycle(self):
        with open(self.pwmdevice(self.DUTY_CYCLE), "rb") as f:
            return int(f.read())

    @duty_cycle.setter
    def duty_cycle(self, dc):
        with open(self.pwmdevice(self.DUTY_CYCLE), "wb") as f:
            f.write(b"%d" % dc)
            f.flush()

    def set(self, frequency):
        period = 1000000000 / frequency
        dc = int(period * self.DC)
        if period < self.duty_cycle:
            self.duty_cycle = dc
            self.period = period
        else:
            self.period = period
            self.duty_cycle = dc

    def midinote(self, note, reference=440):
        frequency = midinumber_to_frequency(note, reference) 
        self.set(frequency)

def midinumber_to_frequency(number, reference=440):
    return (reference / 32) * (2 ** ((number - 9) / 12))

def midinote_to_number(note, octave):
    m = {
        'cb': -1,
        'c': 0,
        'c#': 1,
        'db': 1,
        'd': 2,
        'd#': 3,
        'eb': 3,
        'e': 4,
        'f': 5,
        'f#': 6,
        'gb': 6,
        'g': 7,
        'g#': 8,
        'ab': 8,
        'a': 9,
        'a#': 10,
        'bb': 10,
        'b': 11,

    }
    return m[note] + (octave+1) * 12




def play(filename, track, channel):
    def work(filename, track, channel):
        midi = MIDIFile(filename)
        midi.parse()
        track = midi.tracks[track]
        track.parse()
        if DEBUG:
            print(midi.division.division)
        tempo = 1 / midi.division.division

        started = False

        for i in range(0, len(track.events)):
            event = track.events[i]
            event_next = track.events[i+1] if i < len(track.events) - 1 else None
            try:
                if event.channel == channel:
                    if event.command == 144:
                        # note on
                        started = True
                        if pwm.enabled:
                            note = event.message.note
                            if DEBUG:
                                print("ON [EN]: %d" % midinote_to_number(note.note, note.octave))
                            pwm.midinote(midinote_to_number(note.note, note.octave))
                        else:
                            note = event.message.note
                            if DEBUG:
                                print("ON: %d" % midinote_to_number(note.note, note.octave))
                            pwm.midinote(midinote_to_number(note.note, note.octave))
                            pwm.enable()

                    elif event.command == 128:
                        # note off 
                        note = event.message.note
                        if DEBUG:
                            print("OFF: %d" % (midinote_to_number(note.note, note.octave)))
                        pwm.disable()
                if event_next and event_next.time != event.time and started:  # just continue until a note is played
                    sleep(tempo * (event_next.time - event.time))
            except Exception as e:
                # no channel
                pass
        # silence
        pwm.disable()

    t = threading.Thread(target=work, args=(filename, track, channel))
    t.start()


def main():
    parser = argparse.ArgumentParser(
            prog="FF AD5M Audio 'player'",
            description='This program can either play a midi file, single track, single note, single chanel or a frequency for a specific duration',
            epilog="See https://github.com/xblax/flashforge_adm5_klipper_mod and https://github.com/consp/flashforge_adm5_audio")

    parser.add_argument('mode', type=str, help="Either midi or freq", choices=['midi', 'freq', 'disable'])
    parser.add_argument('-f', '--frequency', type=int, help="Frequency", default=440)
    parser.add_argument('-d', '--duration', type=float, help="Duration of frequency", default=1.0)
    parser.add_argument('-t', '--track', type=int, help="Track of midifile to play", default=0)
    parser.add_argument('-c', '--channel', type=int, help="Channel of track to play", default=0)
    parser.add_argument('-m', '--midifile', type=str, help="Midi filename")

    global pwm
    pwm = PWMAudio(0, 6)

    def signal_handler(sig, frame):
        pwm.disable()
        sys.exit(0)

    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), signal_handler)

    args = parser.parse_args()
    if args.mode == "disable":
        pwm.disable()
    elif args.mode == "freq":
        pwm.set(args.frequency)
        pwm.enable()
        sleep(args.duration)
        pwm.disable()
    elif args.mode == 'midi':
        if args.midifile is None:
            print("--midifile/-m needs to be set")
            exit(1)
        print("Loading %s ..." % args.midifile)
        play(args.midifile, args.track, args.channel)

if __name__ == '__main__':
    main()
