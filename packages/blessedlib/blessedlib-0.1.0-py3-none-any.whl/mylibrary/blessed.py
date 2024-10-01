# mylibrary/blessed.py
import hashlib

def hash_md5(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest()




def hash_sha256(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()


def hash_sha1(data):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(data.encode('utf-8'))
    return sha1_hash.hexdigest()