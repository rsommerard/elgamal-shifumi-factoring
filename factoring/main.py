import client
import random
import sys
import time

BASE_URL = 'http://pac.bouillaguet.info/TP4/factoring'

lpn = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
    317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
    503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
    607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
    701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
    811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
    911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013,
    1019, 1021]

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

def expmod(rn, b, n):
    x = 1
    while b > 0:
        if b & 1 == 0:
            b >>= 1
        else:
            x = (x * rn) % n
            b = (b - 1) >> 1
        rn = (rn * rn) % n

    return x

def _rabin(rn, n):
    b = n - 1
    a = 0

    while b % 2 == 0:
        b >>= 1
        a += 1

    rnpow = expmod(rn, b, n)

    if rnpow == 1:
        return True

    for i in range(0, a):
        if expmod(rn, b, n) == n-1:
            return True
        b *= 2

    return False

def _isprime(n):
    if n < 7:
        if n in (2, 3, 5):
            return True
        else:
            return False

    if n & 1 == 0:
        return False

    k = 3
    sqrtn = heronsqrt(n)

    while k <= sqrtn:
        if n % k == 0:
            return False
        k += 2

    return True

def rabin(n, k=20):
    global lpn

    if n <= 1024:
        if n in lpn:
            return True
        else:
            return False

    if n & 1 == 0:
        return False

    for i in range(0, k):
        rn = random.randint(1, n-1)
        if not _rabin(rn, n):
            return False

    return True

def isprime(n):
    if len(str(n)) > 9:
        return rabin(n)
    else:
        return _isprime(n)

def heronsqrt(n):
    s1 = 1
    while True:
        s2 = (s1 + n // s1) // 2
        if abs(s1 - s2) < 2:
            if s1 * s1 <= n and (s1 + 1) * (s1 + 1) > n:
                return s1
        s1 = s2

def factorsdiv2(n):
    print('factorsdiv2')
    pstack = [2, 3, 5, 7, 11]
    sqrtn = heronsqrt(n)

    for p in pstack:
        if p > sqrtn:
            return [n, 1]
        if n % p == 0:
            return [p, n // p]

    p = pstack[-1] + 2

    while p <= sqrtn:
        if n % p == 0:
            return [p, n // p]
        p += 2

    return [n, 1]

def pollardrho(n):
    print('pollardrho')
    f = lambda x: x*x + 1
    xa = 2
    xb = 2
    y = 1
    while y == 1:
        xa = f(xa) % n
        xb = f(f(xb)) % n
        tmp = (xa - xb)
        for i in range(100):
            xa = f(xa) % n
            xb = f(f(xb)) % n
            xab = f(xa) % n
            xbb = f(f(xb)) % n
            tmp *= (xa - xb) * (xab - xbb) % n
            xa = xab
            xb = xbb

        y, _, _ = XGCD(tmp, n)

    return [y, n // y]

def _pollardpminus1(n, b):
    x = 2

    for i in range(1, b + 1):
        x = pow(x, i, n)

    y, _, _ = XGCD(x - 1, n)
    if y > 1 and y < n:
        return y

    return -1

def pollardpminus1(n):
    b = 2
    y = -1

    while b < n and y == -1:
        b += 1
        y = _pollardpminus1(n, b)

    if y == -1:
        return [n, 1]

    return [y, n // y]

def process(n):
    factors = []
    stack = [n]
    while len(stack) != 0:
        print("#{0}".format(time.strftime("%H:%M:%S")))
        print('>>stack:', stack)
        print('>>factors:', factors)
        x = stack.pop(-1)
        if isprime(x):
            factors.append(x)
        else:
            xa, xb = pollardrho(x)

            if xa == 1 or xb == 1:
                xa, xb = factorsdiv2(x)

            #xa, xb = pollardpminus1(x)

            stack.append(xa)
            stack.append(xb)
    factors.sort()
    return factors

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print("Arg. error.")
        exit(1)

    level_arg = sys.argv[1]
    class_arg = sys.argv[2]

    server = client.Server(BASE_URL)

    response = server.query('/get/' + level_arg + '/' + class_arg)

    n = response['n']
    id = response['id']

    print('-' * 80)
    print('length:', len(str(n)))
    print('n:', n)
    print('id:', id)
    print('-' * 80)

    factors = process(n)
    #factors [1, 3, 5, ...]
    parameters = { 'id': id, 'factors': factors }

    response = server.query('/submit/sommerard', parameters)
    print(response)
