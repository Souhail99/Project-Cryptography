#!/usr/bin/env python

import os

#Bcrypt libarie useful for the hashing
import bcrypt

#Tink useful for the secret key
import tink
from tink import daead, cleartext_keyset_handle, KeysetHandle


#region tink and how to use it

daead.register()
database = 'database.txt'

#Reader of the .json, necessary to read and write (if we don't this file) the secret_key with tink
keysetFilename = "my_keyset.json"

#if the file exist we read the file
if os.path.isfile(keysetFilename):
  lecture = open(keysetFilename, "r")
  secret_key = cleartext_keyset_handle.read(tink.JsonKeysetReader(lecture.read()))
  lecture.close()

#else we create the file
else:
   ecriture = open(keysetFilename, "w")
   secret_key = tink.new_keyset_handle(daead.deterministic_aead_key_templates.AES256_SIV)
   cleartext_keyset_handle.write(tink.JsonKeysetWriter(ecriture), secret_key)
   ecriture.close()
   lecture = open(keysetFilename, "r")
   secret_key = cleartext_keyset_handle.read(tink.JsonKeysetReader(lecture.read()))
   lecture.close()


daead_primitive = secret_key.primitive(daead.DeterministicAead)
#endregion

### Associated
associated_data = b"Souhail"
###

#region Hash Password
def hash_password(pwd:str,salt=None):
  if salt==None:
    salt=bcrypt.gensalt()
  else:
    salt=salt
  hash=bcrypt.hashpw(pwd.encode(),salt)
  return hash,salt
#endregion


#region encryption
def encryption_machine(msg:bytes):
  # encrypt using AES-SIV
  ciphertext=daead_primitive.encrypt_deterministically(msg, associated_data)
  return ciphertext
#endregion


#region save to database
def save_to_database(user, pwd):
  # use a file as a database
  # format: user, hashed_password
  # for example: file.write(user, hash_password(pwd))
  hash,salt=hash_password(pwd)
  pwdisencrypted=encryption_machine(hash)
  pswrd = open(database, "a")
  pswrd.write(f'{user},{pwdisencrypted.hex()},{salt.hex()}\n')
  pswrd.close()
  
#endregion

#region check
def check_password(user, pwd):
  # read from database
  with open(database, 'r') as f:
    error=1
    test=False
    print("Welcome user :",user," we will verify if you are in our database...")
    for line in f.readlines():
      userdatabase,encrypteddatabase,salt= line.split(',')
      hash,salt2=hash_password(pwd,bytes.fromhex(salt))
      password_of_the_current_user=encryption_machine(hash)
      # and check for authentication
      encrypteddatabase=bytes.fromhex(encrypteddatabase)
      if (user == userdatabase) and (encrypteddatabase == password_of_the_current_user):
        test=True
        error=0
        return test,error 
  return test,error
#endregion


#region register
def inscription():
    user=input("Your username please > ")
    pwd=input("Your password please > ")
    print("\n")
    save_to_database(user,pwd) 
    print("\n")
    print("Register finish")
#endregion

#region login
def connexion():
    user=input("Your username please > ")
    pwd=input("Your password please > ")
    test,error=check_password(user, pwd)
    if test==True and error==0:
        print("Good password and good user, welcome :",user)
    if test==False and error==1:
        print("Error, this isn't the good user or pwd")
#endregion

#region Project
def Projet_Crypto():
    c=True
    print("Welcome to my first Crypto-Project ! ")
    while c:
        print("\n")
        print("-------------start-------------")
        print("\n")
        case=input("Do you want to register (Press 1) or login (Press 2) or exit (Press 3) > ")
        print("\n")
        if case == "1":
            inscription()
        elif case =="2":
            if os.path.isfile(database):
              connexion()
            else:
              print("Database isn't yet created, you need to register to initialize the database for the firstime")
        elif case =="3":
            c=False
            print("Au revoir !")
        else:
            print("Something, you don't press an avalaible numbers, please restart")
       
        print("-------------end---------------")
#endregion

#region main
if __name__ == '__main__':
    Projet_Crypto()

