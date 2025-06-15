@@ -0,0 +1,33 @@
print("--------Loop Through a List")
student_name = ["John", "Jane", "Jim", "Jill"]
for name in student_name:
    print(name)


print("--------Loop Through a String")
student_name= "John"
for i in student_name:
    print(i)    


print("--------Loop Through a Dictionary key")
marks= {
    'Ban': 50,
    'Eng' : 'A+',
    'Math' : 'Fail',
}

for key in marks:
    print(key)


print("------Loop Through a Dictionary Value") 
for value in marks.values():
    print(value)   


print("------Loop Through a Dictionary key-Value")
for sub, reg in marks.items():
    print(sub,":",reg)
