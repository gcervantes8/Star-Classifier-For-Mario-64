# -*- coding: utf-8 -*-
"""
Created on Sat May 25 10:06:24 2019

@author: Gerardo Cervantes
"""

from splitter import Splitter
#For testing split keys

split_keys = ['{PGUP}', '{BKSP}', '{F4}']

if __name__ == "__main__":
    splitter = Splitter()
    splitter.split('Livesplit', '{pgup}', 0)

