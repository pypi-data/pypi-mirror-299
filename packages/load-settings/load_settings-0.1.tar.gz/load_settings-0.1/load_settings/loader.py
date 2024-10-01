# load_settings/loader.py

import os
import importlib.util

def find_and_import_settings_menu(search_dir):
    """
    Search for settings_menu.py in the specified directory and its subdirectories.
    Dynamically imports and returns the module if found.
    
    :param search_dir: Directory to search for settings_menu.py
    :return: The imported settings_menu module or None if not found
    """
    for root, dirs, files in os.walk(search_dir):
        if 'settings_menu.py' in files:
            settings_path = os.path.join(root, 'settings_menu.py')
            print(f"Found settings_menu.py at: {settings_path}")
            
            # Dynamically import the settings_menu.py module
            spec = importlib.util.spec_from_file_location("settings_menu", settings_path)
            settings_menu = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(settings_menu)
            
            return settings_menu
    
    print("settings_menu.py not found.")
    return None
