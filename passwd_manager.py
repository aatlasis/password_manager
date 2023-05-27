import os, csv, datetime, getpass
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

special_characters = ['#','!','~','(',')','_']

def generate_salt():
    website = input('Enter the name of the website (e.g. facebook): ')
    salt = os.urandom(16)
    current_time = datetime.datetime.now()
    return website,salt,current_time

def derive_hash(salt,length,special_character_needed):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    password = getpass.getpass('Enter your magic password:')
    bytes_password = bytes(password,'utf-8')
    key = kdf.derive(bytes_password)
    original_hash = key.hex().title()
    if length > 0:
        myhash = original_hash[0:length]
    else:
        myhash = original_hash
    if special_character_needed:
        int_val = bytes(original_hash, encoding='raw_unicode_escape') 
        int_val = int.from_bytes(int_val, "big")
        special_char = int_val%len(special_characters)
        spec_char_position = int_val%len(myhash)
        part1 = myhash[0:spec_char_position]
        part2 = myhash[spec_char_position+1:]
        myhash = part1+special_characters[special_char]+part2
    print("KDF output:", myhash)

def main():
    fieldnames = ['website', 'salt','timestamp']
    with open('salts.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file,fieldnames=fieldnames)
        i=1
        for lines in csv_reader:
            print(i,lines['website'])
            i=i+1 
    choice=input('Enter "0" to read a salt, "1" to generate a new salt, any other integer to print available websites: ')
    try:
        choice=int(choice)
    except:
        print('you must enter an integer number here')
        exit(0)
    if not choice:
        website_id = input('Enter the id number of the website you want to read the key: ')
        try:
            website_id = int(website_id)
        except:
            print('you must enter an integer number here')
            exit(0)
        with open('salts.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file,fieldnames=fieldnames)
            i = 1
            for lines in csv_reader:
                if i == website_id:
                    salt = lines['salt']
                    website = lines['website'].split(':')
                    break
                else:
                    i = i+1
            if 'salt' in locals():
                derive_hash(bytes.fromhex(salt),int(website[1]),int(website[2]))
            else:
                print(f'salt for website with id {website_id} not found')
    elif choice ==1: 
        website,salt,timestamp = generate_salt()
        length = input('Enter the maximum allowed password length (enter 0 if there is no max length or if you do not know): ')
        try:
            length = int(length)
        except:
            print('you must enter an integer number here')
            exit(0)
        spec_char = input('Do you want a special character? (Y/y): ')
        if spec_char == 'Y' or spec_char == 'y':
            special_character_needed = 1
        else:
            special_character_needed = 0 
        with open('salts.csv', 'a+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'website': ':'.join((website,str(length),str(special_character_needed))), 'salt': salt.hex(), 'timestamp': str(timestamp)})
        derive_hash(salt,length,special_character_needed)
    else:
        with open('salts.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file,fieldnames=fieldnames)
            for lines in csv_reader:
                print(lines['website'])

if __name__ == '__main__':
    main()
