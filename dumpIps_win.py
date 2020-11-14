# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 20:05:16 2018

@author: Powermates
"""

import time
import locale
import os
import win32file #pip install pypiwin32, this is necessary in Windows because otherwise it locks file while opened, 
import msvcrt
import datetime
 
#samples:
#[2020.11.02-14.49.32:837][700]LogNet:Warning: UDP recvfrom error: 24 (SE_ENETRESET) from 63.223.60.58:53
#[2020.11.02-14.49.33:370][709]LogNet:Warning: UDP recvfrom error: 12 (SE_EMSGSIZE) from 92.184.105.85:24323
strMagic='LogNet:Warning: UDP recvfrom error'

def udpErr(longString):
    """
    Extracts the ip from error UDP log line
    Input: Complete line from the log
    Output: IPv4 x.x.x.x or '' if line is not an UDP error
    """
    if strMagic in longString: #quicker
        offset = longString.find(strMagic) #slower
        if offset > 29 and offset < 32: #avoid subchains occurrences
            offset2=longString.find(') from ',offset)
            if offset2>0:
                offset3=longString.find(':',offset2)
                if offset3>0: 
                    ip=longString[offset2+7:offset3]
                    return ip
    return ''   

def readIps(ipsFilename, ipList):
    """
    Read the ips from a txt dump file
    """
    with loadFile(ipsFilename) as ipsFileOpened:
        lines=ipsFileOpened.readlines()
        iLines=len(lines)
        for line in lines:
            ip=line.replace(' ','')
            ip=line.replace('\n','') 
            #TODO: sanitize and check ip format
            
            if ip not in ipList:
                ipList.add(ip)
        if len(ipList)<iLines:
            #found duplicates
            print ("Found duplicates or invalid:", iLines-len(ipList))
            #overwrite txt file
            saveIps(ipList,'w')

    return ipList

def readLog(logFilename, ipList, ipListNew):
    """
    Load the provided log and updates the collections
    """
    with loadFile(logFilename) as logFileOpened:
        loglines=logFileOpened.readlines()
        for line in loglines:
            ip=udpErr(line) #checks if the line has the magig key which results in extracting the ip
            if ip != '': #if we have an ip, then we will check if we don't have it, otherwise we will add to the collection
                if ip not in ipList:
                    ipList.add(ip)
                    ipListNew.add(ip)                    
    return ipList

def loadLogs(files,ipList, ipListNew): 
    """
    List and load all log files in the current directory
    """
    files=getLogFiles('.') #TODO test if this line is not needed now

    for file in files:
        ipList=readLog(file,ipList, ipListNew)
        
    return ipList

def loadFile(filename):
    """
    This method is important for win32 to avoid locking the ConanSanbox.log file while it is opened by a running Conan server (which will be the usual).
    In other platforms it is not necessary
    """
    # get a handle using win32 API, specifyng the SHARED access!
    handle = win32file.CreateFile(filename,win32file.GENERIC_READ,
                                    win32file.FILE_SHARE_DELETE|win32file.FILE_SHARE_READ|win32file.FILE_SHARE_WRITE,
                                    None,
                                    win32file.OPEN_EXISTING,
                                    0,
                                    None)

    # detach the handle
    detached_handle = handle.Detach()

    # get a file descriptor associated to the handle
    file_descriptor = msvcrt.open_osfhandle(detached_handle, os.O_RDONLY)

    return open(file_descriptor,"r",encoding="cp437", errors='ignore') 

def getLogFiles(dir='.', bAll=True):
    files=[]
    if bAll==True:
        strName='ConanSandbox'
    else:
        strName='ConanSandbox.log'
    
    for file in os.listdir(dir):
        if file.endswith(".log") and file.startswith(strName):
            files.append(os.path.join(dir, file))
    return files

def saveIps(ipList, mode='a'):
    with open('iplist.txt', mode,encoding="cp437", errors='ignore') as ipFileOpened:
        print(datetime.datetime.now(), " Saving iplist.txt")
        for ip in ipList:
            ipFileOpened.write(ip + '\n')


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__)) #change dir to real exec dir
    print("Starting dir: ", os.getcwd())

    ipList=set()
    ipListNew=set()

    if os.path.exists('iplist.txt'):
        #load existing blacklist
        ipList=readIps('iplist.txt', ipList)    
        iLen=len(ipList)
        print(datetime.datetime.now(), " Loaded ips:", iLen)
    else:
        #creating empty iplist.txt
        with open('iplist.txt', 'w',encoding="cp437", errors='ignore') as ipFileOpened:
            print(datetime.datetime.now(), " Created empty iplist.txt")
        iLen=0   

    #load all the logs for the first time
    files=getLogFiles('.', bAll=True)     
    ipList=loadLogs(files, ipList, ipListNew)

    while True:    
        if len(ipListNew)>0:
            #dump only the new ips and show the number
            saveIps(ipListNew,'a')            
            print(datetime.datetime.now()," Added new ips: ", len(ipListNew))
            ipListNew.clear()        

        #wait 10 secs before trying again
        time.sleep(10)
        
        #retry conan log only, use bAll=True for retrying all the logs every 10 seconds (not recommended)
        files=getLogFiles('.', bAll=False) 
        ipList=loadLogs(files, ipList, ipListNew)
    