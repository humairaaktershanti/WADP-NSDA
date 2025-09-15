# Second Class

<details>
<summary><b>Database Migration</b></summary>

Migrations are Django’s way of propagating changes we make to our models (adding a field, deleting a model, etc.) into our database schema.

+ Make migrations:
  ```cmd
    python manage.py makemigrations
  ```
+ Migrate:
  ```cmd
    python manage.py migrate
  ```

Django framework have a build-in database named db.sqlite3. To manage our database we used DB SQLite3 Server. If it not availabe in our computer we need to download and install this.

### Download Link:<br>
[Download SQLiteBrowser 64-bit Windows](https://download.sqlitebrowser.org/DB.Browser.for.SQLite-3.12.2-win64.msi) <br>
[Download SQLiteBrowser 32-bit Windows](https://download.sqlitebrowser.org/DB.Browser.for.SQLite-3.12.2-win32.msi)

</details>

<details>
<summary><b>How to Create Super User</b></summary>
Creating a superuser in Django is essential for managing and maintaining the application, both during development and in production. Before using this feature, we must have migrated our project, otherwise the superuser database will not be created.

+ At first open the root folder.
+ Open command prompt.
+ Activate the virtual environment.
  ```cmd
    .\environmentname\Scripts\activate
  ```
+ Navigate to our Django project directory. Using `cd`
  ```cmd
    cd directory_path
  ```
+ Migrate project.
  ```cmd
    py manage.py migrate
  ```
+ Create super user
  ```cmd
    py manage.py createsuperuser
  ```
  Enter user name:
  ```cmd
  Username: examplename
  ```
  Enter email address (it is optional):
  ```cmd
  Email address: example@gmail.com
  ```
  Enter Password:
  ```cmd
  Password: ******
  ```
  Enter same password again:
  ```cmd
  Password(again): ******
  ```
+ Now we can login into our Django Admin page by running our django server.
  ```cmd
  python manage.py runserver
  ```
+ Using Username and Password we can login our admin panel. This is the local domai:
  ```cmd
  http://127.0.0.1:8000/admin/
  ```

</details>

<details>
<summary><b>How to Display some text in web browser? Also add custom urls</b></summary>

To send content back to the client's web browser we can used `HttpResponse`. It is a class used to generate HTTP responses. It's part of Django's HTTP handling framework.

+ After active our project. At first create a python script in our porject folder e.g. `views.py`
+ Import reqired class from django:
  ```python
  from django.shortcuts import HttpResponse
  ```
+ Create a function:
  ```python
  def homePage(request):
      return HttpResponse("Hello, Django!")
  ```
+ To display this content into web browser we need to connect this function into `urls.py` script. For do this open `urls.py` scripts.<br>
  Syntax:
  ```python
  from projectfoldername.scriptname import functionname
  ```
  Example:
  ```python
  from myProject.views import homePage
  ```
+ Also add this function with `urlpatterns = []` list:
  ```python
  path('routename',functionname , name="functionname"),
  ```
  Example:
  ```python
  path('home',homePage , name="homepage"),
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

# Home Work

### <b>Django Settings file Explanation:</b>

---

The Django settings file plays a crucial role in configuring and customizing Django projects. It serves as the central hub where various settings and configurations are defined for the project to function correctly.

+ `BASE_DIR:` This defines the base directory of our Django project. It's typically used to construct other paths within our project.

  ```python
    BASE_DIR = Path(__file__).resolve().parent.parent
  ```
  
+ `SECRET_KEY:` It is used to sign cookies and other security-related features.

  ```python
    SECRET_KEY = 'secret_key_here`
  ```

+ `DEBUG:` This determines whether our application is in debug mode or not. It's recommended to set it to False in production for security reasons. When set to **True**, detailed error messages will be displayed in case of exceptions.

  ```python
  DEBUG = True
  ```
+ `ALLOWED_HOSTS:` It is a list having addresses of all domains which can run our Django Project.

  ```python
    ALLOWED_HOSTS = ['example.com', 'www.example.com']
  ```

+ `INSTALLED_APPS:` The **INSTALLED_APPS** setting lists all the Django apps installed in the project. These apps define the functionality and features of the project.

  ```python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'your_custom_app',
    ]
  ```

+ `MIDDLEWARE:` This is a list of middleware classes that process requests and responses.

  ```python
    MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
  ```

+ `TEMPLATES:` The **TEMPLATES** setting configures how Django templates are handled. It includes the list of template engines, directories, and context processors.
+ `DATABASES:` The **DATABASES** setting configures the project’s database connection. It defines the database engine, name, user, password, and other necessary details.
+ `AUTH_PASSWORD_VALIDATORS:` This is a list of validators that are used to check the strength of user passwords.
+ `STATIC_URL:` The **STATIC_URL** setting specifies the URL from where static files will be served. Static files include CSS, JavaScript, and images.