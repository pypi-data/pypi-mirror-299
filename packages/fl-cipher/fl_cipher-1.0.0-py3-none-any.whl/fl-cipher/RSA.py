from rsa import VerificationError
from rsa.key import PrivateKey, PublicKey
import os
import rsa
import base64


class RSAEncryption:

    def __init__(self, keypair_folder_path):
        self.public_key = None
        self.private_key = None
        self.load_keypair(keypair_folder_path)

    # 使用接收人公钥加密,并使用自己的私钥生成签名
    def encrypt(self, plain, publickey_or_folder):
        # 提取公钥对象
        public_key = self.checkout_public_key(publickey_or_folder)
        if not public_key:
            return

        cipher_binary = rsa.encrypt(plain.encode(), public_key)
        signature_binary = rsa.sign(plain.encode(), self.private_key, "SHA-1")

        # 将二进制密文和签名编码为base64字符串返回
        cipher = base64.b64encode(cipher_binary).decode()
        signature = base64.b64encode(signature_binary).decode()
        return cipher, signature

    # 使用自己的私钥解密,并使用发送人公钥验签
    def decrypt(self, cipher, signature, publickey_or_folder):
        # 将base64字符串密文和签名解码为二进制数据
        cipher_binary = base64.b64decode(cipher)
        signature_binary = base64.b64decode(signature)

        # 提取公钥对象
        public_key = self.checkout_public_key(publickey_or_folder)
        if not public_key:
            return

        try:
            plain_binary = rsa.decrypt(cipher_binary, self.private_key)
            encryption_method = rsa.verify(plain_binary, signature_binary, public_key)
        except VerificationError:
            # print(f"签名不正确或数据被篡改！")
            return False
        except Exception as ret:
            # print(f"验签错误！{ret}")
            pass
        else:
            # print(f"加密方式: {encryption_method}")
            return plain_binary.decode()

    def checkout_public_key(self, publickey_or_folder):
        if isinstance(publickey_or_folder, PublicKey):
            public_key = publickey_or_folder
        else:
            public_key = self.load_public_key(publickey_or_folder)

        if not public_key:
            return False
        else:
            return public_key

    @staticmethod
    def generate_keypair(secretkey_name, save_dir='.', is_save=False):
        public_key, private_key = rsa.newkeys(nbits=1024)
        # 是否需要保存密钥文件
        if not is_save:
            return public_key, private_key

        if not os.path.exists(save_dir):
            return print("路径不存在！")
        # 拼接保存密钥对的文件夹路径,如果不存在则创建
        keypair_save_path = os.path.join(save_dir, secretkey_name)
        if not os.path.exists(keypair_save_path):
            os.mkdir(keypair_save_path)

        public_key_path = os.path.join(keypair_save_path, "public_key.pem")
        private_key_path = os.path.join(keypair_save_path, "private_key.pem")
        with open(public_key_path, "wb") as wf:
            wf.write(public_key.save_pkcs1())
        with open(private_key_path, "wb") as wf:
            wf.write(private_key.save_pkcs1())

    @staticmethod
    def load_public_key(folder):
        public_key_path = os.path.join(folder, "public_key.pem")
        if not os.path.exists(public_key_path):
            print("未找到公钥！")
            return False

        try:
            with open(public_key_path, "rb") as pub_file:
                public_key = rsa.PublicKey.load_pkcs1(pub_file.read())
        except Exception:
            print("无效公钥！")
            return False

        return public_key

    @staticmethod
    def load_private_key(folder):
        private_key_path = os.path.join(folder, "private_key.pem")
        if not os.path.exists(private_key_path):
            print("未找到私钥！")
            return False

        try:
            with open(private_key_path, "rb") as pri_file:
                private_key = rsa.PrivateKey.load_pkcs1(pri_file.read())
        except Exception:
            print("无效私钥！")
            return False

        return private_key

    def load_keypair(self, folder):
        public_key = self.load_public_key(folder)
        private_key = self.load_private_key(folder)
        if not public_key or not private_key:
            return print("密钥对缺失！")

        self.public_key = public_key
        self.private_key = private_key


if __name__ == '__main__':
    # 生成密钥对
    RSAEncryption.generate_keypair("laowang", is_save=True)
    RSAEncryption.generate_keypair("cuihua", is_save=True)

    # 创建rsa加密对象
    lw_rsa = RSAEncryption(r"./laowang")
    ch_rsa = RSAEncryption(r"./cuihua")

    # cuihua 加密数据(sham_data为篡改的数据)
    encrypted_data, sign = lw_rsa.encrypt('芝麻开门', 'cuihua')
    encrypted_mock_data, mock_sign = lw_rsa.encrypt('芝麻关门', 'cuihua')
    print(f"加密之后的数据和签名: \n【密文】: {encrypted_data}\n【签名】: {sign}")

    # laowang解密数据
    data1 = ch_rsa.decrypt(encrypted_data, sign, r"./laowang")
    data2 = ch_rsa.decrypt(encrypted_mock_data, sign, r"./laowang")

    print(f"【明文】 : {data1}") if data1 else print("签名不正确或数据被篡改!")
    print(f"【明文】 : {data2}") if data2 else print("签名不正确或数据被篡改!")
