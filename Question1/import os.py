import os
 
def encrypt_char(char, shift1, shift2):
    if char.islower():
        # lowercase
        return chr((ord(char) - ord('a') + shift1 + shift2) % 26 + ord('a'))
    elif char.isupper():
        # uppercase
        return chr((ord(char) - ord('A') + shift1 + shift2) % 26 + ord('A'))
    else:
        return char
 
def decrypt_char(char, shift1, shift2):
    if char.islower():
        return chr((ord(char) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))
    elif char.isupper():
        return chr((ord(char) - ord('A') - (shift1 + shift2)) % 26 + ord('A'))
    else:
        return char
 
def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()
   
    encrypted_text = ''.join([encrypt_char(c, shift1, shift2) for c in raw_text])
   
    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)
    print("Encryption complete. Saved to 'encrypted_text.txt'.")
 
def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        encrypted_text = f.read()
   
    decrypted_text = ''.join([decrypt_char(c, shift1, shift2) for c in encrypted_text])
   
    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted_text)
    print("Decryption complete. Saved to 'decrypted_text.txt'.")
 
def verify_decryption():
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        original = f.read()
    with open("decrypted_text.txt", "r", encoding="utf-8") as f:
        decrypted = f.read()
   
    if original == decrypted:
        print("Verification successful: Decrypted text matches the original.")
    else:
        print("Verification failed: Decrypted text does NOT match the original.")
 
def main():
    shift1 = int(input("Enter shift1 value: "))
    shift2 = int(input("Enter shift2 value: "))
   
    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_decryption()
 
if __name__ == "__main__":
    main()