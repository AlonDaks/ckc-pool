from django.template import Context, loader, Template, RequestContext
from django.template.loader import get_template
from ranking_app.models import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from decimal import *

def register(request, error=None):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if form.clean_password():
                user = form.save()
                return HttpResponseRedirect("/AccountCreated/")
            else:
                return HttpResponseRedirect("/Register/Password")
    else:
        form = RegistrationForm()
    return render_to_response("create_user.html", {
        'form': form, 'error': error,
    }, context_instance=RequestContext(request))

def record_match(request):
    if request.method == 'POST':
        form = MatchEntryForm(request.POST)
        if form.is_valid():
            form.save()
            elo_update(form.winner_id, form.looser_id)
            return HttpResponseRedirect("/Rankings/")
    else:
        form = MatchEntryForm()
    return render_to_response("record_match.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def account_created(request):
	return render_to_response("account_created.html", {})

def rankings(request):
    ranking_objects = Ranking.objects.order_by('-rating')
    prev, ranks, rank_counter = None, [], 0
    for elem in ranking_objects:
        name = elem.user.first_name+" "+elem.user.last_name
        rank_counter+=1
        if prev and elem.rating == prev.rating:
            previous_rank = ranks[-1][0]
            ranks.append([previous_rank, name, str(elem.rating)[:8]])
        else:
            ranks.append([rank_counter, name, str(elem.rating)[:8]])
        prev = elem
    return render_to_response("rankings.html", {'ranks':ranks})

def elo_update(winner_id, looser_id):
    winner = Ranking.objects.get(user_id=winner_id)
    looser = Ranking.objects.get(user_id=looser_id)
    winner.num_wins+=1
    winner.num_matches+=1
    looser.num_matches+=1
    winner_rating, looser_rating = winner.rating, looser.rating
    estimate_winner = calculate_estimate(winner_rating, looser_rating)
    estimate_looser = calculate_estimate(looser_rating, winner_rating)
    winner.rating += 32*(1-estimate_winner)
    looser.rating += 32*(-estimate_looser)

    winner.save()
    looser.save()

def calculate_estimate(rating_a, rating_b):
    return (Decimal(1)/(1+10**((rating_b-rating_a)/Decimal(400))))