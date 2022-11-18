import os, threading
from colorama import init, Fore
from datetime import datetime

def CenterText(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())
    
def Success(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    lock = threading.Lock()
    lock.acquire()
    print(f'[{current_time}] ({Fore.LIGHTGREEN_EX}+{Fore.WHITE}) {text}')
    lock.release()
    
def Error(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    lock = threading.Lock()
    lock.acquire()
    print(f'[{current_time}] ({Fore.RED}-{Fore.WHITE}) {text}')
    lock.release()
    

def Question(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    lock = threading.Lock()
    lock.acquire()
    print(f'[{current_time}] [DEBUG] ({Fore.LIGHTBLUE_EX}*{Fore.WHITE}) {text}')
    lock.release()

def Debug(text):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    lock = threading.Lock()
    lock.acquire()
    print(f'[{current_time}] [DEBUG] ({Fore.LIGHTBLUE_EX}*{Fore.WHITE}) {text}')
    lock.release()
    