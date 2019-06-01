# -*- coding: utf-8 -*-
"""
Created on Wed May 29 18:23:56 2019

@author: Jerry C
"""

from pynput import keyboard
import re


class CaptureKeys:
    
    #Function to be called after on_press is called and key is captured, arg is key
    fn = None
    
    #Returns false to stop fn from looking for more keys
    #From https://stackoverflow.com/questions/11918999/key-listeners-in-python
    def _on_press(self, key):
        try: k = key.char # single-char keys
        except: k = key.name # other keys
        if key == keyboard.Key.esc: return 'Esc' # stop listener
        print('Key pressed: ' + k)
        if self.fn != None:
            self.fn(key)
        return True # remove this if want more keys
    
    def capture_key(self):
        lis = keyboard.Listener(on_press=self._on_press)
        lis.start() # start to listen on a separate thread

    def to_windows_key(input_key):
        #Capslock doesn't work?? It's strange and sometimes sends the key 3 times
        
        #If is an f key. ex. f1, f2
        if re.match('f[0-9]?[0-9]', input_key):
            input_key = input_key[1:] #Remove f letter
            return '{F' + input_key + '}'
        
        if re.match('^[a-z]$', input_key):
            return '{' + input_key + '}'
        
        cap_key_to_windows = {
		'page_up' : '{PGUP}',
		'page_down' : '{PGDN}',
		'backspace' : '{BKSP}',
		'\'' : '{\'}',
		'left' : '{LEFT}',
		'right' : '{RIGHT}',
        'down' : '{DOWN}',
        'up' : '{UP}'
        
	}
        
        pass
        
if __name__ == "__main__":
    cap_keys = CaptureKeys()
    cap_keys.capture_key()