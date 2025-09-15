names=['humaira','Khalid','Mehedi','Habib']


age = [20,88,44,22,55,10]
# print("Full List",names)
# print("Second index",names[1])
# print("Access multiple item:",names[2:4])
# print('First 2 items',names[:2])
# print("negative index",names[-2])
# print("Random Items",names[1],[3])
# print("from last",names[:-2])
# print("same",names[2:-2])


#.....List modify

print("Again Full List",names)
names[0]="Farhan"
print("Modified list",names)
names.append(89654)
print("After append:",names)
names.insert(1,"Sweety")
print("After insert:",names)
names.remove('Khalid')
print("After remove:",names)
names.pop(3)
print("After pop:",names)
names.extend(age)
print("Extend:",names)

