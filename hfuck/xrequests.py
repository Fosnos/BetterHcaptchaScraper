import httpx, certifi, json; from random import randint; from os.path import dirname

settings = json.load(open(dirname(__file__) + '\\settings.json'));
class SSLContext(object):
    def GetContext():
        ciphers_top = "ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM"
        ciphers_mid = 'DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES'
        cl = ciphers_mid.split(":")
        cl_len = len(cl)
        els = []
        
        for i in range(cl_len):
            idx = randint(0, cl_len-1)
            els.append(cl[idx])
            del cl[idx]
            cl_len-=1
        
        ciphers2 = ciphers_top+":".join(els)
        context = httpx.create_ssl_context()
        context.load_verify_locations(cafile=certifi.where())
        context.set_alpn_protocols(["h2"])
        context.minimum_version.MAXIMUM_SUPPORTED
        CIPHERS = ciphers2
        context.set_ciphers(CIPHERS)
        
        ciphers2
    
    def GetTransport():
        return httpx.HTTPTransport(retries=3)


def Session(timeout, proxy, ssl_context=True):
    if proxy != None:
        proxy = f"http://{proxy}"
    if ssl_context:
        return httpx.Client(proxies=proxy, http2=True, timeout=timeout, verify=SSLContext.GetContext(), transport=SSLContext.GetTransport(), headers=settings['headers'])
    else:
        return httpx.Client(proxies=proxy, timeout=timeout, headers=settings['headers'])