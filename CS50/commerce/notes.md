

 Error message:

```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency auctions.0001_initial on database 'default'.
```

Cause:

Running `python manage.py migrate` then `python manage.py makemigrations auctions` then migrating

Solution from stackoverflow

```
Delete the DB
Delete pycache and migrations from all the apps
Make sure you have set AUTH_USER_MODEL
Make migrations
```


Username: user

Password: 123



Get all objects name

`categories=Category.objects.values_list('categoryName', flat=True)`


## Showing static images to django

STATIC_URL defined in settings.py			

In index.html -> Load `{% load static %}` then in img tag `src="{% static 'auctions/media/default.jpg' %}"`
