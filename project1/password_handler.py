import hashlib

def get_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()
    
if __name__ == '__main__':
    print(get_hash('123456sdf#'))
    print(get_hash('123456szf#'))
