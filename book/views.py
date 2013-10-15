#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from book.models import Book

def home(request):
	obj_list = Book.objects.all()
	return render_to_response("home.html", locals(), context_instance=RequestContext(request))
