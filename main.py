import os, json, random, time, threading, ctypes, string, hfuck, requests;
from datetime import datetime; from colorama import Fore, Style, init

image_database = []; scraped = 0; duplicate = 0; init()

class Logger:
    def CenterText(var:str, space:int=None): 
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
        print(f'[{current_time}] ({Fore.YELLOW}?{Fore.WHITE}) {text}')
        lock.release()
    
    def Debug(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock = threading.Lock()
        lock.acquire()
        print(f'[{current_time}] [DEBUG] ({Fore.LIGHTBLUE_EX}*{Fore.WHITE}) {text}')
        lock.release()

class Utils(object):
    @staticmethod
    def GetProxy():
      with open('input/proxies.txt', "r") as f:
        return random.choice(f.readlines()).strip()
    
    @staticmethod
    def GetFormattedProxy(proxy):
        if '@' in proxy:
            return proxy
        elif len(proxy.split(':')) == 2:
            return proxy
        else:
            if '.' in proxy.split(':')[0]:
                return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
            else:
                return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])

class Scraper(object):
    def __init__(self, proxy):
        global scraped, duplicate;

        response = hfuck.Challenge(site_key="4c672d35-0701-42b2-88c3-78380b0db560", site_url="https://discord.com", proxy=proxy, ssl_context=True).get_images()
        
        for image in response['images']:
            image_content = requests.get(image).content

            if image_content in image_database:
                Logger.Debug(f'Duplicate Found : {image[:40]}... ({response["topic"]})')
                duplicate += 1
            else:
                image_database.append(image_content)
                image_name = "".join(random.choice(string.ascii_letters) for x in range(10)) + ""; image_folder = f'/data/{response["topic"]}'; image_path = f'data/{response["topic"]}/{image_name}.png'
                
                exists = os.path.isdir(image_folder)
                
                if exists == True:
                    with open(image_path , "wb") as handler:
                        handler.write(image_content)
                        Logger.Success(f'Successfully Scraped : {image[:40]}... ({response["topic"]})')
                        scraped += 1
                else:
                    try:
                        path = os.path.join('./data', f'{response["topic"]}')
                        os.mkdir(path, 0o777)
                    
                        with open(image_path , "wb") as handler:
                            handler.write(image_content)
                            Logger.Success(f'Successfully Scraped : {image[:40]}... ({response["topic"]})')
                            scraped += 1
                    except Exception:
                        with open(image_path , "wb") as handler:
                            handler.write(image_content)
                            Logger.Success(f'Successfully Scraped : {image[:40]}... ({response["topic"]})')
                            scraped += 1
            
            ctypes.windll.kernel32.SetConsoleTitleW(f'[Space Scraper] - Scraped : {scraped} | Duplicates : {duplicate} | Site : https://discord.com | Site Key : 4c672d35-0701-42b2-88c3-78380b0db560')

def run():
    while True:
        proxy = Utils.GetProxy()
        format = Utils.GetFormattedProxy(proxy)
        Scraper(format)

Logger.Question(f'Please Enter The Number Of Threads : ')
thread_amt = int(input(''))
threads = []
for i in range(thread_amt):
     t = threading.Thread(target=run)
     t.start()
     threads.append(t)
for i in range(thread_amt):
    threads[i].join()