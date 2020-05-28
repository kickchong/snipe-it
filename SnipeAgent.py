# Libraries
import requests, json, math
import socket, sys, os
import datetime
import wmi
import math
import datetime
from winregistry import WinRegistry as Reg
from getpass import getuser
from io import StringIO, BytesIO
from math import ceil
from lxml import etree
import argparse
import re
import logging

###
### TODO: Add fields for software list
###

# Globals
snipe_server = 'ttf-lax-snipe01.thirdfloor.lan'
debug = 1
SESSION = requests.Session()
VERSION = "2018.11.01"

JSON_HEADERS =  {   'Accept':'application/json', 
                    'Content-Type':'application/json',
                    'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjEwN2UxMTgwZmU2YmQwZDk3YTNiYzc1Yjg4OWYxNTY2MzFhOTVkMTA2NDMyZmY1YTZiMGZkNmU2ZTY5MTMyZDAxYjU4YzBmMzgxMmZkM2ViIn0.eyJhdWQiOiIxIiwianRpIjoiMTA3ZTExODBmZTZiZDBkOTdhM2JjNzViODg5ZjE1NjYzMWE5NWQxMDY0MzJmZjVhNmIwZmQ2ZTZlNjkxMzJkMDFiNThjMGYzODEyZmQzZWIiLCJpYXQiOjE1MzY5NDY2MjUsIm5iZiI6MTUzNjk0NjYyNSwiZXhwIjoxNTY4NDgyNjI1LCJzdWIiOiIzIiwic2NvcGVzIjpbXX0.ETol4LHKkJQMLIDteNeHSEmNR7OhK3RJFtBPPsx50vAs4dnNaxxwOG7Su1M0FpP6gV64XooOHlOSeXIr5QwfYn6F6BoW5rg2s_xCzvK_cWsAYDLvn5lGx0gH5mDmNtB9WZ1IrWhlc_Ru1BuONBaNA0FSISDtDdBbfpZW_n-E0UbSxJAVtVi4u4gDGvviqCxW4WBjKtGaZ8v3V9b3T-SVqVw4ujG8NEs0iYMEwuJ23H4DhJLhP-tGSSJuf4b5W-KuDjaZbY47j7N9bWnSwrLlqPeSNFmZ7xESh4SIvzXLe9_KtfQoKxmumgz41SKAuooA31g3PMsS5fjGelyGfOeaDD88c5us-A0GnY8SWFUo8s5Jt2QlpteOUSnSNE0PA4IE4PoYJKDcErhI1WxoAUzBE8bqLTu1p-0AjBKsteGUSZX8FHmU-jrmvZjvzdmlWK8wmFs1Mkyhj4_Iw2HVPeEEdO0snazlpdsTzE1n7ufAQIoVLkT-VgMouEjT1vUCWTii_2dengaZIyCPcng7YA5LDO-MmukOSTrEWTuFSKg-Of2xglKVu3hexILzecOpbSim793LHHXuY-mT0tRcamJvKE63IBz6dC-JGcVlXOuwv3liDhp-HO2_POdY764c9rYhEDEKXXmMfEYOrhok5Zi0aDUPtWCthyqYCr_w6AY8Uk8'
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
 
def getCliOptions():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--debug', type=int, default=1, help='Debug level. 0 = no debugging. 1 = some. 2 = verbose. 3 = verbose + console output')
    parser.add_argument('--server', type=str, default='ttf-lax-snipe01', help='Server hostname or IP address for Snipe.')
    parser.add_argument('--debug_file', type=str, default='C:\Windows\Temp\SnipeAgent.log', help='File path (including filename) for debug log.')

    args = parser.parse_args()
    
    return args
 
def getImageVersion():
    reg = Reg()
    path = r'HKLM\SOFTWARE\TheThirdfloor'
    try:
        reg.read_key(path)
        iv = reg.read_value(path, 'ImageVersion')
        return iv['data']
    except:
        return 0
        
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
    if computer_info.Model == "All Series":
        wks_temp.model = "Antec Workstation"
    else:
        wks_temp.model = computer_info.Model
    wks_temp.lastLogonUsername = getuser()

    wks_temp.OSName = os_name
    wks_temp.OSVersion = os_version
    wks_temp.CPU = proc_info.Name
    wks_temp.RAM = (math.ceil(system_ram))

    wks_temp.GPU = gpu_info.Name
    wks_temp.imageVersion = getImageVersion()
    if debug >= 2:
        logging.debug( "Workstation Image Version " + str( wks_temp.imageVersion ) )

    # Variable for holding a MAC address and its IP address
    netInfo = []
    
    for nic in computer.Win32_NetworkAdapterConfiguration():
        nicMac = "00:00:00:00:00:00"
        nicIP = "0.0.0.0"
        #print json.dumps(nic.properties)
        
        if ( nic.MACAddress != None ) and ( nic.IPEnabled ):
            nicMac = nic.MACAddress
            #print nic.IPAddress
            #print("MAC: {0} IP: {1}").format( nic.MACAddress, nic.IPEnabled )
            try:
                for IPAddress in nic.IPAddress:
                    # Only grab the IPv4 Address
                    if re.search( '[.]', IPAddress ) != None:
                        nicIP = IPAddress
            except: pass
            netInfo.append({'MAC':nicMac, 'IP': nicIP})
            if debug >= 3:
                logging.debug( "Inspecting ethernet adaptor: MAC " + nicMac + " with IP " + nicIP )
    wks_temp.networkInfo = netInfo
    if debug >= 3:
        logging.debug( "Ethernet adapter info -- Found " + str(netInfo) )
    return wks_temp
                   
def getJSON( url ):
    r = SESSION.get(url,headers=JSON_HEADERS)
    return r.json() 

def findWorkstationID( current_wks ):
    # Find out how many items are in the Snipe Inventory
    recs = getJSON( 'http://' + snipe_server + '/api/v1/hardware' + "?limit=1" )
    # Get the record of all the workstations in Snipe
    recs = getJSON( 'http://' + snipe_server + '/api/v1/hardware' + "?limit=" + str(recs['total']) )
    
    MACfound = False
    wksID = 0
    
    if debug >= 3:
        logging.debug( "Looking up computer record in Snipe." )  
     
    for r in recs['rows']:
        for m in current_wks.networkInfo:
            #print("{0}: {1} ({2})").format(m['MAC'], r['custom_fields']['MAC Address']['value'], r['id'])
            if m['MAC'] == r['custom_fields']['MAC Address']['value']:
                MACfound = True
                wksID = int( r['id'] )
                if debug >= 2:
                    logging.debug( "Found record for MAC " + m['MAC'] + ". Record ID is " + str( wksID ) )
                break            
        if MACfound:
            break
    if MACfound == False:
        if debug >= 2:
            logging.debug( "Computer record for MAC " + m['MAC'] + " was NOT found!" )
            
    return wksID

def findManufactureID( wks ):
    # Find out how many items are in the Manufacturers
    recs = getJSON( 'http://' + snipe_server + '/api/v1/manufacturers' + "?limit=1" )
    # Get the record of all the workstations in Snipe
    recs = getJSON( 'http://' + snipe_server + '/api/v1/manufacturers' + "?limit=" + str(recs['total']) )
    
    if debug >= 3:
        logging.debug( "Reported computer manufacturer: " + wks.manufacturer )
                
    for r in recs['rows']:
        if r['name'] == wks.manufacturer:
            if debug >= 3:
                logging.debug( "Computer manufacturer ID: " + str( r['id'] ) )
            return r['id']
            
    if debug >= 3:
        logging.debug( "Computer manufacturer NOT found!" )    
    return 0

def findModelID( wks ):
    # Find out how many items are in the Models
    recs = getJSON( 'http://' + snipe_server + '/api/v1/models' + "?limit=1" )
    # Get the record of all the models in Snipe
    recs = getJSON( 'http://' + snipe_server + '/api/v1/models/' + "?limit=" + str(recs['total']) )
    
    if debug >= 3:
        logging.debug( "Reported computer model: " + wks.model )
                
    for r in recs['rows']:
        if r['name'] == wks.model:
            if debug >= 3:
                logging.debug( "Computer model ID: " + str( r['id'] ) )
            return r['id']
            
    if debug >= 3:
        logging.debug( "Computer model NOT found!" )    
    return 0
    
def addManufacturer( name ):
    record = {'name': name}
    url = 'http://' + snipe_server + '/api/v1/manufacturers'
    if debug >= 2:
        logging.debug( "Adding manufacturer " + name + "..." )  
    r = SESSION.post(url, data=json.dumps( record ), headers=JSON_HEADERS).json()
    if (r['payload'] != None) and ('id' in r['payload']):
        return r['payload']['id']
    else:
        if debug >= 1:
            logging.debug( "Could not add manufacturer " + name + " to Snipe." )        
        return 0
        
def addModel( name ):
    record = {'name': name}
    url = 'http://' + snipe_server + '/api/v1/models'
    if debug >= 2:
        logging.debug( "Adding model " + name + "..." )  
    r = SESSION.post(url, data=json.dumps( record ), headers=JSON_HEADERS).json()
    if (r['payload'] != None) and ('id' in r['payload']):
        return r['payload']['id']
    else:
        if debug >= 1:
            logging.debug( "Could not add model " + name + " to Snipe." )        
        return 0    
        
def getWorkstationById( id ):
    recs = getJSON( 'http://' + snipe_server + '/api/v1/hardware' + "/" + str(id) )
    return recs

def updateSnipeRecord( id, wks, rec ):  
    # Update record fields with new information  
    rec['_snipeit_mac_address_8'] = wks.networkInfo[0]['MAC']
    rec['_snipeit_memory_6'] = wks.RAM
    rec['_snipeit_gfx_card_7'] = wks.GPU
    rec['_snipeit_cpu_5'] = wks.CPU
    rec['name'] = wks.computerName
    rec['_snipeit_ip_address_9'] = wks.networkInfo[0]['IP']
    rec['_snipeit_username_10'] = wks.lastLogonUsername
    rec['_snipeit_os_11'] = wks.OSName + " (" + str( wks.OSVersion ) + ")"
    # Build Model/Manufacturer entry
    # NOT WORKING YET!!
    #mm_node =  {'id': wks.modelID, 'name': wks.model, 'manufacturer_id': wks.manufacturerID}
    #rec['model'] = json.dumps( mm_node )

    if wks.imageVersion != 0:
        rec['_snipeit_image_version_12'] = wks.imageVersion
    else:
        rec['_snipeit_image_version_12'] = "N/A"
    
    if id > 0:
        url = 'http://' + snipe_server + '/api/v1/hardware/' + str( rec['id'] )
        r = SESSION.patch(url, data=json.dumps(rec), headers=JSON_HEADERS)
    else:
        rec['status_id'] = 1
        rec['status'] = 1
        rec['model_id'] = 4
        rec['messages'] = ''
        url = 'http://' + snipe_server + '/api/v1/hardware'
        r = SESSION.post(url, data=json.dumps(rec), headers=JSON_HEADERS)
    
    if debug >= 2:
        logging.debug( "Updating Snipe record. Webserver reply was " + str( r.status_code ) )
    if debug >= 0:
        logging.debug( str( json.loads(r.text)['status'] ).upper() + ": " + str( json.loads(r.text)['messages'] ) )
        
    return json.loads(r.text)['status']
    
    # Main program
if __name__ == "__main__":
    
    # Grab command line options
    args = getCliOptions()
    # Set the SNIPE server address
    snipe_server = args.server  
    # Delete the current logging file
    try:
        os.remove( args.debug_file )
    except:
        if debug >= 3:
            logging.debug( "Could not delete log file." )   
        
    # Set our internal debugging level
    debug = args.debug
    # Prepare logging output to a file
    logging.basicConfig(format='%(asctime)s %(message)s', filename=args.debug_file, level=logging.DEBUG)
    # Disable messages from REQUESTS (web connection messages)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
    # If DEBUG level is set to 4, also output to the console
    if debug >= 4:
        logging.getLogger().addHandler(logging.StreamHandler())
    
    if debug >= 1:
        logging.debug( "Running SnipeAgent version " + str ( VERSION) )  
        
    if debug >= 3:
        logging.debug( "Command line options: " + str(args) )

    # Query the local machine to get its details
    if debug >= 1:
        logging.debug( "Getting workstation information... " )    
    wks = getWorkstationInfo()
    
    wks.modelID = findModelID( wks )   
    if wks.modelID == 0:
        wks.modelID = addModel( wks.model ) 
        
    wks.manufacturerID = findManufactureID( wks )   
    if wks.manufacturerID == 0:
        wks.manufacturerID = addManufacturer( wks.manufacturer )    
    
    # Check if the workstation exists
    if debug >= 2:
        logging.debug( "Checking if the workstation is already in the database... ")   
        
    wksID = findWorkstationID( wks )    
    rec = getWorkstationById( wksID )
   
    modRec = updateSnipeRecord( wksID, wks, rec )
 
        
        
