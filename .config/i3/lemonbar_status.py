from collections import namedtuple
from datetime import datetime
from itertools import groupby
from time import sleep
import re
import socket
import subprocess
import psutil

# ---AESTHETICS---
GEOMETRY = 'x38+0+0'
FONT = 'GohuFont Nerd Font-10'
FONT2 = 'Font Awesome 5 Free-8'
DELAY = 0.2

# ---COLORS---
FG_BODY_NORMAL = '#4979db'
FG_HEADER_NORMAL = '#c251bd'

BG_BODY_NORMAL = '[100]#000000'
BG_HEADER_NORMAL = '[100]#000000'

FG_LOW_BATTERY = '#4979db'
BG_LOW_BATTERY = '[100]#000000'

BG_BAR = '[100]#000000'

# ---ICONS---
NOBATT = "\uf244"
QUARTERBATT = "\uf243"
HALFBATT = "\uf242"
THREEQUARTERBATT = "\uf241"
FULLBATT = "\uf240"
CHARGING = "\uf0e7"

NOVOL = "\uf026"
LOWVOL = "\uf027"
HIGHVOL = "\uf028"

CONNECTED = '\uf1eb'
NOTCONNECTED = "\uf06a"

CALENDAR = "\uf073"
CLOCK = "\uf017"

# ---EVERYTHING ELSE---
def format_fg(color): return '%{F' + color + '}'

def format_bg(color): return '%{B' + color + '}'

FG_BODY_NORMAL = format_fg(FG_BODY_NORMAL)
FG_HEADER_NORMAL = format_fg(FG_HEADER_NORMAL)

BG_BODY_NORMAL = format_bg(BG_BODY_NORMAL)
BG_HEADER_NORMAL = format_bg(BG_HEADER_NORMAL)

FG_LOW_BATTERY = format_fg(FG_LOW_BATTERY)
BG_LOW_BATTERY = format_bg(BG_LOW_BATTERY)

CENTER = '%{c}'
LEFT = '%{l}'
RIGHT = '%{r}'
SEPARATOR = '  '
BATTERY_DIR = '/sys/class/power_supply/BAT0'
cycle_num = 0

Section = namedtuple('Section', ('alignment', 'fg_header', 'bg_header', 'header','fg_body', 'bg_body', 'body'))

def get_stdout(command):
    pipe = subprocess.Popen(command.split(' '),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    return str(pipe.stdout.read())

def status_datetime():
    return datetime.now().strftime('%d/%m %H:%M')

def status_volume():
    data = get_stdout("amixer get Master")
    return int(data.split('\\n')[-2].split(' ')[-2][1:-2]) if data[-5] == 'n' else 0 

def status_battery_level():
    with open(BATTERY_DIR + '/capacity') as f:
        return int(f.readlines()[0])

def status_battery_status(lvl):
    with open(BATTERY_DIR + '/status') as f:
        if f.readlines()[0][0] == 'D':
            if lvl <= 15:
                return NOBATT
            elif lvl <= 25:
                return QUARTERBATT
            elif lvl <= 50:
                return HALFBATT
            elif lvl <= 75:
                return THREEQUARTERBATT
            elif lvl <= 100:
                return FULLBATT
        else:
            return CHARGING

def status_connected():
    try:
        socket.create_connection(('www.google.com', 80))
    except OSError:
        return False
    return True

def status_network(): 
    return get_stdout('iwconfig').split('\\n')[0].split('ESSID:')[1].strip()[1:-1]


def sections_to_string(sections, separator):
    display_string = ''
    # Separate into left, center and right groups
    groups = groupby(sections, lambda s: s.alignment)
    for sections in groups:
        group_string = format_bg(BG_BAR)
        sections = [i for i in sections[1]]

        for idx, s in enumerate(sections):
            group_string += (s.alignment if idx == 0 else '') + \
                s.fg_header + s.bg_header + \
                            (' ' if s.header else '') + \
                s.header + ' ' + \
                s.fg_body + s.bg_body + s.body
            if idx < len(sections) - 1:
                group_string += separator
            display_string += group_string

    return display_string + '  '

def write_bar(bar, display_string):
    bar.stdin.write((display_string + '\n').encode('utf-8'))
    try:
        bar.stdin.flush()
    except BrokenPipeError:
        # Process killed
        exit()

def run():
    global cycle_num
    status = subprocess.Popen(['lemonbar', '-f', FONT, '-f',
                               FONT2, '-p', '-g', GEOMETRY,
                               '-o', '1', '-B', BG_BAR],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE)
    while True:
        datetime = status_datetime().split(' ')
        datetime = CALENDAR + " " + \
            datetime[0] + "  " + CLOCK + " " + datetime[1]
        volume = status_volume()
        battery_level = status_battery_level()
        battery_status = status_battery_status(battery_level)

        low_battery = battery_level <= 15 and battery_status != CHARGING
        high_volume = NOVOL if volume == 0 else (LOWVOL if volume <= 60 else HIGHVOL)
        # run expensive network operations only once in a while
        if cycle_num % 40 == 0:
            connected = status_connected()
            if connected:
                network = status_network()
            cycle_num = 0

        network_status = CONNECTED if connected else NOTCONNECTED

        fg_header = (FG_LOW_BATTERY if low_battery else FG_HEADER_NORMAL)
        bg_header = (BG_LOW_BATTERY if low_battery else BG_HEADER_NORMAL)
        fg_body = (FG_LOW_BATTERY if low_battery else FG_BODY_NORMAL)
        bg_body = (BG_LOW_BATTERY if low_battery else BG_BODY_NORMAL)

        sections_status = [
            #Section(LEFT, fg_header, bg_header,
            #       str(workspaces), fg_body, bg_body, ''),
            Section(CENTER, fg_header, bg_header,
                    str(datetime), fg_body, bg_body, ''),
            Section(RIGHT, fg_header, bg_header,
                    high_volume, fg_body, bg_body, '{}%'.format(volume)),
            Section(RIGHT, fg_header, bg_header,
                    battery_status, fg_body, bg_body, '{}%'.format(battery_level)),
            Section(RIGHT, fg_header, bg_header,
                    network_status, fg_body, bg_body, (network if connected else '-'))
        ]
        display_string = sections_to_string(sections_status, SEPARATOR)
        write_bar(status, display_string)

        sleep(DELAY)
        cycle_num += 1

if __name__ == '__main__': 
    run()
