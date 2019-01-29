"""kinkgarden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

urlpatterns = [
    path('', lambda request: HttpResponse("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>kink.garden - coming soon</title>
    <style>
        body {
            width: 40em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
</head>
<body>
<h1>kink.garden</h1>
<h2>share your kinks with your friends, or the world</h2>
<p>kink.garden is a work in progress. coming soon, hopefully!</p>
<p>in the meantime, feel free to follow us on <a href="https://twitter.com/kinkgarden">Twitter</a>.</p>
<h4>what is this?</h4>
<p>kink.garden is a project that aims to create a website where you can make a <b>list of your kinks</b> that you can
    share with friends, the world, or no one but yourself!</p>
<p>this project was started and conceptualized <b>by queer people, for queer people.</b> it is being built from the
    ground up to be queer-inclusive, always with respectfulness in mind. you won't have to worry about bigotry,
    objectifying slurs, or tastelessly fetishizing marginalized people.</p>

</body>
</html>
""")),
    path('kinks/', include('kinks.urls')),
    path('admin/', admin.site.urls),
]
