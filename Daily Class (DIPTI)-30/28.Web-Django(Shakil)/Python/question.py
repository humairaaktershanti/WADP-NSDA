numlst = []
evnlst = []
oddlst = []
numlst_sum = 0
evnlst_sum = 0
oddlst_sum = 0
oddevn_sum = 0

size = int(input("Enter the size of list: "))
print("Enter the list item: ")

for i in range(size):
    val = int(input())
    numlst.append(val)
    numlst_sum +=val
    if val % 2 == 0:
        evnlst.append(val)
        evnlst_sum+=val
    else:
        oddlst.append(val)
        oddlst_sum += val

oddevn_sum = oddlst_sum + evnlst_sum

if numlst_sum == oddevn_sum:
    print("Hello")
else:
    print("Not Equal")

print("List:",numlst, numlst_sum)   
print("Odd: ",oddlst, oddlst_sum)
print("Even: ",evnlst, evnlst_sum)

    