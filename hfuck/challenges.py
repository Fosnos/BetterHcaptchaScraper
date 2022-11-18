from .exceptions import ChallengeError, GetCaptchaRejected, RequestRejected; from os.path import dirname
from typing import Iterator, List, Union; from .mouse_curves import *; from . import xrequests, logger, utils
from random import randint; from .proofs import get_proof;
import string, json, random, urllib, httpx, threading; 

class Challenge:
    _version_id = utils.get_latest_version();
    def __init__(self, site_key: str, site_url: str, data: Union[dict, None] = None, proxy=None, ssl_context=True):
        self._site_key = site_key; self._site_url = site_url
        self._site_hostname = utils.hostname_from_url(site_url)
        self._custom_data = data or {}
        self._widget_id = utils.random_widget_id()

        if proxy != None: proxy = utils.format_proxy(proxy)
        
        self.session = xrequests.Session(timeout=None, proxy=proxy, ssl_context=True)
        self.settings = json.load(open(dirname(__file__) + '\\settings.json'));
        self.id = None; self.token = None; self.config = None; self.mode = None; 
        self.question = None; self.tiles = []; self._answers = {}; self._start = 0; self.task_thread = []



    @property
    def _motionData(self) -> dict:
        return {
            "st": self._start + 1000 + randint(10, 100),
            "v": 1,
            "topLevel": {
                "inv": False,
                "st": self._start,
                "sc": {
                    "availWidth": 1920, "availHeight": 1022, "width": 1920, "height": 1080, "colorDepth": 24,
                    "pixelDepth": 24, "availLeft": 0, "availTop": 18, "onchange": None, "isExtended": True
                },
                "nv": {
                    "vendorSub": "", "productSub": "20030107", "vendor": "Google Inc.", "maxTouchPoints": 0,
                    "scheduling": {}, "userActivation": {}, "doNotTrack": "1", "geolocation": {}, "connection": {},
                    "pdfViewerEnabled": True, "webkitTemporaryStorage": {}, "webkitPersistentStorage": {},
                    "hardwareConcurrency": 8, "cookieEnabled": True, "appCodeName": "Mozilla", "appName": "Netscape",
                    "appVersion": self.settings["appVersion"],
                    "userAgent": self.settings["userAgent"],
                    "platform": "Win32", "product": "Gecko", "language": "en-US", "languages": ["en-US", "en"],
                    "onLine": True, "webdriver": False, "bluetooth": {}, "clipboard": {}, "credentials": {},
                    "keyboard": {}, "managed": {}, "mediaDevices": {}, "storage": {}, "serviceWorker": {},
                    "virtualKeyboard": {}, "wakeLock": {}, "deviceMemory": 8, "ink": {}, "hid": {}, "locks": {},
                    "mediaCapabilities": {}, "mediaSession": {}, "permissions": {}, "presentation": {}, "serial": {},
                    "usb": {}, "windowControlsOverlay": {}, "xr": {},
                    "userAgentData": {
                        "brands": [
                            {"brand": "Chromium", "version": "106"},
                            {"brand": "Google Chrome", "version": "106"},
                            {"brand": "Not;A=Brand", "version": "99"}
                        ],
                        "mobile": False,
                        "platform": "Windows"
                    },
                    "plugins": [
                        "internal-pdf-viewer",
                        "internal-pdf-viewer",
                        "internal-pdf-viewer",
                        "internal-pdf-viewer",
                        "internal-pdf-viewer"
                    ]
                },
                "dr": "", "exec": False, "wn": [], "wn-mp": 0, "xy": [], "xy-mp": 0,
            },
            "session": [],
            "widgetList": [],
            "widgetId": "",
            "href": self._site_key,
            "prev": {"escaped": False, "passed": False, "expiredChallenge": False, "expiredResponse": False}
        }
    
    def _getMotionData(self) -> dict:
        j = self._motionData

        mc = MotionController(j["st"], (randint(0, 480), randint(0, 270)))
        mc.move(randint(1440, 1920), randint(810, 1022), 35)
        mc.click()
        j.update(**mc.get())

        tmm = MotionController(self._start + 1000 + randint(100, 150), (randint(0, 480), randint(0, 270)))
        tmm.move(randint(1440, 1920), randint(810, 1022), 70)

        j["topLevel"].update(tmm.get(md=False, mu=False))
        return j
    
    
    def get_task(self):
        payload = { 'v': utils.get_latest_version(), 'host': self._site_hostname, 'sitekey': self._site_key, 'sc': '1', 'swa': '1' }
        payload = urllib.parse.urlencode(payload)

        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.session.headers['Content-Length'] = str(len(payload))
        
        response = self.session.post(f'https://hcaptcha.com/checksiteconfig?{payload}', data=payload, headers=self.settings['headers']).json()
        return response['c']
    
    def get_captcha(self, data, n):
        del self.session.headers['Content-Length']

        payload = { "v": utils.get_latest_version(), "host": self._site_hostname, "sitekey": self._site_key, "hl": "en", "n":  n, "c": json.dumps(data), "motionData": self._getMotionData(), **self._custom_data }
        payload = urllib.parse.urlencode(payload)


        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.session.headers['Content-Length'] = str(len(payload))

        captcha = self.session.post(f"https://hcaptcha.com/getcaptcha/?s={self._site_key}", data=payload, headers=self.settings['headers'])
        if captcha.status_code == 200:
            return captcha.json()
        else:
            raise GetCaptchaRejected('GetCaptcha data was rejected.')

    def get_images(self):
        self._start = int(time() * 1000 - 2000)
        
        task_data = self.get_task()
        
        n = get_proof(task_data['req']); task = self.get_captcha(task_data, n)

        try:
            self.topic = task["requester_question"]["en"].split('Please click each image containing a ')[1].split('.')[0]
        except:
            self.topic = task["requester_question"]["en"].split('Please click each image containing an ')[1].split('.')[0]
        
        self.id = task['key'];

        return { 'topic': self.topic, 'question': task["requester_question"]["en"], 'images': task['requester_question_example'] }
