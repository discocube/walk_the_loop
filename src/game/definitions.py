"""
Where's root?
"""
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(ROOT_DIR, 'icons')


print(ROOT_DIR)