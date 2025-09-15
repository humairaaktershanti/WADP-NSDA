# Class - 06

## Topics:
+ Read Data
+ Display data on HTML Template

## Read Data From Model and Display

+ After Following the `Class-05` process then the next step is to fetch/read data model/database:
+ For this we need to read data from our template fuction. That already write on the `views.py` script.
+ From project folder open `views.py` script. 
+ Then import the model class from `myFolder`
    ```python
    from appDirectory.models import modelName
    ```
+ Then modified the function script, to fetch:
    ```python
    student=modelName.objects.all()
    ```
+ For this data create dictionary and return this data into the HTML template
    ```python
    def studentPage(request):
        student= modelName.objects.all()
        mydict = {
        'std': student
        }
        return render(request, 'studentPage.html', mydict)
    ```
+ Now getting data from HTML template. To display multiple table rows data we need to used for loop.
    ```html
    {% for i in dictkey %}
    <tr>
        <td>{{i.modelentity_name}}</td>
        <td>{{i.modelentity_name}}</td>
    </tr>
    {% endfor %}
    ```
    Example:
    ```html
    {% for i in std %}
        <tr>
            <td>{{i.roll}}</td>
            <td>{{i.name}}</td>
            <td>{{i.dept}}</td>
        </tr>
    {% endfor %}
    ```
    modelentity_name must be the same as the model entity name

