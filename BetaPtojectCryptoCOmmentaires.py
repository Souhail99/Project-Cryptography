# from cryptography.fernet import Fernet
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.backends import default_backend

# import os
# import sys
# import hashlib

import Crypto
import Crypto.Random
from Crypto.Cipher import AES
from Crypto import Random

import random
import bcrypt

import base64
import tink
from tink import daead
import binascii
import json



database = 'database.txt'


daead.register()
secret_key = tink.new_keyset_handle(daead.deterministic_aead_key_templates.AES256_SIV)


daead_primitive = secret_key.primitive(daead.DeterministicAead)

### Associated
associated_data="Souhail AIT LAHCEN"
# We need to transform the str in bytes
associated_data_code = binascii.hexlify(bytes(associated_data, encoding='utf-8'))
###


#region JSON write
def JsonTest(file):
    keyId = 1234567
    employee = {
	"key": "Marie Richardson",
	"id": 1,
	"recrutement": True,
	"department": "Ventes"
    }
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=4)
    return 5
	
def Json(file):
    with open(file, 'w', encoding='utf-8') as f:
        secret_key.write(tink.JsonKeysetWriter(file), daead_primitive)
    return 5
#endregion

#region Hash Password
def hash_password(pwd:str):
  
  #binascii.hexlify(bytes(pwd, encoding='utf-8'))
  hash=bcrypt.hashpw(pwd.encode(),bcrypt.gensalt())
  if bcrypt.checkpw(pwd.encode(),hash):
    print("good !")
  else:
    print("bad")

  return hash
#endregion


#region encryption
def encryption_machine(msg):
  # encrypt using AES-SIV
  ciphertext=daead_primitive.encrypt_deterministically(msg, associated_data_code)
  return ciphertext
#endregion


#region save to database
def save_to_database(user, pwd):
  # use a file as a database
  # format: user, hashed_password
  # for example: file.write(user, hash_password(pwd))
  pwdisencrypted=encryption_machine(hash_password(pwd))
  pswrd = open(database, "a")
  #pswrd.write(user + ' , '+ pwdisencrypted.hex()+' , ')
  pswrd.write(f'{user},{pwdisencrypted.hex()} \n')
  pswrd.close()
#endregion



#region check_password
def check_password(user, pwd):
  # read from database
  error=0
  f=open(database,'r')
  lignes = f.readlines()
  liste=[]
  for ligne in lignes:
    #liste.append(ligne)
    userdatabase,encrypteddatabase=ligne.split(',')
    test=False
    print("userdata",userdatabase)
    print("pwddata",encrypteddatabase," ", type(encrypteddatabase))
    s=(encryption_machine(hash_password(pwd)))
    print("le sang4",s)
    
    # and check for authentication
    print("le s en bytes",s.hex())
    #ecrypted_pwd=bytes.fromhex(encryption_machine(hash_password(pwd)))
    #print("permeir type",type(ecrypted_pwd))
    edb=bytes.fromhex(encrypteddatabase)
    ecrypted_pwd=bytes.fromhex((encryption_machine(hash_password(pwd))))
    print("deuxieme type",type(ecrypted_pwd))
    # print(ecrypted_pwd.decode('utf-8'))
    if (user == userdatabase) and (edb == s):
      test=True
    elif (user == userdatabase) and (edb == s):
      test=False
      error=1
    elif (user == userdatabase) and (edb == s):
      test=False
      error=2
    else:
      test=False
      error=3
  return test,error


#region check_password2
def check_password2(user, pwd):
  # read from database
  error=0
  f=open(database,'r')
  lignes = f.readlines()
  liste=[]
  for ligne in lignes:
    #liste.append(ligne)
    liste.append(ligne.split(' , '))
  test=False
  print(liste)
  print(type(liste))
  s=str(liste[0])
  print("le s ",s)
  # and check for authentication
  #ecrypted_pwd=bytes.fromhex(encryption_machine(hash_password(pwd)))
  #print("permeir type",type(ecrypted_pwd))
  ecrypted_pwd=bytes.fromhex((encryption_machine(hash_password(pwd))))
  print("deuxieme type",type(ecrypted_pwd))
  # print(ecrypted_pwd.decode('utf-8'))
  if (user in s) and (ecrypted_pwd in s):
    test=True
  elif (user in s) and (ecrypted_pwd not in s):
    test=False
    error=1
  elif (user not in s) and (ecrypted_pwd in s):
    test=False
    error=2
  else:
    test=False
    error=3
  
  return test,error
#endregion


#region register
def inscription():
    user=input("Your username please > ")
    pwd=input("Your password please > ")
    save_to_database(user,pwd) 
    print("Register finish")
#endregion

#region login
def connexion():
    user=input("Your username please > ")
    pwd=input("Your password please > ")
    test,error=check_password(user, pwd)
    print("test ",test)
    print("error ",error)
    if test==True:
        print("Good password and good user, welcome : ",user)
    elif test==False and error==1:
        print("Error, this is the good user but not the good pwd")
    elif test==False and error==2:
        print("Error, this isn't the good user but the good pwd")
    else:
        print("Error, this isn't the good user and pwd")
#endregion

#region Project
def Projet_Crypto():
    c=True
    while c:
        print("Welcome to my first Crypto-Project")
        case=input("Do you want to register (Press 1) or login (Press 2) or quite (Press 3) > ")
        print("\n")
        if case == "1":
            inscription()

        elif case =="2":
            connexion()
        elif case =="3":
            c=False
            print("Au revoir !")
        else:
            print("Something, you don't press an avalaible numbers, please restart")
            print("\n")
#endregion

#region main
if __name__ == '__main__':
    Projet_Crypto()

