import os

GIT_DIR = ".mygit"

def init():
    try:
        os.makedirs(GIT_DIR)
    except Exception as e:
        pass