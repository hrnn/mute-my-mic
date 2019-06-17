import os
import signal
import sys
import subprocess
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'mute-my-mic-indicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('sample_icon.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    # quit
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    #mute

    item_mute = gtk.MenuItem('Mute/Unmute')
    item_mute.connect('activate', toggle)
    menu.append(item_mute)

    menu.show_all()
    return menu

def check_mic():
    process = subprocess.Popen(['amixer -D pulse sget Capture'], shell=True, stdout=subprocess.PIPE)
    output= process.communicate()[0].split("\n")
    is_mute = False
    for line in output:
        data = line.lower()
        if ('capture' in data) and '[off]' in data:
            is_mute = True

    return is_mute

def toggle(source):
    mute_command   = 'amixer -D pulse sset Capture toggle'
    p = subprocess.Popen([mute_command], shell=True, stdout=subprocess.PIPE)
    is_mute = check_mic()
    if is_mute:
        message = "mic activated"
        is_mute = False
    else:
        message = "mic deactivated"
        is_mute = True

    sys_message(message) #mute was enabled

def sys_message(msg):
    subprocess.call(['notify-send', '-t', '1000', '{}'.format(msg)])

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()


