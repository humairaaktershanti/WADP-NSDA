#print the odd or even from a list
print('---------print the odd or even from a list-------')

age = [1, 2, 3, 4, 77, 74, 23, 77, 0, 112]

for data in age:
    if(data%2 == 0):
        print(data, "is a even number")
    else:
        print(data, "is a odd number")

#print possitive or nagative from a list
print('---------print possitive or nagative from a list-------')

li = [44,-42,0,-5,-66,-65,-55,33,99]

for data in li:
    if(data >= 0):      # >= is equal to "gater or equal"
        print(data, "is a possitive number")
    else:
        print(data, "is a nagative number")


#print the odd or even from a 1 to 20
print('---------print the odd or even from a 1 to 20-------')

for data in range(1,21):
    if(data%2 == 0):
        print(data, "is a even number")
    else:
        print(data, "is a odd number")

#Sum of the all numbers from a list
print('---------Sum of the all numbers from a list-------')
listforsum = [2,4,6,8]
sum = 0
for i in listforsum:
    sum = sum + i
    
print("summetion is equal to: ", sum)

#count how many odd or even numbers from 1 to 20
print('---------count how many odd or even numbers from 1 to 20-------')
even = 0
odd = 0
for data in range(1, 21):
    if(data%2 == 1):
        odd = odd + 1
    else:
        even = even + 1
print("Total odd number =",odd)
print("Total even number =",even)

#the largest number in a list
print('---------the largest number in a list-------')
listForLar = [44,-42,0,-5,-66,-65,-55,33,99]

for i in listForLar:
    ...
# a=9
# b=6
# c = 77
# if(a<b):
#     print("B is big")
# else:
#     print("A is big")

#print the multiplication table of number 5   
      

