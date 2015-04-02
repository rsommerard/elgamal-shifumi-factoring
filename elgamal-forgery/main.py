import client
import random

BASE_URL = 'http://pac.bouillaguet.info/TP4/ElGamal-forgery'

def XGCD(a, b):
    u = (1, 0)
    v = (0, 1)

    while(b != 0):
        q, r = divmod(a, b)
        a = b
        b = r
        tmp = (u[0] - q * v[0], u[1] - q * v[1])
        u = v
        v = tmp

    return a, u[0], u[1]

def modinv(a, b):
    g, x, y = XGCD(a, b)
    return x

if __name__ == '__main__':
    server = client.Server(BASE_URL)

    response = server.query('/PK/sommerard')
    
    p = response['p']
    g = response['g']
    h = response['h']
    
    q = p - 1
    
    b = random.randrange(1, p)
    c = random.randrange(1, p)
    
    tmp, _, _ = XGCD(c, q)
    while tmp != 1:
        c = random.randrange(1, p)
        tmp, _, _ = XGCD(c, q)

    r = (pow(g, b, p) * pow(h, c, p)) % p
   
    invc = modinv(c, q)
    s = (r * -1 * invc) % q
    
    m = (b * s) % q
    
    if(pow(g, m, p) == ((pow(h, r, p) * pow(r, s, p)) % p)):
        print('signature: OK')
    else:
        print('signature: KO')
    
    parameters = { 'm': m, 'signature': (r, s) }

    response = server.query('/verify/sommerard', parameters)
    print(response)

