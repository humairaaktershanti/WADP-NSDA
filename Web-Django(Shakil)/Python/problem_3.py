# Find Greatest Number Between 4

a=2000
b=300
c=4400
d=3400

if a > b:
    if a > c:
        if a > d:
            print("A is greatest")
        else:
            print("D is greatest")
    else:
        if c > d:
            print("C is greatest")
        else:
            print("D is greatest")
else:
    if b > c:
        if b > d:
            print("B is greatest")
        else:
            print("D is greatest")
    else:
        if c > d:
            print("C is greatest")
        else:
            print("D is greatest")  

