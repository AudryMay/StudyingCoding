Notes

Run code

`python manage.py runserver`

Library to import markdown functions `markdown2`

URLS

`path('wiki/<str:title>', views.get_title, name='url_title_name'),`

- url name
- parameter: type - name
- function to handle request
- name of path -> can be used in django html

Getting POST

Views function

- Note use of `request.method` and `request.POST`

```
def edit(request):
    if request.method == "POST":
        page_title = request.POST["page_title"]
        markdown_content = util.get_entry(page_title)
        return render(request, "encyclopedia/edit.html", 
        {
            "page_title":page_title,
            "markdown_content":markdown_content
        })
```


URLS function

- Note use of name

`path('edit/', views.edit, name='url_edit_page'),`


HTML template

- note the action `"{% url'url_edit_page' %}"`
- note the csrf_token

```code
<form action="{% url 'url_edit_page' %}" method="POST">
        {% csrf_token %}
        <input type="hidden" value="{{ title }}" name="page_title">
        <input type="submit" value="Edit Page" class="btn btn-primary">
    </form>
```
