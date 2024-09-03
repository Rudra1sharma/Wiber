# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

from tinyec import registry 
import secrets 

# Function to calculate compress point  
# of elliptic curves 
def compress(publicKey): 
 return hex(publicKey.x) + hex(publicKey.y % 2)[2:] 
  

# Function to derive a symmetric key from the ECC shared key
def derive_key(shared_key):
    shared_key_bytes = shared_key.x.to_bytes((shared_key.x.bit_length() + 7) // 8, 'big')
    symmetric_key = hashlib.sha256(shared_key_bytes).digest()  # Create a 256-bit key
    return symmetric_key

# Function to encrypt a message using AES
def encrypt_message(symmetric_key, plaintext):
    cipher = AES.new(symmetric_key, AES.MODE_CBC)
    iv = cipher.iv  # Initialization vector for CBC mode
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return iv + ciphertext  # Prepend the IV to the ciphertext

# Function to decrypt a message using AES
def decrypt_message(symmetric_key, ciphertext):
    iv = ciphertext[:AES.block_size]  # Extract the IV
    ciphertext = ciphertext[AES.block_size:]  # The actual ciphertext
    cipher = AES.new(symmetric_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

if __name__ == '__main__':
    
    # The elliptic curve which is used for the ECDH calculations 
    curve = registry.get_curve('brainpoolP256r1') 
      
    # Generation of secret key and public key 
    Ka = secrets.randbelow(curve.field.n) 
    X = Ka * curve.g  
    print("X:", compress(X)) 
    Kb = secrets.randbelow(curve.field.n) 
    Y = Kb * curve.g  
    print("Y:", compress(Y)) 
    print("Currently exchange the publickey (e.g. through Internet)") 
      
    # (A_SharedKey): represents user A 
    # (B_SharedKey): represents user B 
    A_SharedKey = Ka * Y 
    print("A shared key :",compress(A_SharedKey)) 
    B_SharedKey = Kb * X 
    print("(B) shared key :",compress(B_SharedKey)) 
    assert A_SharedKey == B_SharedKey
    
    
    # Example usage
    message = "Hello World"
    
    # Step 1: Derive symmetric key from the shared ECC key
    
    symmetric_key = derive_key(A_SharedKey)
    
    # Step 2: Encrypt the message
    ciphertext = encrypt_message(symmetric_key, message)
    print("Encrypted message:", ciphertext)
    
    # Step 3: Decrypt the message (using the same symmetric key derived from B's perspective)
    decrypted_message = decrypt_message(symmetric_key, ciphertext)
    print("Decrypted message:", decrypted_message)