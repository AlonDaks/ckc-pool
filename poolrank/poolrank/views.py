from django.template import Context, loader, Template, RequestContext
from django.template.loader import get_template
from ranking_app.models import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/AccountCreated/")
    else:
        form = RegistrationForm()
    return render_to_response("create_user.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def account_created(request):
	return render_to_response("account_created.html", {})

