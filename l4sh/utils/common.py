#!/usr/bin/env python3
import ipaddress
import requests
import re,random
import string
import binascii
from .enum import *

import base64

from sqlmap.lib.core.convert import decodeBase64,getUnicode
from sqlmap.thirdparty import six

from base64 import b64encode,b64decode

def base64encoder(data):
    return b64encode(data.encode('utf-8'))


def base64decoder(data):
    return b64decode(data.encode('utf-8')).decode()

def random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))




def obfuscate_ip(ip):
    ips = []
    for match in re.finditer(r'((?P<a>\d+)\.)((?P<b>\d+)\.)((?P<c>\d+)\.)'
                             '(?P<d>\d+)', ip):
        ips.append(str(int(match.group('a'))*256**3 +
                                int(match.group('b'))*256**2 +
                                int(match.group('c'))*256 +
                                int(match.group('d'))))
        ips.append(str(hex(int(match.group('a'))*256**3 +
                                int(match.group('b'))*256**2 +
                                int(match.group('c'))*256 +
                                int(match.group('d')))))
        ips.append(re.sub('o', '', str(oct(int(match.group('a')) *
                                   256**3+int(match.group('b'))*256**2 +
                                   int(match.group('c'))*256 +
                                   int(match.group('d'))))))
        ips.append(re.sub('o', '', str(oct(int(match.group('a')))) +
                                   '.'+str(oct(int(match.group('b'))))+'.' +
                                   str(oct(int(match.group('c'))))+'.' +
                                   str(oct(int(match.group('d'))))))
        ips.append(re.sub('o', '0000000',
                                   str(oct(int(match.group('a'))))+'.' +
                                   str(oct(int(match.group('b'))))+'.' +
                                   str(oct(int(match.group('c'))))+'.' +
                                   str(oct(int(match.group('d'))))))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              str(hex(int(match.group('b'))))+'.' +
              str(hex(int(match.group('c'))))+'.' +
              str(hex(int(match.group('d')))))
        ips.append(re.sub('x', 'x00000000',
              str(hex(int(match.group('a'))))+'.' +
              str(hex(int(match.group('b'))))+'.' +
              str(hex(int(match.group('c'))))+'.' +
              str(hex(int(match.group('d'))))))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              str(hex(int(match.group('b'))))+'.' +
              str(hex(int(match.group('c'))))+'.'+match.group('d'))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              str(hex(int(match.group('b'))))+'.' +
              match.group('c')+'.'+match.group('d'))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              match.group('b')+'.'+match.group('c')+'.'+match.group('d'))
        ips.append(match.group('a')+'.' +
              str(hex(int(match.group('b'))))+'.' +
              str(hex(int(match.group('c'))))+'.' +
              str(hex(int(match.group('d')))))
        ips.append(match.group('a')+'.'+match.group('b')+'.' +
              str(hex(int(match.group('c'))))+'.' +
              str(hex(int(match.group('d')))))
        ips.append(match.group('a')+'.'+match.group('b')+'.' +
              match.group('c')+'.'+str(hex(int(match.group('d')))))
        ips.append(re.sub('o', '', str(oct(int(match.group('a')))) +
              '.'+str(oct(int(match.group('b'))))+'.' +
              str(oct(int(match.group('c'))))+'.'+match.group('d')))
        ips.append(re.sub('o', '', str(oct(int(match.group('a')))) +
              '.'+str(oct(int(match.group('b'))))+'.' +
              match.group('c')+'.'+match.group('d')))
        ips.append(re.sub('o', '', str(oct(int(match.group('a')))) +
              '.'+match.group('b')+'.'+match.group('c')+'.'+match.group('d')))
        ips.append(re.sub('o', '', match.group('a')+'.' +
              str(oct(int(match.group('b'))))+'.' +
              str(oct(int(match.group('c'))))+'.' +
              str(oct(int(match.group('d'))))))
        ips.append(re.sub('o', '', match.group('a')+'.' +
              match.group('b')+'.'+str(oct(int(match.group('c'))))+'.' +
              str(oct(int(match.group('d'))))))
        ips.append(re.sub('o', '', match.group('a')+'.' +
              match.group('b')+'.'+match.group('c')+'.' +
              str(oct(int(match.group('d'))))))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              str(hex(int(match.group('b'))))+'.'+str(int(match.group('c')) *
              256+int(match.group('d'))))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              str(int(match.group('b'))*256**2+int(match.group('c'))*256 +
              int(match.group('d'))))
        ips.append(re.sub('o', '', str(oct(int(match.group('a')))) +
              '.'+str(oct(int(match.group('b')))))+'.' +
              str(int(match.group('c'))*256+int(match.group('d'))))
        ips.append(re.sub('o', '', str(oct(int(match.group('a'))))) +
              '.'+str(int(match.group('b'))*256**2+int(match.group('c'))*256 +
                      int(match.group('d'))))
        ips.append(str(hex(int(match.group('a'))))+'.' +
              re.sub('o', '', str(oct(int(match.group('b')))))+'.' +
              str(int(match.group('c'))*256+int(match.group('d'))))
        ips.append(re.sub('o', '', str(oct(int(match.group('a'))))) +
              '.'+str(hex(int(match.group('b'))))+'.' +
              str(int(match.group('c'))*256+int(match.group('d'))))
        ips.append('::ffff:'+str(hex(int(match.group('a'))*256**3 +
              int(match.group('b'))*256**2+int(match.group('c'))*256 +
              int(match.group('d'))))[2:])
        ips.append('0:0:0:0:0:ffff:'+str(hex(int(match.group('a')) *
              256**3+int(match.group('b'))*256**2+int(match.group('c'))*256 +
              int(match.group('d'))))[2:])
        ips.append('0000:0000:0000:0000:0000:ffff:' +
              str(hex(int(match.group('a'))*256**3+int(match.group('b'))*256 **
                  2+int(match.group('c'))*256+int(match.group('d'))))[2:])
        ips.append('0000:0000:0000:0000:0000:ffff:'+ip)
    return ips

def validate_ip(ip):
    try:
        int(ipaddress.ip_address(ip))
        return True
    except:
        pass
    return False

def validate_url(target):
    if not re.search(r"(?i)\Ahttp[s]*://", target):
        target = "http://%s" % target
    try:
        requests.head(target,timeout=15)
        return target
    except Exception as e:
        pass
    return False

def filterStringValue(value, charRegex, replacement=""):

    retVal = value

    if value:
        retVal = re.sub(charRegex.replace("[", "[^") if "[^" not in charRegex else charRegex.replace("[^", "["), replacement, value)

    return retVal


#from sqlmap project
def parseRequestFile(reqFile, checkParams=True):
    retz = {}
    content = open(reqFile,'r').read()
    if not re.search(BURP_REQUEST_REGEX, content, re.I | re.S):
          if re.search(BURP_XML_HISTORY_REGEX, content, re.I | re.S):
                reqResList = []
                for match in re.finditer(BURP_XML_HISTORY_REGEX, content, re.I | re.S):
                      port, request = match.groups()
                      try:
                            request = decodeBase64(request, binary=False)
                      except (binascii.Error, TypeError):
                            continue
                      _ = re.search(r"%s:.+" % re.escape(HTTP_HEADER.HOST), request)
                      if _:
                          host = _.group(0).strip()
                          if not re.search(r":\d+\Z", host):
                                request = request.replace(host, "%s:%d" % (host, int(port)))
                      reqResList.append(request)
          else:
                reqResList = [content]
    else:
          reqResList = re.finditer(BURP_REQUEST_REGEX, content, re.I | re.S)

    for match in reqResList:
          request = match if isinstance(match, six.string_types) else match.group(1)
          request = re.sub(r"\A[^\w]+", "", request)
          schemePort = re.search(r"(http[\w]*)\:\/\/.*?\:([\d]+).+?={10,}", request, re.I | re.S)
          if schemePort:
                scheme = schemePort.group(1)
                port = schemePort.group(2)
                request = re.sub(r"\n=+\Z", "", request.split(schemePort.group(0))[-1].lstrip())
          else:
                scheme, port = None, None
          if "HTTP/" not in request:
                continue
          if re.search(r"^[\n]*%s.*?\.(%s)\sHTTP\/" % (HTTPMETHOD.GET, "|".join(CRAWL_EXCLUDE_EXTENSIONS)), request, re.I | re.M):
                continue

          getPostReq = False
          url = None
          host = None
          method = None
          data = None
          cookie = None
          params = False
          newline = None
          lines = request.split('\n')
          headers = {}
          for index in range(len(lines)):
                line = lines[index]
                if not line.strip() and index == len(lines) - 1:
                      break
                newline = "\r\n" if line.endswith('\r') else '\n'
                line = line.strip('\r')
                match = re.search(r"\A([A-Z]+) (.+) HTTP/[\d.]+\Z", line) if not method else None
                if len(line.strip()) == 0 and method and method != HTTPMETHOD.GET and data is None:
                      data = ""
                      params = True
                elif match:
                      method = match.group(1)
                      url  = match.group(2)
                      if any(_ in line for _ in ('?', '=', '*')):
                            params = True
                      getPostReq = True
                elif data is not None and params:
                      data += "%s%s" % (line, newline)
                elif "?" in line and "=" in line and ": " not in line:
                      params = True
                elif re.search(r"\A\S+:", line):
                      key, value = line.split(":", 1)
                      value = value.strip().replace("\r", "").replace("\n", "")
                      if key.upper() == HTTP_HEADER.COOKIE.upper():
                            cookie = value
                      elif key.upper() == HTTP_HEADER.HOST.upper():
                            if '://' in value:
                                  scheme, value = value.split('://')[:2]
                            splitValue = value.split(":")
                            host = splitValue[0]
                            if len(splitValue) > 1:
                                  port = filterStringValue(splitValue[1], "[0-9]")
                      if key.upper() == HTTP_HEADER.CONTENT_LENGTH.upper():
                            params = True
                      elif key not in (HTTP_HEADER.PROXY_CONNECTION, HTTP_HEADER.CONNECTION, HTTP_HEADER.IF_MODIFIED_SINCE, HTTP_HEADER.IF_NONE_MATCH):
                            headers[getUnicode(key)] = getUnicode(value)
          data = data.rstrip("\r\n") if data else data
          if getPostReq and (params or cookie or not checkParams):
                if not port and hasattr(scheme, "lower") and scheme.lower() == "https":
                      port = "443"
                elif not scheme and port == "443":
                      scheme = "https"
                if not url.startswith("http"):
                      url = "%s://%s:%s%s" % (scheme or "http", host, port or "80", url)
                      scheme = None
                      port = None
          retz['host'] = host
          retz['url'] = url
          retz['method'] = method
          retz['cookie'] = cookie
          retz['data'] = data
          retz['scheme'] = scheme
          retz['headers'] = headers
          retz['params'] = params
    return retz