from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Article, Comment
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django import forms


# Create your views here.



class CommentForm(forms.Form):
    name = forms.CharField()
    url = forms.URLField()
    comment = forms.CharField(widget=forms.Textarea)
    private = forms.CheckboxInput()


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


class ArticleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Input the title',

    }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write the Article',
    }))
    private = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        # 'class': 'form-control',
    }), required=False)
    show = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        # 'class':'form-control',
    }), required=False)


# @login_required
def write(request):
    articleform = ArticleForm()
    return render(request, 'post/write.html', {
        'articleform': articleform,
    })


class DetailView(generic.DetailView):
    model = Article
    template_name = 'post/detail.html'
    context_object_name = 'article'


# @login_required
def edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'GET':
        articleform = ArticleForm(
            data={
                'title': article.title,
                'text': article.text,
                'private': article.private,
                'show': article.show,
            })
        return render(request, 'post/edit.html', {'article': article,
                                                  'articleform': articleform}, )
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
                      show=request.POST.get('show', False),
                      private=request.POST.get('private', False),
                      pub_date=timezone.now())
    article.save()
    return HttpResponseRedirect(reverse('post:index'))
