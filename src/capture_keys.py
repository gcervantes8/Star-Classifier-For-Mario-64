# -*- coding: utf-8 -*-
"""
Created on Wed May 29 18:23:56 2019

@author: Gerardo Cervantes
"""

from pynput import keyboard
import re


class CaptureKeys:

    # Function to be called after on_press is called and key is captured, arg is key
    fn = None
    
    # Returns false to stop fn from looking for more keys
    # From https://stackoverflow.com/questions/11918999/key-listeners-in-python
    def _on_press(self, key):
        try:
            k = key.char  # single-char keys
        except AttributeError:
            k = self.to_windows_key(key)
        if key == keyboard.Key.esc:
            return 'Esc'  # stop listener
        print('Key pressed: ' + k)
        if self.fn:
            self.fn(k)
        return True  # remove this if want more keys
    
    def capture_key(self):
        lis = keyboard.Listener(on_press=self._on_press)
        lis.start()  # start to listen on a separate thread

    # Returns String with the windows key, if no windows key was found, then return name of key inputted
    def to_windows_key(self, input_key):
        key_name = input_key.name
        print('Input key: %s' % input_key)
        print('Name:%s' % key_name)

        # If is an f key. ex. f1, f2
        if re.match('f[0-9]?[0-9]', key_name):
            key_name = key_name[1:]  # Remove f letter
            return '{F' + key_name + '}'
        
        if re.match('^[a-z]$', key_name):
            return '{' + key_name + '}'

# https://github.com/moses-palmer/pynput/blob/master/lib/pynput/keyboard/_base.py has the input keys
# https://docs.microsoft.com/en-us/dotnet/api/system.windows.forms.sendkeys?redirectedfrom=MSDN&view=netframework-4.7.2
        cap_key_to_windows = {'page_up': '{PGUP}',
                              'page_down': '{PGDN}',
                              'backspace': '{BKSP}',
                              '\'': '{\'}',
                              'left': '{LEFT}',
                              'right': '{RIGHT}',
                              'down': '{DOWN}',
                              'up': '{UP}',
                              'ctrl': '^',
                              'ctrl_l': '^',
                              'ctrl_r': '^',
                              'alt': '%',
                              'alt_l': '%',
                              'alt_r': '%',
                              'alt_gr': '%',
                              'shift': '+',
                              'shift_l': '+',
                              'shift_r': '+',
                              'space': '{SPACE}',
                              'end': '{END}',
                              'enter': '{ENTER}',
                              'home': '{HOME}',
                              'insert': '{INSERT}',
                              'pause': '{BREAK}',
                              'delete': '{DELETE}',
                              'caps_lock': '{CAPSLOCK}',
                              'num_lock': '{NUMLOCK}',
                              'print_screen': '{PRTSC}',
                              'scroll_lock': '{SCROLLLOCK}',
                              'tab': '{TAB}',
                              'cmd': '{LWIN}',
                              'cmd_l': '{LWIN}',
                              'cmd_r': '{RWIN}',
                              'media_play_pause': '{MEDIA_PLAY_PAUSE}',
                              'media_volume_mute': '{VOLUME_MUTE}',
                              'media_volume_up': '{VOLUME_DOWN}',
                              'media_volume_down': '{VOLUME_UP}',
                              'media_previous': '{MEDIA_PREV}',
                              'media_next': '{MEDIA_NEXT}'
                              }
        if key_name in cap_key_to_windows:
            return cap_key_to_windows[key_name]
        return key_name


if __name__ == "__main__":
    cap_keys = CaptureKeys()
    cap_keys.capture_key()
