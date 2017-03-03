'''
Created on 3 Mar 2017

@author: Moriarty
'''

import requests
import json

apicode = ""

def dropletIdStatus(id,info):
    '''
    https://developers.digitalocean.com/documentation/v2/#droplets
    '''
    payload = {'Authorization': 'Bearer '+apicode}
    url_droplets ='https://api.digitalocean.com/v2/droplets'
    r = requests.get(url_droplets, headers=payload)
    response = r.json()
    return response["droplets"][id][info]

def snapshotIdStatus(id,info):
    '''
    https://developers.digitalocean.com/documentation/v2/#snapshots
    '''
    payload = {'Authorization': 'Bearer '+apicode}
    url_droplets ='https://api.digitalocean.com/v2/snapshots'
    r = requests.get(url_droplets, headers=payload)
    response = r.json()
    return response["snapshots"][id][info]

def actionDroplet(process):
    '''
    {"type":"power_cycle"}    Turn Droplets off and back on again.
    {"type":"power_on"}    Power Droplets on. Must be off.
    {"type":"power_off"}    Power Droplets off. Must be on.
    {"type":"shutdown"}    Shutdown Droplets, similar to powering down from the command line.
    {"type":"enable_private_networking"}    Enable private networking.
    {"type":"enable_ipv6"}    Enable IPv6 addresses for Droplets.
    {"type":"enable_backups"}    Enable backups for Droplets.
    {"type":"disable_backups"}    Disable backups.
    {"type":"snapshot, "name": "snapshot_name"}    Take snapshots of Droplets. Droplets must be powered off first, and a name is mandatory.
    '''
    dropletId = dropletIdStatus(0,"id")
    url = "https://api.digitalocean.com/v2/droplets/" + str(dropletId)+"/actions"
    headers = {'Authorization': 'Bearer '+apicode}
    payload = {"type":process} # payload = {"type":process, "name": "snapshotname"} for snapshot
    r = requests.post(url, data=payload, headers=headers)
    print dropletIdStatus(0, "status")
    return r

def imageStatus(id,info):
    '''
    https://developers.digitalocean.com/documentation/v2/#images
    '''
    payload = {'Authorization': 'Bearer '+apicode}
    url_droplets ='https://api.digitalocean.com/v2/images?page=1&per_page=1&private=true'
    r = requests.get(url_droplets, headers=payload)
    response = r.json()
    return response["images"][id][info]

def deleteDroplet(id):
    dropletId = dropletIdStatus(id,"id")
    url = "https://api.digitalocean.com/v2/droplets/" + str(dropletId)+""
    headers = {'Authorization': 'Bearer '+apicode}
    r = requests.delete(url, headers=headers)
    return r

def createDropletFromImage(name,region):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = {'Authorization': 'Bearer '+apicode}
    imageId = imageStatus(0, "id")
    payload = {"name":name,"region":region,"size":"512mb","image": str(imageId)}
    r = requests.post(url, data=payload, headers=headers)
    return r.text

def dropletIPAdress(id):
    '''
    https://developers.digitalocean.com/documentation/v2/#droplets
    '''
    payload = {'Authorization': 'Bearer '+apicode}
    url_droplets ='https://api.digitalocean.com/v2/droplets'
    r = requests.get(url_droplets, headers=payload)
    response = r.json()
    return response["droplets"][id]["networks"]["v4"][0]["ip_address"]

def readOpenvpn(ip,name):
    input = open("template.ovpn", "r")
    temp = input.read()
    input.close()
    temp = temp.replace("@",ip)
    output = open(name+".ovpn", "w")
    output.write(temp)
    output.close()

if __name__ == '__main__':
    deleteDroplet(0)
    deleteDroplet(1)
    deleteDroplet(2)
    deleteDroplet(3)
