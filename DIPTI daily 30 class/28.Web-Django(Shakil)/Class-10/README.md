# Class - 10

## Topics:
+ Delete Data From the database

## Delete Operation
If we want to delete any data from our model or database. For that we need to make change to our template file.

+ At first add a delete button into the template file:
    ```html
    {% for i in std %}
        <tr>
            <td> {{i.FirstName}} </td>
            <td> {{i.LastName}} </td>
            <td> {{i.Department}} </td>
            <td>
                <a href="{% url 'deletestudent' i.id %}">Delete</a>
            </td>
        </tr>
            
        {% endfor %}
    ```
    Here, `deletestudent` is a URL pattern defined in the Django project's URL configuration. `i.id` is a variable representing the id, which is likely passed to this template.
+ Then create a URL from `urls.py`
