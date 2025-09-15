# Find Greatest Number Between 5

a = 20
b = 15
c = 12
d = 54
e = 100

if (a>=b and a>=c and a>=d and a>=e):
    print("A is greatest")
elif (b>=c and b>=d and b>=e):
    print("B is greatest")
elif (c>=d and d>=e):
    print("C is greatest")
elif (d>=e):
    print("D is greatest")
else:
    print("E is greatest")