!SLIDE
# An Introduction to Django
   
    Created by Jibo He, <a>drhejibo@gmail.com</a>

!SLIDE
### Table of Content
- Environment configuration
- urls.py for URL configuration
- views.py for view control

!SLIDE
### Environment configuration
~~~~{python}
pip install Django
~~~~

!SLIDE
### Environment configuration
~~~~{python}
pip install Django
~~~~

![Check-Django-installation](Check-Django-installation.png)

!SLIDE

### Starting a Project
~~~~{python}
django-admin startproject mysite 
~~~~

The above command will generate the following code structure. 

~~~~{python}
mysite/
  manage.py 
  mysite/
    __init__.py 
    settings.py 
    urls.py 
    wsgi.py 
~~~~

!SLIDE

### file explanation

* The outer mysite/ root directory. 
    * It’s just a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.
* manage.py. 
    * A command-line utility that lets you interact with your Django project in various ways. You can read all the details about manage.py on the Django Project website.
* The inner mysite/ directory. 
    * It’s the Python package for your project. It’s the name you’ll use to import anything inside it (e.g. mysite.urls).
* mysite/__init__.py. 
    * An empty file that tells Python that this directory should be considered a Python package. (Read more about packages in the official Python docs if you’re a Python beginner.).
* mysite/settings.py. 
    * Settings/configuration for this Django project. Appendix D will tell you all about how settings work.
* mysite/urls.py. 
    * The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in Chapters 2 and 7.
* mysite/wsgi.py. 
    * An entry-point for WSGI-compatible web servers to serve your project. See Chapter 13 for more details.

!SLIDE
## Start the web server
Run the following code in the command line.
~~~~{python}
python manage.py runserver 
~~~~

You will see this in the command line.
~~~~{python}
Performing system checks...

0 errors found June 12, 2016 - 08:48:58 Django version 1.8.13, using settings 'mysite\
.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
~~~~

!SLIDE
## It just works!
* Then open your browser and go to the address of http://127.0.0.1:8000/
* CONGRATULATIONS! It works!

![sample django page](django-it-worked-page.png)

!SLIDE
## The Model-View-Controller Design Pattern
* The model(M) is a model or representation of your data. 
* The view(V) is what you see. 
* The controller(C) controls the flow of information between the model and the view. 

!SLIDE
## Hello, Django, change views.py
* add views.py under /mysite/
* put the following code in views.py
~~~~{python}
from django.http import HttpResponse  

def hello(request):
    return HttpResponse("Hello django")
~~~~

!SLIDE
## update urls.py
* add views.py under /mysite/
* put the following code in views.py
~~~~{python}
from django.conf.urls import include, url
from django.contrib import admin
from mysite.views import hello  
urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', hello),
]
~~~~

!SLIDE
## match the site root
*  use the URLpattern “^$”

~~~~{python}
from django.conf.urls import include, url
from django.contrib import admin
from mysite.views import hello  
urlpatterns = [
    url(r'^$', hello),   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/$', hello),
]
~~~~

!SLIDE
## dynamic website
~~~~{python}
from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "It is now %s." % now
    return HttpResponse(html)
~~~~

!SLIDE
## Use a webpage template
* add the template directory in settings.py
~~~~{python}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'C:\Users\zoomq\Desktop\Computer Applications for Social Scientists\Lecture 17. An Introduction to Django\homepage\mysite\templates'
        ],
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
~~~~


!SLIDE
## Use a webpage template
* Renders variables in the views.py
~~~~{python}
from django.http import HttpResponse
from django.shortcuts import render
import datetime

def current_datetime2(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})
~~~~


!SLIDE
## Use a webpage template
* code for the html template
~~~~{python}
from django.http import HttpResponse
from django.shortcuts import render
import datetime

def current_datetime2(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})
~~~~