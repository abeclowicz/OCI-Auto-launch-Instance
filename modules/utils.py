class Text:
    codes = {
        "BOLD": '\033[1m', 

        "BLACK": '\033[30m', 
        "RED": '\033[31m', 
        "GREEN": '\033[32m', 
        "YELLOW": '\033[33m', 
        "BLUE": '\033[34m', 
        "MAGENTA": '\033[35m', 
        "CYAN": '\033[36m', 
        "LIGHT_GRAY": '\033[37m', 
        "DARK_GRAY": '\033[90m', 
        "BRIGHT_RED": '\033[91m', 
        "BRIGHT_GREEN": '\033[92m', 
        "BRIGHT_YELLOW": '\033[93m', 
        "BRIGHT_BLUE": '\033[94m', 
        "BRIGHT_MAGENTA": '\033[95m', 
        "BRIGHT_CYAN": '\033[96m', 
        "WHITE": '\033[97m', 

        "RESET": '\033[0m'
    }
    
    def __new__(self, data, *args):
        res = ""

        for arg in args:
            res += self.codes[arg] if arg in self.codes else ""

        return res + str(data) + (self.codes["RESET"] if args else "")

# ======== ======== ======== ======== ======== ======== ======== ========

from datetime import date
from string import ascii_letters, digits
from random import choices

def default_name(resource):
    date_str = date.today().strftime("%Y-%m-%d")
    rand_str = ''.join(choices(ascii_letters + digits, k = 8))

    return f"{resource}-{date_str}-{rand_str}"

# ======== ======== ======== ======== ======== ======== ======== ========

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def ssh_keygen():
    private_key = rsa.generate_private_key(
        public_exponent = 65537, 
        key_size = 2048, 
        backend = default_backend()
    )

    private_bytes = private_key.private_bytes(
        encoding = serialization.Encoding.PEM, 
        format = serialization.PrivateFormat.PKCS8, 
        encryption_algorithm = serialization.NoEncryption()
    )

    public_bytes = private_key.public_key().public_bytes(
        encoding = serialization.Encoding.OpenSSH, 
        format = serialization.PublicFormat.OpenSSH
    )
    
    return [bytes.decode("utf-8") for bytes in [private_bytes, public_bytes]]