from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Request, Recommend, Curation, MyBookmark, Popular


# Create your views here.

# 큐레이션 개수 받아오기
def get_count(reque):
    curation = Curation.objects.filter(request=reque)
    curation_count = curation.count()
    return curation_count

# request.html
@login_required
def request_board(request):
    request_list = Request.objects.all().order_by('-id')
    # 북마크 여부 확인 후 북마크 개수 받아서 계산
    if request.method == 'POST':
        clickBookmark = Request.objects.get('ifbookmark')
        bookmarkCount = Request.objects.get('bookmark')

        if clickBookmark == True:
            bookmarkCount += 1
        else:
            bookmarkCount -= 1
        request_list.save()

    # 큐레이션 개수 받아서 계산
    for reque in request_list :
        curation_count = get_count(reque)
        reque.curation_count = curation_count  # curation_count 로 사용 가능
    
    context = {
        'request_list' : request_list,
    }
    return render(request, 'request.html', context)

# create -> request 
@login_required
def reque_post(request):
    if request.method == 'POST' :
        title = request.POST.get('title')
        content = request.POST.get('content')
        Request.objects.create (
            title=title,
            content=content,
            writer=request.user
        )
        return redirect('playlistApp:request_board')
    else :
        return render(request, 'reque-write.html')

@login_required
def count_bookmark(request, id) :
    request_list = get_object_or_404(Request, pk=id)
    ifbookmark = request_list.ifbookmark
    bookmark = request_list.bookmark

    bookmark += 1

    # if ifbookmark == False:
    #     bookmark += 1
    #     request_list.ifbookmark == True

    # else:
    #     bookmark -= 1
    #     request_list.ifbookmark == False

    request_list.bookmark = bookmark
    request_list.save()

# detail page -> request 
def reque_detail(request, id) :
    request_list = get_object_or_404(Request, pk=id)

    count_bookmark(request, id)
    bookmark_count = request_list.bookmark
    request_list.bookmark_count = bookmark_count
    request_list.save()

    curation = Curation.objects.filter(request=id).order_by('-id')
    curation_count = get_count(request_list)
    request_list.curation_count = curation_count  # curation_count 로 사용 가능
    
    context = {
        'request_list' : request_list,
        'curation' : curation,
    }

    return render(request, 'reque_post.html', context) # detail 페이지 

#curation
@login_required
def create_curation(request, id) :
    if request.method == 'POST' :
        request_list = get_object_or_404(Request, id=id)
        content = request.POST.get('cu_content') # 링크 받아올 것 
        Curation.objects.create (
            content=content,
            writer=request.user,
            request=request_list
        )
        return redirect('playlistApp:reque_detail', request_list.id)  # request - detail 


# update -> request : 사용 안할 수 있음 우선 만듦
def reque_update(request, id) :
    request_list = get_object_or_404(Request, pk=id)
    curation = Curation.objects.filter(request=id).order_by('-id')
    if request.method == 'POST' :
        title = request_list.POST.get('title')
        content = request_list.POST.get('content')
        if title :
            request_list.title = title
        if content :    
            request_list.content = content
        request_list.save()
        return redirect('playlistApp:reque_detail', request_list.id) # detail 페이지 
    else :
        context = {
            'request_list' : request_list,
            'curation' : curation,
        }
        return render(request, 'reque-write.html', context) 
    
# delete -> request : 사용 안할 수 있음 
def reque_delete(request, id) :
    request_list = Request.objects.get(pk=id)
    request_list.delete()
    return redirect('playlistApp:request_board')

# 검색 기능
def reque_search(request) :
    if request.method == 'POST':
        searched = request.POST['searched']     
        request_list = Request.objects.filter(content__contains=searched)
        return render(request, 'reque_searched.html', {'searched': searched, 'request_list': request_list})
    else:
        return render(request, 'reque_searched.html', {})

#recommend
@login_required
def recommend_board(request):
    if request.method == 'POST':
        clickBookmark = Request.objects.get('ifbookmark')
        bookmarkCount = Request.objects.get('bookmark')

        if clickBookmark == True:
            bookmarkCount += 1
        else:
            bookmarkCount -= 1
        bookmarkCount.save()
        
    recomment_list = Recommend.objects.all().order_by('-id')
    context = {
        'recomment_list' : recomment_list
    }
    return render(request, 'recommend.html', context)

# create -> recommend
@login_required
def recom_post(request) :
    if request.method == 'POST' :
        title = request.POST.get('title')
        content = request.POST.get('content')
        Recommend.objects.create (
            title=title,
            content=content,
            writer=request.user
        )
        return redirect('playlistApp:recommend_board')
    else :
        return render(request, 'recommend-write.html')

# detail page -> recommend 
def recom_detail(request, id) :
    recommend = get_object_or_404(Recommend, pk=id)
    context = {
        'recommend' : recommend,
    }
    return render(request, 'recomm_board.html', context) # recommend detail 페이지 

# update -> recommend 
def recom_update(request, id) :
    recommend = get_object_or_404(Recommend, id=id)
    if request.method == 'GET' :
        context = {
            'recommend' : recommend,
        }
        return render(request, 'recommend-write.html', context) #detail 페이지 
    elif request.method == 'POST' :
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title :
            recommend.title = title
        if content:    
            recommend.content = content
        recommend.save()
        return redirect('playlistApp:recommend_detail', recommend.id) # detail 페이지 
    
# delete -> recommend 
def recom_delete(request, id) :
    recommend = Recommend.objects.get(pk=id)
    recommend.delete()
    return redirect('playlistApp:recommend_board')

def recom_search(request) :
    if request.method == 'POST':
        searched = request.POST['searched']        
        recommend = Recommend.objects.filter(content__contains=searched)
        return render(request, 'recommend_searched.html', {'searched': searched, 'recommend': recommend})
    else:
        return render(request, 'recommend_searched.html', {})

@login_required
def popular_board(request):
    Popular.objects.all().delete()

    request_top10 = Request.objects.all().order_by('-bookmark')[:10]
    recom_top10 = Recommend.objects.all().order_by('-bookmark')[:10]
    
    count = 0
    for request_item in request_top10:
        if Popular.objects.filter(title=request_item.title, content=request_item.content).exists():
            continue
        Popular.objects.create(
                title=request_item.title,
                content=request_item.content,
                date=request_item.date,
                writer=request_item.writer,
                bookmark=request_item.bookmark,
                ifbookmark=request_item.ifbookmark,
            )
        
        for recommend_item in recom_top10:
            if count == 9:
                break

            if Popular.objects.filter(title=recommend_item.title, content=recommend_item.content).exists():
                continue
            Popular.objects.create(
                title=recommend_item.title,
                content=recommend_item.content,
                date=recommend_item.date,
                writer=recommend_item.writer,
                bookmark=recommend_item.bookmark,
                ifbookmark=recommend_item.ifbookmark,
            )
            
            if request_item.bookmark > recommend_item.bookmark:
                Popular.objects.create(
                    title=request_item.title,
                    content=request_item.content,
                    date=request_item.date,
                    writer=request_item.writer,
                    bookmark=request_item.bookmark,
                    ifbookmark=request_item.ifbookmark,
                )
                break
            
            elif request_item.bookmark < recommend_item.bookmark:
                Popular.objects.create(
                    title=recommend_item.title,
                    content=recommend_item.content,
                    date=recommend_item.date,
                    writer=recommend_item.writer,
                    bookmark=recommend_item.bookmark,
                    ifbookmark=recommend_item.ifbookmark,
                )
                continue
            
            count += 1

    popular_list = Popular.objects.all().order_by('bookmark')
    context = {
        'popular_list' : popular_list
    }
    return render(request, 'popular_board.html', context)

def mypage(request):
    return render(request, 'mypage.html')

# 마이페이지 
def get_reque_bookmark(request) :
    request_list = Request.objects.all().order_by('-id')
    for reque in request_list :
        if reque.objects.get('ifbookmark') :
            MyBookmark.objects.create (
                title=reque.objects.get('title'),
                content=reque.objects.get('content'),
                date=reque.objects.get('date'),
                writer=reque.objects.get('writer'),
                bookmark=reque.objects.get('bookmark'),
                ifbookmark=reque.objects.get('ifbookmark'),
            )
    return render(request, 'mybookmark.html') # 만들 페이지 

def get_recom_bookmark(request) :
    recommend_list = Recommend.objects.all().order_by('-id')
    for recom in recommend_list :
        if recom.objects.get('ifbookmark') :
            MyBookmark.objects.create (
                title=recom.objects.get('title'),
                content=recom.objects.get('content'),
                date=recom.objects.get('date'),
                writer=recom.objects.get('writer'),
                bookmark=recom.objects.get('bookmark'),
                ifbookmark=recom.objects.get('ifbookmark'),
            )
    return render(request, 'mybookmark.html') # 만들 페이지 

def bookmark_board(request) :
    bookmark_list = MyBookmark.objects.all().order_by('-id')
    context = {
        'bookmark_list' : bookmark_list
    }
    return render(request, 'mybookmark.html') # 만들 페이지 