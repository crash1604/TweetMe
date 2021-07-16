from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.conf import settings 

from django.utils.http import is_safe_url

from .models import Tweet 
from .forms import TweetForm 

ALLOWED_HOSTS = settings.ALLOWED_HOSTS 

def tweetlistview(request, *args, **kwargs):
    qs= Tweet.objects.all()
    tweetList=[ {"id":x.id, "content":x.content, "likes":12 } for x in qs]
    data= {
        "isUser": False,
        "response": tweetList }
    return JsonResponse(data)  

def tweetCreateView(request, *args, **kwargs):
    next_url=request.POST.get("next") or None
    print(next_url)
    form= TweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            obj= form.save(commit=False)
            obj.save()
            if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
                return redirect(next_url)
            form = TweetForm() 
        return render(request,'components/form.html', context={"form": form})
    if request.method == "GET":
        return render(request,'components/form.html', context={"form":form})

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