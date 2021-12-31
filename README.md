# Project-Cryptography
By Souhail AIT LAHCEN

### Question  1 :

For Wikipedia : case sensitivity defines whether uppercase and lowercase letters are treated as distinct (case-sensitive) or equivalent (case-insensitive). But for for password and in our case, we are in acase-sensitive mode. 

This is the list :

![PhotoCrypto](https://user-images.githubusercontent.com/55179344/147825946-69da5716-ba1d-4e64-94d9-ae91c3ec83dd.png)


We have 26+15 =41 characters (distinct)

So logN = (log2 * 64)/41 => lnN =(ln10 * ln2 * 64)/41 => lnN = 2.49136447252 => N=12.077744633128626 => So N=13 is the minimum length.


## How to securely store user passwords ?

### Attempt 1 (Naive solution) :

We have different solutions like a cold wallet : you write your password on paper etc., But many people like me, they want save time and not to search everytime our password, who use google for example to save our password or (maybe the worst case) to use the same password for each account.

### Attempt 2 (Increasing the entropy) :

Like now, we have lot websites, which ask us to use non alphanumeric character or maybe to use uppercase and lowercase (both)  why ? Because as you know, in the entropy formula the number of symbols in the password and the number of possible symbols are proportional to the entropy. As you understood we can use on alphanumeric character or use uppercase and lowercase (both), increase the lentgh of the password and also to fight against the database breaches, use differents passwords between our different account.

### Attempt 3 (Which hashing algorithm to use) :

With google researchs, we can notice that the experts recommend us to use stronger hashing algorithms like SHA-256 or SHA-3. But we can also bcrypt or argon for example. 

### Attempt 4 (Data breaches and how to deal with it)

Store a another key in another database, to avoid this.One key for the all company.


## Usage of the script

First to import (or install) this :.


```py
import os

#Bcrypt libarie useful for the hashing
import bcrypt

#Tink useful for the secret key
import tink
from tink import daead, cleartext_keyset_handle, KeysetHandle
```
