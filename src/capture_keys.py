# -*- coding: utf-8 -*-
"""
Created on Wed May 29 18:23:56 2019

@author: Jerry C
"""

from pynput import keyboard



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
        return False # remove this if want more keys
    
    def capture_key(self):
        lis = keyboard.Listener(on_press=self._on_press)
        lis.start() # start to listen on a separate thread

    def to_windows_key(input_key):
        
        pass
        
if __name__ == "__main__":
    cap_keys = CaptureKeys()
    cap_keys.capture_key()