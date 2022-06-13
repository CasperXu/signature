
def mod_inverse(a, m):
	m0 = m
	y = 0
	x = 1
	if (m == 1):
		return 0

	while (a > 1):
		q = a // m

		t = m
		m = a % m
		a = t
		t = y
		y = x - q * y
		x = t

	if (x < 0):
		x = x + m0
	return x

def doubling(A):
    s = (3*A[0]**2+a)*mod_inverse((2*A[1])%p,p)%p
    x = (s**2-2*A[0])%p
    y = (s*(A[0]-x)-A[1])%p
    return (x, y)

def add(A,B):
    if A==B: 
        return doubling(A)
    s = (A[1]-B[1])*mod_inverse((A[0]-B[0])%p,p)%p
    x = (s**2-A[0]-B[0])%p
    y = (s*(A[0]-x)-A[1])%p
    return (x, y)

def double_and_add(A,d):
    A_bin = []
    while d>0:
        A_bin.append(d%2)
        d = d//2
        
    B = A
    for i in range(len(A_bin)-2,-1,-1):
        B = doubling(B)
        if A_bin[i]==1:
            B = add(A,B)

    return B

#config
q = 19
p = 17
d = 10
a = 2
b = 2
A = (5,1)

B = double_and_add(A,d)

print(f"Public key: (p,a,b,q,A,B) = ({p}, {a}, {b}, {q}, {A}, {B})")
print(f"Private key: (d)=({d})")

while 1:
    print("Enter h(x) and k_E: ")
    h, kE = map(int,input().split())
    R = double_and_add(A,kE)
    r = R[0]
    print("--------------sign--------------")
    print(f"R = k_E*A = {R}, r = x_R = {r}")
    s = (h+d*r)*mod_inverse(kE,q)%q
    print(f"s = (h(x)+dr)kE^(-1) = {s} mod 19")
    print("----------verification----------")
    w = mod_inverse(s,q)
    u1 = w*h%q
    u2 = w*r%q
    P = add(double_and_add(A,u1),double_and_add(B,u2))
    print(f"w = s^(-1) = {w} mod 19\nu1 = w*h(x) = {u1} mod 19\nu2 = w*r = {u2} mod 19\nP = u1*A + u2*B = {P} mod 19")
    if P[0]%q == r%q:
        print("valid signature")
    else:
        print("invalid signature")