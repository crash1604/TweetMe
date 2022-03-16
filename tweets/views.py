import json
from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.conf import settings 
from .serializers import ( 
    TweetSerializer,
    TweetActionSerializer,
    TweetCreateSerializer
)

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.http import is_safe_url

from .models import Tweet 
from .forms import TweetForm 

ALLOWED_HOSTS = settings.ALLOWED_HOSTS 



@api_view(['GET'])
# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
def tweetlistview(request, *args, **kwargs):
    qs= Tweet.objects.all()
    serializer= TweetSerializer(qs, many=True)
    return Response(serializer.data, status=201)

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def TweetActionView(request, *args,**kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=200)
    return Response({}, status=200)

    # # action view that handles like unlike retweet etc.
    # serializer= TweetActionSerializer(data=request.POST)
    # if serializer.is_valid(raise_exception=True):
    #     data = serializer.validated_data()
    #     tweet_id=data.get("id")
    #     action=data.get("action")
    # qs= Tweet.objects.filter(id=tweet_id)
    # if not qs.exists():
    #     return Response({},status=404)
    # obj= qs.first()
    # if action =="unlike":
    #     obj.likes.remove(request.user)
    # elif action=="like":
    #     obj.likes.add(request.user)
    # elif action=="retweet":
    #     #to be implemented
    #     pass
    # return Response({}, status=201)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detailview(request, tweet_id, *args, **kwargs):
    qs= Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj=qs.first()
    serializer= TweetSerializer(obj)
    return JsonResponse(serializer.data, status=201)  

@api_view(['POST']) #http method the client == POST
@permission_classes([IsAuthenticated])
def tweetCreateView_DRF(request, *args,**kwargs):
    serializer= TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201) 
    return Response({},status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs= Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs=qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":'You cannot delete the tweet without permissions'}, status=401)
    obj=qs.first()
    obj.delete()
    return Response({"message":'delete was successful'}, status=200)


def homeview(request, *args,**kwargs):
    # return HttpResponse('<H1>Foo blah </H1>')
    return render(request, 'pages/home.html', context={}, status=200) 


# PURE DJANGO VIEWS 

def detailview_pure_django(request, tweet_id, *args,**kwargs):
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

def tweetlistview_pure_django(request, *args, **kwargs):
    if not request.user.is_authenticated:
        if request.is_ajax():
            return JsonResponse({}, status=401)
    qs= Tweet.objects.all()
    tweetList=[ x.serialize() for x in qs]
    data= {
        "isUser": False,
        "response": tweetList }
    return JsonResponse(data)  

def tweetCreateView_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})
