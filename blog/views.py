from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Journal, Project, Topic

def home(request):
	journal_entries = Journal.objects.all()[:4]
	current_project = Project.objects.all().order_by('last_entry')[:1]
	
	return render(request, 'home.html', {'entries': journal_entries, 'current_project': current_project})

