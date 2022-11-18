from os.path import dirname
import os

def get_proof(req):
    res = os.popen(f'node ./window.js {req}').read()
    return res