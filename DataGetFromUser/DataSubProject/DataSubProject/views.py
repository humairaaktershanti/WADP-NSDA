from django.shortcuts import render

def studentList(req):
    return render(req,'studentList.html')

def addStudent(req):

    if req.method == 'POST':
        name = req.POST.get('name')
        age = req.POST.get('age')
        email = req.POST.get('email')



        student = studentModel(
            name=name,
            age=age,
            email=email
        )

        student.save()

    return render(req,'addStudent.html')

def contact(req):
    return render(req,'contact.html')