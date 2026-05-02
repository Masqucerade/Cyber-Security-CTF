import base64
import math
import os

def parse_ssh_pubkey(data):
# Extracts n and e from the OpenSSH public key string (ssh-rsa)
    parts = data.strip().split()
    if len(parts) < 2 or parts[0] != 'ssh-rsa':
        return None, None
    b64 = parts[1]
    try:
        decoded = base64.b64decode(b64)
    except:
        return None, None
    pos = 0
    # type name
    name_len = int.from_bytes(decoded[pos:pos+4], 'big')
    pos += 4
    name = decoded[pos:pos+name_len]
    pos += name_len
    # exp
    e_len = int.from_bytes(decoded[pos:pos+4], 'big')
    pos += 4
    e = int.from_bytes(decoded[pos:pos+e_len], 'big')
    pos += e_len
    # mod abs
    n_len = int.from_bytes(decoded[pos:pos+4], 'big')
    pos += 4
    n = int.from_bytes(decoded[pos:pos+n_len], 'big')
    return n, e

def int_to_bytes(n, size=None):
    # Преобразует целое в байты (big-endian)
    if n == 0:
        b = b'\x00'
    else:
        b = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    if size is not None and len(b) < size:
        b = b'\x00' * (size - len(b)) + b
    return b

def encode_length(l):
    #Encodes the length for ASN.1 DER
    if l < 0:
        raise ValueError("Negative length")
    if l < 128:
        return bytes([l])
    # long form
    len_bytes = l.to_bytes((l.bit_length() + 7) // 8, 'big')
    return bytes([0x80 | len(len_bytes)]) + len_bytes

def encode_integer(x):
    """Кодирует целое в ASN.1 INTEGER."""
    b = int_to_bytes(x)
    # if the highest bit is set, add the leading 0x00
    if b[0] & 0x80:
        b = b'\x00' + b
    return b'\x02' + encode_length(len(b)) + b

def generate_private_key_pem(n, e, d, p, q):
    #Generates an RSA private key in PEM format
    exp1 = d % (p-1)
    exp2 = d % (q-1)
    coeff = pow(q, -1, p)
    # ASN.1 SEQUENCE from 9 INTEGER
    seq_parts = [
        encode_integer(0),   # version
        encode_integer(n),
        encode_integer(e),
        encode_integer(d),
        encode_integer(p),
        encode_integer(q),
        encode_integer(exp1),
        encode_integer(exp2),
        encode_integer(coeff),
    ]
    seq = b''.join(seq_parts)
    der = b'\x30' + encode_length(len(seq)) + seq
    # PEM wrapper
    pem = b'-----BEGIN RSA PRIVATE KEY-----\n'
    b64_der = base64.b64encode(der).decode('ascii')
    for i in range(0, len(b64_der), 64):
        pem += b64_der[i:i+64].encode() + b'\n'
    pem += b'-----END RSA PRIVATE KEY-----\n'
    return pem

def main():
    files = [f for f in os.listdir('.') if f.startswith('id_rsa_')]
    files.sort(key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else -1)
    print(f"Найдено файлов: {len(files)}")

    keys = []
    for filename in files:
        with open(filename, 'r') as f:
            content = f.read()
        n, e = parse_ssh_pubkey(content)
        if n is not None:
            keys.append((n, e, filename))
        else:
            print(f"Предупреждение: не удалось распарсить {filename}")

    print(f"Загружено {len(keys)} публичных ключей.")

    # Search for a pair with a common multiplier
    for i in range(len(keys)):
        n1, e1, fname1 = keys[i]
        for j in range(i+1, len(keys)):
            n2, e2, fname2 = keys[j]
            g = math.gcd(n1, n2)
            if g > 1 and g != n1:
                print(f"Общий множитель {fname1} и {fname2}: p = {g}")
                p = g
                q = n1 // p
                phi = (p-1)*(q-1)
                # Calculate d = e^{-1} mod φ
                d = pow(e1, -1, phi)
                pem = generate_private_key_pem(n1, e1, d, p, q)
                with open('private_key.pem', 'wb') as out:
                    out.write(pem)
                print("Закрытый ключ в private_key.pem")
                print("Подключение:")
                print("  chmod 600 private_key.pem")
                print("  ssh -i private_key.pem eskin@fdca:22c8:7316::1 -p 16976")
                return

    print("Общий множитель ntnt.")

if __name__ == '__main__':
    main()
