from django.db import models
from django.contrib.auth.models import User

class Request(models.Model) :
    title = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    date = models.DateField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bookmark = models.IntegerField(verbose_name="북마크개수", default=0)
    ifbookmark = models.BooleanField(verbose_name="북마크여부", default=False)
    
    def __str__(self) :
        return str(self.title)
    
class Curation(models.Model) :
    content = models.URLField(verbose_name="링크")
    request = models.ForeignKey(Request, on_delete=models.CASCADE, default=None)
    date = models.DateField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) :
        return self.content
    
class Recommend(models.Model) :
    title = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    date = models.DateField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bookmark = models.IntegerField(verbose_name="북마크개수", default=0)
    ifbookmark = models.BooleanField(verbose_name="북마크여부", default=False)
    
    def __str__(self) :
        return str(self.title)
    
class Popular(models.Model) :
    title = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    date = models.DateField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bookmark = models.IntegerField(verbose_name="북마크개수", default=0)
    ifbookmark = models.BooleanField(verbose_name="북마크여부", default=False)
    
    def __str__(self) :
        return str(self.title)

class MyBookmark(models.Model) :
    title = models.CharField(verbose_name="제목", max_length=200)
    content = models.TextField(verbose_name="내용")
    date = models.DateField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bookmark = models.IntegerField(verbose_name="북마크개수", default=0)
    ifbookmark = models.BooleanField(verbose_name="북마크여부", default=False)