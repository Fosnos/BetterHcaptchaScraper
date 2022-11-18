import string, random, json; from base64 import b64decode
from os.path import dirname

settings = json.load(open(dirname(__file__) + '\\settings.json'));

def random_widget_id():
    widget_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(10, 12)))
    return widget_id

def get_latest_version():
    return settings["hcaptcha_version"]

def parse_jsw_data(data):
    fields = data.split(".")
    return {
        "header": json.loads(b64decode(fields[0])),
        "payload": json.loads(b64decode(fields[1] + ("=" * ((4 - len(fields[1]) % 4) % 4)))),
        "signature": b64decode(fields[2].replace("_", "/").replace("-", "+")  + ("=" * ((4 - len(fields[1]) % 4) % 4))),
        "raw": {
            "header": fields[0],
            "payload": fields[1],
            "signature": fields[2]
        }
    }

def hostname_from_url(url):
    return url.split("://", 1)[1].split("/", 1)[0].lower()

def is_main_process():
    proc = __import__("multiprocessing").current_process()
    return proc.name == "MainProcess"

def format_proxy(proxy):
    if '@' in proxy:
        return proxy
    elif len(proxy.split(':')) == 2:
        return proxy
    else:
        if '.' in proxy.split(':')[0]:
            return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
        else:
            return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])