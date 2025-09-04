thislist = ["banana","apple","kiwi","banana"]
# thislist = ["banana","cherry","banana","kiwi"]

for i in thislist:
    if 'a' in i:
        thislist.remove(i)
        
print(thislist)