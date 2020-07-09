# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 10:37:33 2018

@author: Gerardo Cervantes
"""

import xml.etree.cElementTree as ET
from src.coordinates import Coordinates
from src.hotkeys import Hotkeys


class SharedPreferences():
    
    COORDINATES_TAG = 'coordinates'
    SPLIT_TAG = 'split_key'
    RESET_TAG = 'reset_key'
    ROUTE_TAG = 'route'
    
    def write_preferences(self, file_name, coordinates, route_name, hotkeys):
        xml_str = self.create_xml(coordinates, route_name, hotkeys)        
        with open(file_name, "wb") as f:
            f.write(xml_str)

    def create_xml(self, coordinates, route_name, hotkeys):
        root = ET.Element("root") 
        
        ET.SubElement(root, self.ROUTE_TAG).text = self.to_valid_xml_str(route_name)
        ET.SubElement(root, self.SPLIT_TAG).text = self.to_valid_xml_str(hotkeys.get_split_key())
        ET.SubElement(root, self.RESET_TAG).text = self.to_valid_xml_str(hotkeys.get_reset_key())
        
        xml_coordinates = ET.SubElement(root, self.COORDINATES_TAG)
        x, y, width, height = coordinates.get_coordinates()
        
        ET.SubElement(xml_coordinates, "x").text = str(x)
        ET.SubElement(xml_coordinates, "y").text = str(y)
        ET.SubElement(xml_coordinates, "width").text = str(width)
        ET.SubElement(xml_coordinates, "height").text = str(height)
        
        xml_str = ET.tostring(root, encoding='utf8', method='xml')
        return xml_str
    
    def to_valid_xml_str(self, text):
        if text == '':
            return ' '
        return text
    
    def parse_xml(self, file_name):
        try:
            tree = ET.parse(file_name)
        except FileNotFoundError:
            return None, None, None
        root = tree.getroot()
        route_name = root.find(self.ROUTE_TAG).text
        split_key = root.find(self.SPLIT_TAG).text
        reset_key = root.find(self.RESET_TAG).text
        coordinates_xml = root.find(self.COORDINATES_TAG)
        
        x = coordinates_xml.find("x").text
        y = coordinates_xml.find("y").text
        width = coordinates_xml.find("width").text
        height = coordinates_xml.find("height").text
        
        coordinates = Coordinates()
        coordinates.set_coordinates(x, y, width, height)
        
        hotkeys = Hotkeys()
        hotkeys.set_split_key(split_key)
        hotkeys.set_reset_key(reset_key)
        
        return coordinates, route_name, hotkeys

        
if __name__ == "__main__":
    shared_prefs = SharedPreferences()
    coordinates = Coordinates()
    coordinates.set_coordinates(20, 25, 50, 30)
    hotkeys = Hotkeys()
    file_name = 'example_pref_file.zd'
    shared_prefs.write_preferences(file_name, coordinates, '', hotkeys)
    coordinates, route_name, hotkeys = shared_prefs.parse_xml(file_name)
    print(coordinates)
    print(hotkeys.get_split_key())
    print(hotkeys.get_reset_key())
    print(route_name)
#    xml_str = shared_prefs.create_xml(coordinates, 'Home', 'Other', 'Route')
#    shared_prefs.xml_print(xml_str)
