from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Journal, Project

def home(request):
	journal_entries = Journal.objects.all()[:4]
	current_project = Project.objects.all().order_by('last_entry')[:1]
	article_entries = Article.objects.all()[:4]
	
	return render(request, 'home.html', {'journal_entries': journal_entries, 'current_project': current_project, 'article_entries': article_entries})

def journal_entry(request, slug):
	journal_slug = get_object_or_404(Journal, slug = slug)
	return render(request, 'journal.html', {'journal': journal_slug})

def article(request, slug):
	article_slug = get_object_or_404(Article, slug = slug)
	return render(request, 'articles.html', {'article': article_slug})