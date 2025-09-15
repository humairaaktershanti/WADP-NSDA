# Third Class

<details>
<summary><b>Render HTML Template</b></summary>

If we want to display any HTML template/page in our client browser. We need to used `render`. Using this method we can View any HTML template. 

+ After active our project. At first create a 2 folder/directory under the main project folder. Folder Name: `template & static`
+ Search django static file in website and add it into the `settings.py` script.
    ```python
    STATICFILES_DIRS = [
        BASE_DIR / "static",
        "/var/www/static/",
    ]
    ```
    from this file remove this line: `"/var/www/static/",` after remove we can see like this:
    ```python
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
    ```
+ From `settings.py` file Modified the `TEMPLATES` List. This list:
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    ```
    Modified `DIRS` using below command: 
    ```python
    'DIRS': [BASE_DIR, 'template'],
    ```
+ Now create a html file under the `template` folder. Like: `homepage.html`. Into this html file write some html code.
+ Then create a python script in our porject folder e.g. `views.py`
+ Import reqired class from django:
    ```python
    from django.shortcuts import render
    ```
+ Create a function into the `views.py` script.
    ```python
    def home(request):
        return render(request, 'homepage.html')
    ```
+ To display this html template into web browser we need to connect this function into `urls.py` script. For do this open `urls.py` scripts.<br>
  Syntax:
  ```python
  from projectfoldername.scriptname import functionname
  ```
  Example:
  ```python
  from myProject.views import home
  ```
+ Also add this function with `urlpatterns = []` list:
  ```python
  path('routename',functionname , name="functionname"),
  ```
  Example:
  ```python
  path('home',home , name="home"),
  ```
+ After connect the url then run the project.
  ```python
  py manage.py runserver
  ```
+ Copy and paste the local url into browser also add the route with the urls:
  ```cmd
  http://127.0.0.1:8000/routename
  ```
  Example:
  ```cmd
  http://127.0.0.1:8000/home
  ```
In this way we can create multiple function and urls.

</details>

<details>
<summary><b>Pass content from Django views to HTML templates:</b></summary>

To pass content from Django views to HTML templates, we typically use the Django template engine along with views.

+ At first we need to do render process.
+ Then modified the function from `views.py` script.
+ Now we can pass the data using python dictionary. This is my dictionary:
    ```python
    tableDict = {
            'cmpName': 'Google',
            'cmpContact': '012342',
            'country': 'USA',
        }
    ```
    Add this dictionary into the function.
    ```python
    def home(request):
    
        tableDict = {
            'cmpName': 'Google',
            'cmpContact': '012342',
            'country': 'USA',
        }
        return render(request, 'home.html',tableDict)
    ```
+ Create an HTML template file, such as `home.html`, where we'll render the content passed from the view. In the template, we can access the data passed from the `views.py` using the Django template language enclosed in double curly braces `{{ }}`.
  ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Template</title>
    </head>
    <body>
        <h1>Company Name: {{ cmpName }}</h1>
        <h1>Company Contact: {{ cmpContact }}</h1>
        <h1>Country: {{ country }}</h1>
    </body>
    </html>
  ```
+ Must be mapping the URL into `urls.py` scripts to view page.
    ```python
    urlpatterns = [
        path('my-url/', my_view, name='my-view'),
        ]
    ```
</details>