import os, csv, datetime, getpass
from tempfile import NamedTemporaryFile
import shutil
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

special_characters = ['#','!','~','(',')','_']
fieldnames = ['website', 'salt','timestamp']

def generate_salt(website):
    salt = os.urandom(16)
    current_time = datetime.datetime.now()
    return salt,current_time

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

def print_websites():
    print('\n')
    with open('salts.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file,fieldnames=fieldnames)
        i=1
        for lines in csv_reader:
            print(i,lines['website'],lines['timestamp'])
            i=i+1 

def main():
    #print_websites()
    choice=input('\nEnter:\n-------\n"0" to read a salt, \n"1" to generate a new salt, \n"2" to update an exisitng password, \n"3" to delete an existing entry, \nany other integer to print available websites: ')
    try:
        choice=int(choice)
    except:
        print('you must enter an integer number here')
        exit(0)
    if not choice:
        print_websites()
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
        website = input('Enter the name of the website (e.g. facebook): ')
        salt,timestamp = generate_salt(website)
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
    elif choice ==2 or choice ==3:
        print_websites()
        if choice ==2:
            website_id = input('Enter the id number of the website you want to update the key: ')
        else:
            website_id = input('Enter the id number of the website you want to delete the key: ')
        try:
            website_id = int(website_id)
        except:
            print('you must enter an integer number here')
            exit(0)
        temp_file = NamedTemporaryFile(mode='w', delete=False)
        filename = 'salts.csv'
        with open(filename, mode='r') as csv_file, temp_file:
            csv_reader = csv.DictReader(csv_file,fieldnames=fieldnames)
            csv_writer = csv.DictWriter(temp_file,fieldnames=fieldnames)
            i = 1
            for lines in csv_reader:
                salt = lines['salt']
                website = lines['website']
                timestamp = lines['timestamp']
                if i == website_id:
                    website_name = lines['website'].split(':')
                    if choice == 2:
                        print('updating', website_name[0])
                        salt,timestamp = generate_salt(website_name[0])
                        csv_writer.writerow({'website': website, 'salt': salt.hex(), 'timestamp': str(timestamp)})
                        derive_hash(salt,int(website_name[1]),int(website_name[2]))
                    else:
                        print('\nwebsite:',website_name[0])
                        print('---------')
                        confirmation = input('Are you sure to want to delete the key for this website (Y/y)? ')
                        if confirmation == 'Y' or confirmation == 'y':
                            print('deleting entry for',website_name[0])
                        else:
                            print('deletion of entry for',website_name[0],'cancelled')
                            exit(0)
                else:
                    csv_writer.writerow({'website' : website, 'salt' : salt, 'timestamp' : timestamp})
                i = i+1
        shutil.move(temp_file.name, filename)
        print_websites()
    else:
        print_websites()

if __name__ == '__main__':
    main()
