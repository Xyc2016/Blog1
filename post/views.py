from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Article, Comment
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request, page='1'):
    if request.user.is_authenticated:
        article_list = Article.objects.filter(show=True)
    else:
        article_list = Article.objects.filter(private=False, show=True)
    paginator = Paginator(article_list, 7)
    articles = paginator.page(int(page))
    return render(request, 'post/index.html', {'articles': articles, })


def get_json(request):
    return JsonResponse({
        'result': request.GET['arg'] * 15
    })





def all_articles(request, page):
    if request.user.is_authenticated:
        article_list = Article.objects.all()
    else:
        article_list = Article.objects.filter(private=False)
    paginator = Paginator(article_list, 7)
    page = int(page)
    articles = paginator.page(page)
    return render(request, 'post/all_articles.html', {'articles': articles, })


# @login_required
def dlt_article(request, article_id):
    get_object_or_404(Article, id=article_id).delete()
    return HttpResponseRedirect(reverse('post:index'))


# @login_required
def to_public(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.private = False
    article.save()
    return HttpResponseRedirect(reverse('post:index'))


# @login_required
def to_private(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.private = True
    article.save()
    return HttpResponseRedirect(reverse('post:index'))


# @login_required
def write(request):
    return render(request, 'post/write.html')


class DetailView(generic.DetailView):
    model = Article
    template_name = 'post/detail.html'
    context_object_name = 'article'


# @login_required
def edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'GET':
        return render(request, 'post/edit.html', {'article': article})
    elif request.method == 'POST':
        article.title = request.POST['title']
        article.text = request.POST['text']
        article.edit_date = timezone.now()
        article.save()
        return HttpResponseRedirect(reverse('post:detail', args=(article.id,)))


def add_comment(request, article_id):
    comment = Comment(article=Article.objects.get(
        pk=article_id), text=request.POST['text'],
        pub_date=timezone.now(), visitor=request.POST['visitor'])
    comment.save()
    return HttpResponseRedirect(reverse('post:detail', args=(article_id,)))


def create(request):
    article = Article(title=request.POST['title'],
                      text=request.POST['text'],
                      pub_date=timezone.now())
    article.save()
    return HttpResponseRedirect(reverse('post:index'))
