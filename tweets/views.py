from typing import ContextManager
from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse, Http404

from .models import Tweet 

def tweetlistview(request, *args, **kwargs):
    qs= Tweet.objects.all()
    tweetList=[ {"id":x.id, "content":x.content} for x in qs]
    data= {
        "isUser": False,
        "response": tweetList }
    return JsonResponse(data)  

def homeview(request, *args,**kwargs):
    # return HttpResponse('<H1>Foo blah </H1>')
    return render(request, 'pages/home.html', context={}, status=200) 

def detailview(request, tweet_id, *args,**kwargs):
    """
    REST API VIEW
    CONSUMED BY JS, ANDROID , JAVA, IOS
    RETURN JSON
    """
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404

    data={
        "id": tweet_id,
        "content":obj.content,
        # "image_path":obj.image.url,
    }
    return JsonResponse(data)