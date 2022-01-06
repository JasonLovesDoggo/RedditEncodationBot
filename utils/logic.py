import argparse
import base64
import binascii
import codecs
import logging
import shlex

import praw

from utils.funcs import create_gist, reply, remove_markdown
from utils.vars import MorseCode, MorseCodeReversed, footer_message

log = logging.getLogger(__name__)

"""
Basic logic 
-e/encode : Encode
-d/decode : Decode

types:

-b64/base64 : Base64
"""


def logic(bot: praw.Reddit, message):
    argument = remove_markdown(str(message.body).replace(f'u/{str(bot.user.me())}', ''))
    print(f'{argument=}')
    pr = argparse.ArgumentParser()
    pr.add_argument('--encode', '-e', help='Pick encode as your choice', action='store_true')
    pr.add_argument('--decode', '-d', help='Pick decode as your choice', action='store_true')
    pr.add_argument('--base32', '-b32', help='Encode/Decode in base32', action='store_true')
    pr.add_argument('--base64', '-b64', help='Encode/Decode in base64', action='store_true')
    pr.add_argument('--rot13', '-r13', help='Encode/Decode in rot13', action='store_true')
    pr.add_argument('--hex', '-he', help='Encode/Decode in hex', action='store_true')
    pr.add_argument('--base85', '-b85', help='Encode/Decode in base85', action='store_true')
    pr.add_argument('--ascii85', '-a85', help='Encode/Decode in ASCII85', action='store_true')
    pr.add_argument('--morse', '-m', help='Encode/Decode in morse code', action='store_true')
    pr.add_argument('--binary', '-b', help='Encode/Decode in binary', action='store_true')
    pr.add_argument('--text', '-t', help='the data')

    args = pr.parse_args(shlex.split(argument))
    print(f'{args=}')
    if not args.text:
        return warning(message, 'you need to fill the --text argument')
    text = args.text
    # types
    if args.base32:
        codec = 'base32'
    elif args.base64:
        codec = 'base64'
    elif args.rot13:
        codec = 'rot13'
    elif args.hex:
        codec = 'hex'
    elif args.base85:
        codec = 'base85'
    elif args.ascii85:
        codec = 'ascii85'
    elif args.morse:
        codec = 'morse'
    elif args.binary:
        codec = 'binary'
    else:
        return warning(message, 'you need to fill in a least one of these options')

    if args.encode:
        encode(codec, message, text)
    elif args.base64:
        decode(codec, message, text)

    if not args.encode and not args.decode:
        return warning(message, 'You need to pick either encode or decode\ne.g. -e -b32 hey')
    elif args.encode and args.decode:
        return warning(message, 'You can\'t pick both encode and decode')


def encode(codec, message, txt):
    """All encode methods"""
    match codec:
        case 'base32':
            encode_base32(message, txt)
        case 'base64':
            encode_base64(message, txt)
        case 'base85':
            encode_base85(message, txt)
        case 'rot13':
            encode_rot13(message, txt)
        case 'hex':
            encode_hex(message, txt)
        case 'ascii85':
            encode_ascii85(message, txt)
        case 'morse':
            encode_morse(message, txt)
        case 'binary':
            encode_binary(message, txt)


def decode(codec, message, txt):
    """All decode methods"""
    match codec:
        case 'base32':
            decode_base32(message, txt)
        case 'base64':
            decode_base64(message, txt)
        case 'base85':
            decode_base85(message, txt)
        case 'rot13':
            decode_rot13(message, txt)
        case 'hex':
            decode_hex(message, txt)
        case 'ascii85':
            decode_ascii85(message, txt)
        case 'morse':
            decode_morse(message, txt)
        case 'binary':
            decode_binary(message, txt)


def warning(message, msg):
    log.warning(f'Message: {message} '
                f'{msg}')

    message.reply(f'{msg}'
                  f'{footer_message()}')


def InvalidWarning(message, param):
    log.info(f'Message: {message} '
             f'{param}')

    message.reply(f'Sorry {message.author} but it looks like that was some {param}, Please try again.'
                  f'{footer_message()}')


def encryptout(message, ConversionType: str, text):
    """The main, modular function to control encrypt/decrypt commands"""
    if not text:
        return warning(message,
                       f'Aren\'t you going to give me anything to encode/decode **{message.author.name}**'
                       )
    # todo return if over 1500 chars in lengh a github gist
    try:
        text = str(text, 'utf-8')
    except:
        pass
    
    try:
        content = f'**{ConversionType}**\n{text}'
    except Exception as e:
        log.error(f'Somthing went wrong with {e}')
        return warning(message, f'Somthing went wrong, sorry {message.author}...')

    if len(text) < 1500:
        reply(message, content)

    else:
        CreateGistMessage(message, content=content)

def CreateGistMessage(message, content: str):
    return reply(message, content=f'The text was a bit long so I put it in a gist {CreateGist(message, content)}')

def CreateGist(message, content: str) -> str:
    return create_gist(description=f'Encodation feed for u/{message.author}',
                       content=content)

def encode_base32(message, text: str):
    encryptout(
        message, 'Text -> base32', base64.b32encode(text.encode('utf-8'))
    )

def decode_base32(message, text: str):
    try:
        encryptout(
            message, 'base32 -> Text', base64.b32decode(text.encode('utf-8'))
        )
    except Exception:
        InvalidWarning(message, 'Invalid base32...')

def encode_base64(message, text: str):
    encryptout(
        message, 'Text -> base64', base64.urlsafe_b64encode(text.encode('utf-8'))
    )


def decode_base64(message, text: str):
    try:
        encryptout(
            message, 'base64 -> Text', base64.urlsafe_b64decode(text.encode('utf-8'))
        )
    except Exception:
        InvalidWarning(message, 'Invalid base64...')

def encode_rot13(message, text: str):
    encryptout(message, 'Text -> rot13', codecs.decode(text, 'rot_13'))

def decode_rot13(message, text: str):
    try:
        encryptout(message, 'rot13 -> Text', codecs.decode(text, 'rot_13'))
    except Exception:
        InvalidWarning(message, 'Invalid rot13...')

def encode_hex(message, text: str):
    encryptout(
        message, 'Text -> hex', binascii.hexlify(text.encode('utf-8'))
    )

def decode_hex(message, text: str):
    try:
        encryptout(
            message, 'hex -> Text', binascii.unhexlify(text.encode('utf-8'))
        )
    except Exception:
        InvalidWarning(message, 'Invalid hex...')

def encode_base85(message, text: str):
    encryptout(
        message, 'Text -> base85', base64.b85encode(text.encode('utf-8'))
    )

def decode_base85(message, text: str):
    try:
        encryptout(
            message, 'base85 -> Text', base64.b85decode(text.encode('utf-8'))
        )
    except Exception:
        InvalidWarning(message, 'Invalid base85...')

def encode_ascii85(message, text: str):
    encryptout(
        message, 'Text -> ASCII85', base64.a85encode(text.encode('utf-8'))
    )

def decode_ascii85(message, text: str):
    try:
        encryptout(
            message, 'ASCII85 -> Text', base64.a85decode(text.encode('utf-8'))
        )
    except Exception:
        InvalidWarning(message, 'Invalid ASCII85...')

def encode_morse(message, text: str):
    try:
        answer = ' '.join(MorseCode.get(i.upper()) for i in text)
    except TypeError:
        return InvalidWarning(message, 'Invalid Morse')
    encryptout(message, 'Text -> Morse', answer)

def decode_morse(message, text: str):
    try:
        answer = ' '.join(MorseCodeReversed.get(i.upper()) for i in text.split())
    except TypeError:
        return InvalidWarning(message, 'Invalid Morse')
    encryptout(message, 'Morse -> Text', answer)

def encode_binary(message, text: str):
    try:
        res = ''.join(format(ord(i), '08b') for i in text)
    except TypeError:
        return InvalidWarning(message, 'Invalid Binary')
    encryptout(
        message, 'Text -> binary', res)

def decode_binary(message, text: str):
    try:
        binary_int = int(text, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, 'big')
        ascii_text = binary_array.decode()
    except TypeError:
        return InvalidWarning(message, 'Invalid Binary')
    encryptout(
        message, 'Binary -> Text', ascii_text)
