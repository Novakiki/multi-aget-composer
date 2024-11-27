"""Configuration for examples"""
import os
import sys

# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR) 