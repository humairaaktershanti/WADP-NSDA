#print the odd or even

g = 91 # = (equal) is meaning to assign a value # == (exact equal) is use for compare two value
print("------Find a even or odd number-------")
if(g%2 == 1):
    print(g, "is a odd number")
else:
    print(g, "is a even number")


print("------Find a number from a list: even or odd number-------")
age = [20,88,44,22,55,10]
for data in age:
    if(data%2 == 0):
        print(data, "is a even number")
    else:
        print(data, "is a odd number")



li = [44,42,0,-5,-66,-65,55,33,99]

for Huma in li:
    if(Huma%2==0):
        print(Huma,':even')
    else:
        print(Huma,':odd')            