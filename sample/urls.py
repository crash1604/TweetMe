"""sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from tweets.views import tweetCreateView_DRF
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from tweets.views import ( 
    homeview,
    detailview,
    tweetlistview,
    tweetCreateView_DRF,
    tweet_delete_view,
    TweetActionView,
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homeview),
    path('react/',TemplateView.as_view(template_name='react.html')),
    path('tweets/<int:tweet_id>/', detailview),
    path('tweets/', tweetlistview ),
    path('create-tweet', tweetCreateView_DRF),
    path('api/tweets/',include('tweets.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
