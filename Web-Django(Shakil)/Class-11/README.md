# Class-11

### **Topics:**
+ Update Operation

<details>
<summary><b>Edit & Update Data</b></summary>
We can edit and update our data that are already in our database. Using update operation we can update our data. Here we update our data using a edit form.

+ At first add a edit button into the template file:
    ```html
    {% for i in std %}
        <tr>
            <td> {{i.FirstName}} </td>
            <td> {{i.LastName}} </td>
            <td> {{i.Department}} </td>
            <td>
                <a href="{% url 'editstudent' i.id %}">Edit</a>
            </td>
        </tr>
            
        {% endfor %}
    ```
    Here, `editstudent` is a URL pattern defined in the Django project's URL configuration. `i.id` is a variable representing the id, which is likely passed to this template.
+ Then create a URL from `urls.py` script.
    ```python
    urlpatterns = [
    path('editstudent/<str:myid>',editstudent,name="editstudent"),
    ]
    ```
+ After define the url. Now create a function into `views.py` file. With this function pass a argument named `myid` this id pass from url:
    ```python
    def editstudent(request, myid):
        pass
    ```

</details>