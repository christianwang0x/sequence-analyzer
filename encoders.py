import base64
import urllib.parse

# Error constants
BAD_LENGTH_MSG = "One of the parameters given does not have a correct length"

BAD_CHARS_MSG = "Invalid characters for this encoding scheme"

BAD_ENCODER_MSG = "Invalid encoder specified"


# Encoding scheme superclass that acts
#   as an interface to the scheme subclasses
class EncodingScheme:
    nr_chars = ""
    re_chars = ""

    @staticmethod
    def encode(input_bytes):
        pass

    @staticmethod
    def decode(input_string):
        pass


#  Encodes and decodes base64 data
class Base64(EncodingScheme):
    nr_chars = "="
    re_chars = ("ABCDEFGHIJKLMNOP"
                "QRSTUVWXYZabcdef"
                "ghijklmnopqrstuv"
                "wxyz0123456789+/")

    @staticmethod
    def encode(input_bytes):
        return base64.b64encode(input_bytes)

    @staticmethod
    def decode(b64_string):
        return base64.b64decode(b64_string)


#  Encodes and decodes ASCII hexadecimal data
#  This data is represented by a series of hex
#    numbers, where each two numbers represent
#    one byte of data.
class AsciiHex(EncodingScheme):
    nr_chars = ""
    re_chars = "0123456789ABCDEFabcdef"

    @staticmethod
    def encode(input_bytes):
        return ascii_hex_encode(input_bytes)

    @staticmethod
    def decode(hex_string):
        return ascii_hex_decode(hex_string)


# Encodes and decodes from a binary string
# Data should be provided as a string of
#   0's and 1's, without a prefix
class Binary(EncodingScheme):
    nr_chars = "b"
    re_chars = "01"

    @staticmethod
    def encode(input_bytes):
        return binary_encode(input_bytes)

    @staticmethod
    def decode(binary_string):
        return binary_decode(binary_string)


# Encodes and decodes from URL hexadecimal
#   format, where special characters are
#   encoded as a hex pair prefixed with a %
#   and spaces are replaced with +
class Url(EncodingScheme):
    nr_chars = ""
    re_chars = (" !\"#$%&'()*+,-./0123456789"
                ":;<=>?@ABCDEFGHIJKLMNOPQRST"
                "UVWXYZ[\]^_`abcdefghijklmno"
                "pqrstuvwxyz{|}~")

    @staticmethod
    def encode(input_bytes):
        return url_encode(input_bytes)

    @staticmethod
    def decode(url_string):
        return url_decode(url_string)


# Handles plain text input, converts directly
#   to bytes.
# The encode function actually decodes bytes
#   and the decode function encodes bytes
#   because the desired format is bytes, not str
class Plain(EncodingScheme):
    nr_chars = ""
    re_chars = (" !\"#$%&'()*+,-./0123456789"
                ":;<=>?@ABCDEFGHIJKLMNOPQRST"
                "UVWXYZ[\]^_`abcdefghijklmno"
                "pqrstuvwxyz{|}~")

    @staticmethod
    def encode(input_bytes):
        return plain_encode(input_bytes)

    @staticmethod
    def decode(string):
        return plain_decode(string)


# Exception object
class EncoderException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


# Encode to ASCII hex format
def ascii_hex_encode(input_bytes):
    encoded = ""
    for b in input_bytes:
        encoded += hex(int.from_bytes(b, 'big'))[2:]

    return encoded


# Decode from ASCII hex format
def ascii_hex_decode(hex_string):
    if len(hex_string) % 2 != 0:
        e = EncoderException(BAD_LENGTH_MSG, [])
        raise e
    decoded_bytes = b""
    try:
        for i in range(0, len(hex_string), 2):
            pair = hex_string[i:i+2]
            b = bytes((int(pair, 16),))
            decoded_bytes += b
        return decoded_bytes
    except ValueError:
        e = EncoderException(BAD_CHARS_MSG, [])
        raise e


# Encode to binary format
def binary_encode(input_bytes):
    encoded = ""
    for b in input_bytes:
        bits = bin(int.from_bytes(b, 'big'))[2:]
        bits = "0" * (8 - len(bits)) + bits
        encoded += bits
    return encoded


# Decode from binary format
# No prefix should be used for the binary string
#   (110101 instead of 0b110101)
def binary_decode(binary_string):
    if len(binary_string) % 8 != 0:
        e = EncoderException(BAD_LENGTH_MSG, [])
        raise e

    decoded_bytes = b""

    for i in range(0, len(binary_string), 8):
        bits = binary_string[i:i+8]
        b = bytes((int(bits, 2),))
        decoded_bytes += b

    return decoded_bytes


# Encode to plain text string from bytes
def plain_encode(input_bytes):
    return input_bytes.decode('utf-8')


# Decode to bytes from a string
def plain_decode(string):
    return bytes(string, 'utf-8')


# Encode with URL encoding scheme
# Including space character
def url_encode(input_bytes):
    return urllib.parse.quote_plus(input_bytes)


# Decode URL-encoded string
def url_decode(url_string):
    return urllib.parse.unquote_to_bytes(url_string)


# Decode a 2d table of bytes with the
#   appropriate encoder
def decode_list(l, encoder_obj):
    sequence = []
    for line in l:
        decoded = encoder_obj.decode(line)
        sequence.append(decoded)
    return sequence
