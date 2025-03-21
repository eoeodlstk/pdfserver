from Crypto.Cipher import AES
import binascii

class AESCipher:
    def __init__(self):
        self.key = b"" # 32 바이트 키 (AES256)
        self.iv = b"" # 16 바이트 IV
        self.BS = 16 # 블록 크기
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS) # PKCS7 패딩
        self.unpad = lambda s: s[:-ord(s[-1:])] # PKCS7 패딩 해제

    def encrypt(self, raw):
        raw = self.pad(raw).encode()
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(raw)
        return binascii.hexlify(encrypted).decode() # HEX 문자열 반환

    def decrypt(self, enc):
        try:
            enc = binascii.unhexlify(enc) # HEX 문자열을 바이트로 복원
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            decrypted = cipher.decrypt(enc)
            returnval = self.unpad(decrypted.decode()) # PKCS7 패딩 해제
            return returnval
        except Exception as e:
            print("JSON 변환에 실패했습니다:", e)

