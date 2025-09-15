print("\n----For with continue----")
st = "banana"
for x in st:
    if x == 'a':
        continue
    print(x,end="")
    
print("\n----For with break----")
st = "bananajbsddd"
for x in st:
    if x == 'j':
        break
    print(x,end="")

print("\n----For with list----")
fruits = [['shakil','tansen','jessica','urmi'],"banana","chery"]

for x in fruits:
    for i in x:
        for j in i:
            print(j)
        print("\n")

    print("\n")
