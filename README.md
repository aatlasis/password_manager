# password_manager

A simple yet effective personal password manager, written in Python. 

Each password is generated based on two inputs: 
a) the name of the website for which you want to create a password
b) a user master password. 

Even if the same (common) master password is used for all websites, the final passord for each one of them is _unique_. 
An intermediate (also unique) salt is created for each website. 
Neither the master password, nor the final generated one are stored anywhere; only the intermediate salts per website are. 
In order to use the password manager in more than one devices, you only need to copy/transfer the salt file. 
However, salt file does not need to be protected, since someone with this file cannot generate the final password without knowing the master password. 

The master password needs to be sufficiently complex to resist brute force attacks. This complexity depends on personal preferences and risk assessment.

NOTE: This small program will not tell you whether the master password you used is correct or not, but every time it will rather create a password based on the master passowrd you used. 

WARNING: If you forget the master password, or you accidentally delete the salt file, there is no way of recovering the passwords. 

_DISCLAIMER_
This program was created for educational purposes only. Use it at your own risk. 
