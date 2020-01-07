def get_lucky(number_range):
    ns = [i for i in range(number_range)]
    ns = [(None if i % 2 is 0 else i) for i in ns]

    lucky_ns = []
    for i in range(3, len(ns)-1):
        if ns[i] is not None:
            for j in range(0, len(ns), i):
                ns[j] = None
                break
            for j in ns[i:]:
                if j is not None:
                    lucky_ns.append(j)
                    break
    return lucky_ns


def isUlam(n, h, u, r):

    if h == 2: 
        return False

    hu = u[0]
    hr = r[0]

    if hr <= hu: 
        return h == 1

    if hr + hu > n: 
        r = r[1:]
    elif hr + hu < n: 
        u = u[1:]
    else: 
        h += 1
        r = r[1:]
        u = u[1:]

    return isUlam(n, h, u, r)

def get_ulam(n):
    u = [1, 2]
    r = [2, 1]
    p = 2

    while u[-1] < n-1:
        p += 1
        if isUlam(p, 0, u, r):
            u.append(p)
            r.insert(0, p)
    return u

def get_even(n):
    return [i for i in range(2, n+1, 2)]







