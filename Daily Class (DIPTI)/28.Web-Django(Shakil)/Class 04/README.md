# Fourth Class

### Class Topics:
+ Navigation
+ Template Mastering

<details>
<summary><b>Navigate Every Page with Navbar:</b></summary>
We can easy navigate our every page with navbar. After navigation we can easily navigate one page to another page by clicking navbar list.

+ At first create some html page under the `template directory` to navigate page.
+ Define individual function into  `views.py` script.
    ```python
    def home(request):
        return render(request, 'home.html')
    def about(request):
        return render(request, 'about.html')
    ```
+ After that, mapping the every template function into `urls.py` scripts. such as:
    ```py
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('',home, name='homePage'),
        path('about/',about, name='aboutPage'),
    ]
    ```
+ Then we need to create a Navbar into our html template.
    ```html
    <div class="topnav">
        <a class="active" href="">Home</a>
        <a href="">About</a>
    </div>
    ```
+ For linking used `url` method into navbar `href=""`:
    ```python
    {% url 'homePage' %}
    ```
    Example:
    ```html
    <div class="topnav">
        <a class="active" href="{% url 'homePage' %}">Home</a>
        <a href="{% url 'aboutPage' %}">About</a>
    </div>
    ```

</details>