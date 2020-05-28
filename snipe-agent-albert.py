import requests, json, math
import socket, sys, os
import datetime
import wmi
import math
import datetime
from getpass import getuser


snipe_server = 'develop.snipeitapp.com/'
SESSION = requests.Session()

JSON_HEADERS = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImVmMGVhY2Y4MjAyYzgwZWI2M2JkNmIwZDc0OGYwY2FkYzU2Y2ZlMzgyNzY4ODY0N2EwNmU4ZTBlNmYwZDgwODNjZmMyMzI2YWYyYTZlMTFkIn0.eyJhdWQiOiIxIiwianRpIjoiZWYwZWFjZjgyMDJjODBlYjYzYmQ2YjBkNzQ4ZjBjYWRjNTZjZmUzODI3Njg4NjQ3YTA2ZThlMGU2ZjBkODA4M2NmYzIzMjZhZjJhNmUxMWQiLCJpYXQiOjE0OTMzMzI2MjgsIm5iZiI6MTQ5MzMzMjYyOCwiZXhwIjoxODA4ODY1NDI4LCJzdWIiOiIyIiwic2NvcGVzIjpbXX0.NU7ZRIt-d4b0o8uv9ipo1vSWcg1svbmPp47kHErafm9iuK4FjygKd2_4Hp73HKAmjiYcEn3r39pwNh2t9BMFnTXv0KeDGC8zfZ9z7OJN_a59LPoarWBFzCsYETyAm-CeeFnfdj9Cr0ZeGOnnaPuWPYxicwKFeqJI4Hn8nCymcamDGE0u4WOO95ihGOAen4_fqpj-kkBDsvsGhB-cQxeuKdlbvO1yOsKmgQv-kQuxiFMn1zgU7P02mC6XXrbw6jTm7JOaBSbvqSwNtsrSKZkim1jxLsQ4dm36lFmeMkU6hZvNSUnxg8JwbmoxQ_3tZlG3IJh3Sc9ZUi-AEAQ4bbGzi_xNS9fenIdzLDaSiv_esYyNOYXqOuSBk8Yr-720N9OcVjGLnPrV3RtmPisV1aLFgKWLImtlyQgUq3d5LA3QXz8Q_8isvO9Am1u8ri2plbHGJLJ6GRW_mYcBEYMwUozaeXTUe_FUSSO8gpGtO9Hpa5SbERY272_tojyVXpYPaPdUYYmS9CP332jBNESPT8wGwpOM-iddeVo_n82w3dHmDEdp1Brbs3_vKk0AcgvDLsAbd4dZZO-UqddVx6SDb3HLw1Pmw1wGGYHA6w8wWQAiS9kg2xMcz5i75HOULaN3miqYvcPCvHpI2CBfuvdplI8QNm_XzFPmoQRu_5kR8knzla4",
    'accept': "application/json",
    'content-type': "application/json"
    }

class Workstation(object):
    def __init__(self):
        self.id = None
        self.assetTag = None
        self.computerName = None
        self.hostname = None
        self.domain = None
        self.manufacturer = None
        self.manufacturerID = None
        self.model = None 
        self.modelID = None         
        self.lastLogonUsername = None 
        self.OSName = None
        self.OSVersion = None
        self.CPU = None
        self.RAM = None
        self.GPU = None
        self.imageVersion = None
        self.NICCount = None
        self.MACAddresses = None
        self.IPAddress = None
        self.networkInfo = []

def getWorkstationInfo():
    # Reserve a class var to hold our workstation info
    wks_temp = Workstation()
    
    computer = wmi.WMI()
    computer_info = computer.Win32_ComputerSystem()[0]
    os_info = computer.Win32_OperatingSystem()[0]
    proc_info = computer.Win32_Processor()[0]
    gpu_info = computer.Win32_VideoController()[0]
    os_name = os_info.Name.encode('utf-8').split(b'|')[0]
    #os_version = ' '.join([os_info.Version, os_info.BuildNumber])
    os_version = os_info.Version
    system_ram = float(os_info.TotalVisibleMemorySize) / 1024  # KB to MB

    wks_temp.computerName = computer_info.DNSHostName
    wks_temp.hostame = computer_info.DNSHostName
    wks_temp.domain = computer_info.Domain
    #print('Hypervisor: {0}'.format(computer_info.HypervisorPresent))
    wks_temp.manufacturer = computer_info.Manufacturer
    wks_temp.OSName = os_name
    wks_temp.OSVersion = os_version
    wks_temp.CPU = proc_info.Name
    wks_temp.RAM = (math.ceil(system_ram))

    print(wks_temp.CPU)
    return wks_temp.computerName

def getJSON( url ):
    print(url)
    print(SESSION)
    r = SESSION.get(url,headers=JSON_HEADERS)
    return r.json() 
def findWorkstationID( current_wks ):
    # Find out how many items are in the Snipe Inventory
    recs = getJSON( 'http://' + snipe_server + '/api/v1/hardware' + "?limit=1" )
    print(recs)

if __name__ == "__main__":    
    wks = getWorkstationInfo()
    print(wks)
    findWorkstationID(wks)
    
    
  