#!/usr/bin/env python3
import os
from .common import *

def prepre_payloads(known_ips=[],known_payloads_path=None,additionalpayloads=None):
    payloads = []
    if os.path.exists(known_payloads_path):
        for p in open(known_payloads_path,'r').readlines():
            p = p.replace('\n', '')
            payloads.append(p) if not p in payloads else None
    if known_ips:
        newpayloads = []
        for ip in known_ips:
            if validate_ip(ip) and (not ip == "127.0.0.1"):
                newpayloads+= obfuscate_ip(ip)
        payloads+=newpayloads
    if additionalpayloads:
        if os.path.exists(additionalpayloads):
            for p in open(additionalpayloads,'r').readlines():
                p = p.replace('\n', '')
                payloads.append(p) if not p in payloads else None 
    return payloads
    

def prepre_headers(additionalheaders=None,known_headers_path=None):
    headers = []
    if additionalheaders:
        if os.path.exists(additionalheaders):
            for p in open(additionalheaders,'r').readlines():
                p = p.replace('\n', '')
                headers.append(p) if not p in headers else None
    if known_headers_path:
        if os.path.exists(known_headers_path):
            for p in open(known_headers_path,'r').readlines():
                p = p.replace('\n', '')
                headers.append(p) if not p in headers else None
    return headers

def prepare_all(headers=[],payloads=[]):
    data = []
    for header in headers:
        for payload in payloads:
            h = {header:payload}
            data.append(h) if h not in data else None
    return data



