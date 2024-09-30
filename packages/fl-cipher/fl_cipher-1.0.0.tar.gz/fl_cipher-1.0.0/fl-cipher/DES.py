from Cryptodome.Cipher import DES
import base64

# 秘钥 必须为8个字符
SECRET_KEY = "fengling"
# 初始向量/IV向量(CBC、CFB、OFB加密机制才需要设置)  必须为8个字符
IV = "12345678"


class DESEncryption:
    def __init__(self, key, iv):
        self.secret_key = key.encode()
        self.iv = iv.encode()
        self.__allow_mode = ["ECB", "CBC", "CFB", "OFB"]

    def query_support_model(self):
        return self.__allow_mode

    @staticmethod
    def _handle_encrypt_data(data):
        """
        处理待加密数据: 将传入数据转换成64位倍数的二进制数据
        """
        if isinstance(data, str):
            data = data.encode()

        pading_size = DES.block_size - len(data) % DES.block_size
        pading = bytes([pading_size]) * pading_size
        return data + pading

    @staticmethod
    def _handle_decrypt_data(data):
        """
        处理待解密数据: 将传入64位的二进制数据转换成原始字符串数据
        """
        padding_size = data[-1]
        return data[:-padding_size]

    def get_rule(self, mode):
        if mode in self.__allow_mode:
            _mode = getattr(DES, "MODE_" + mode)

            rule_params = {
                "key": self.secret_key,
                "mode": _mode,
            }
            if mode != "ECB":
                rule_params.update({
                    "iv": self.iv
                })

            return DES.new(**rule_params)

    def encrypt(self, plain_data, mode):
        en_rule = self.get_rule(mode)
        if not en_rule:
            print("不支持该加密模式！")
            return

        # 将明文数据编码为二进制数据并添加填充符号/数据加密/将二进制密文数据转化base64字符串输出
        plain_binary = self._handle_encrypt_data(plain_data)
        cipher_binary = en_rule.encrypt(plain_binary)
        return base64.b64encode(cipher_binary)

    def decrypt(self, cipher_data, mode):
        de_rule = self.get_rule(mode)
        if not de_rule:
            print("不支持该解密模式！")
            return

        # 将base64密文字符串转化为二进制密文数据/数据解密/解析二进制明文并剔除填充符
        cipher_binary = base64.b64decode(cipher_data)
        plain_binary = de_rule.decrypt(cipher_binary)
        return self._handle_decrypt_data(plain_binary)


if __name__ == '__main__':
    ready_data = "人生苦短,我学Python!"
    des = DESEncryption(SECRET_KEY, IV)

    encrypted_data = des.encrypt(ready_data, "OFB")
    print(f"【密文】: {encrypted_data.decode()}")
    decrypted_data = des.decrypt(encrypted_data, "OFB")
    print(f"【明文】: {decrypted_data.decode()}")
