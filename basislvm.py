#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "jacobbjones"
__date__ = "$Feb 8, 2016 11:03:55 AM$"
import subprocess
import os
import re

sid = raw_input("what's your sid?:")
          
def createlv (size,name,vggroup):
        argument = "lvcreate -L " + str(size)+ "G -n "+ name +" "+vggroup   
        subprocess.call(argument,shell=True)
        lv = "/dev/"+vggroup+"/"+name
        argfs="mkfs.ext3 " + lv
        subprocess.call(argfs,shell=True)
        return lv
        
        
def mountpoint(mps):
        f = open("/etc/fstab","r")
        contents = f.readlines()
        f.close()
        
        contents.append(mps)
        
        f = open("/etc/fstab", "w" )
        contents = "".join(contents)
        f.write(contents)
        f.close()

def find_word(text, search):

   result = re.findall('\\b'+search+'\\b', text)
   if len(result)>0:
      return False
   else:
      return True

def maked (mkdir):
    if not os.path.isdir(mkdir):
        subprocess.call(("mkdir "+ mkdir),shell=True)
    else:
        print(mkdir[i]+" already exsists")
                
name = ["orabase","ora"+sid,"mirrlogA","mirrlogB","orahome","origlogA","origlogB","client","oraarch","sapreorg","stage","sapdata1","sapdata2","sapdata3","sapdata4","sap"+sid,"sapmnt","trans"]
size=[1,1,1,1,8,1,1,1,19.5,2,8,25,50,65,20,6,4,10]
vggroup="vgora"
oracle= "/oracle/"+sid
mount=["/oracle",oracle,oracle+"/mirrlogA",oracle+"/mirrlogB",oracle+"/112_64",oracle+"/origlogA",oracle+"/origlogB","/oracle/client",oracle+"/oraarch",oracle+"/sapreorg","/oracle/stage/112_64",oracle+"/sapdata1",oracle+"/sapdata2",oracle+"/sapdata3",oracle+"/sapdata4","/usr/sap/"+sid,"/sapmnt/"+sid,"/usr/sap/trans"]
mkdir=["/oracle",oracle,"/oracle/client","/oracle/stage","/oracle/stage/112_64",oracle+"/mirrlogA",oracle+"/mirrlogB",oracle+"/112_64",oracle+"/origlogA",oracle+"/origlogB",oracle+"/oraarch",oracle+"/sapreorg",oracle+"/sapdata1",oracle+"/sapdata2",oracle+"/sapdata3",oracle+"/sapdata4","/usr/sap","/usr/sap/trans","/sapmnt","/sapmnt/"+sid,"/usr/sap/"+sid]  

#for i in range (0,21):
 #   if not os.path.isdir(mkdir[i]):
  #      subprocess.call(("mkdir "+ mkdir[i]),shell=True)
   # else:
    #    print(mkdir[i]+" already exsists")
    
for i in range (0,18):
  #  output=subprocess.check_output("lvs",shell=True) in python 2.7 doesn't work in sles 2.6
    if (i>14):
        vggroup="vgsap"
    if (i<2):
        maked(mkdir[i])
    if (i == 2):
        for b in range (2,21):
            maked(mkdir[b])
    process = os.popen('lvs')
    preprocessed = process.read()
    process.close()
    if find_word(preprocessed,name[i]):        
        lv = createlv(size[i],name[i],vggroup)
        mps = (lv +" "+ mount[i]+ " ext3 acl,user_xattr  1 2 \n")
        mountpoint(mps)
        subprocess.call("mount "+lv+" "+mount[i],shell=True)
    else:
        print(name[i]+" logical volume already exsits")

subprocess.call("mount -a",shell=True)
