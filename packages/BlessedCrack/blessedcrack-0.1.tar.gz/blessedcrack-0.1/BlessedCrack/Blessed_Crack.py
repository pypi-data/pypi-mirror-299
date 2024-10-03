import hashlib
from passlib.hash import md5_crypt, sha256_crypt

class HashCracker:
    def __init__(self):
        pass

    def crack_md5(self, hash_to_crack, wordlist_file):
        """فك تجزئة MD5 باستخدام قاموس كلمات."""
        try:
            with open(wordlist_file, 'r') as file:
                for word in file:
                    word = word.strip()
                    if md5_crypt.verify(word, hash_to_crack):
                        print(f"[+] تم العثور على المطابقة: {word}")
                        return word
            print("[-] لم يتم العثور على أي تطابق.")
            return None
        except FileNotFoundError:
            print("[-] ملف القاموس غير موجود.")
            return None
        except Exception as e:
            print(f"[-] حدث خطأ: {e}")
            return None

    def crack_sha256(self, hash_to_crack, wordlist_file):
        """فك تجزئة SHA256 باستخدام قاموس كلمات."""
        try:
            with open(wordlist_file, 'r') as file:
                for word in file:
                    word = word.strip()
                    if sha256_crypt.verify(word, hash_to_crack):
                        print(f"[+] تم العثور على المطابقة: {word}")
                        return word
            print("[-] لم يتم العثور على أي تطابق.")
            return None
        except FileNotFoundError:
            print("[-] ملف القاموس غير موجود.")
            return None
        except Exception as e:
            print(f"[-] حدث خطأ: {e}")
            return None

    def encrypt_md5(self, plain_text):
        """تشفير النص باستخدام MD5."""
        try:
            md5_hash = hashlib.md5(plain_text.encode()).hexdigest()
            return md5_hash
        except Exception as e:
            print(f"[-] حدث خطأ أثناء التشفير: {e}")
            return None

    def encrypt_sha256(self, plain_text):
        """تشفير النص باستخدام SHA256."""
        try:
            sha256_hash = hashlib.sha256(plain_text.encode()).hexdigest()
            return sha256_hash
        except Exception as e:
            print(f"[-] حدث خطأ أثناء التشفير: {e}")
            return None