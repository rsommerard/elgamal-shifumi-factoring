import client
import random
import sys

BASE_URL = 'http://pac.bouillaguet.info/TP4/factoring'

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
    if(len(sys.argv) < 3):
        print("Arg. error.")
        return

    level = sys.argv[1]
    _class = sys.argv[2]

    server = client.Server(BASE_URL)

    response = server.query('/get/<level>/<class>')

    N = response['n']
    id = response['id']
    h = response['h']


    #factors 
    parameters = { 'id': id, 'factors': factors }

    response = server.query('/submit/sommerard', parameters)
    print(response)
