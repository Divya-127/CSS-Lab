import rsa
from cryptography.fernet import Fernet

def create_keys(public_key_file_name, private_key_file_name):
    (pubkey, privkey) = rsa.newkeys(2048)
    with open(public_key_file_name, 'wb') as key_file:
        key_file.write(pubkey.save_pkcs1('PEM'))
    with open(private_key_file_name, 'wb') as key_file:
        key_file.write(privkey.save_pkcs1('PEM'))

create_keys("my_public_key.pem", "my_priv_key.pem")
create_keys("company_public_key.pem", "company_private_key.pem")

key = Fernet.generate_key()
k = open('symmetric_key.pem', 'wb')
k.write(key)
k.close()
