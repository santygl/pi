import urlparse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from PI.forms import UserCreateForm

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import oauth2 as oauth
import cgi
import urllib
import requests as r
import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from PI.models import Twitter

@csrf_protect
def register(request, template_name='registration/register2.html',
             redirect_field_name=REDIRECT_FIELD_NAME,
             extra_context=None):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        context = None
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            current_site = get_current_site(request)
            context = {
                'form': form,
                redirect_field_name: redirect_to,
                'site': current_site,
                'site_name': current_site.name,
            }
            if extra_context is not None:
                context.update(extra_context)

            return TemplateResponse(request, template_name, context)

    else:
        form = UserCreateForm()  # An unbound form
        current_site = get_current_site(request)
        context = {
            'form': form,
            redirect_field_name: redirect_to,
            'site': current_site,
            'site_name': current_site.name,
        }
        if extra_context is not None:
            context.update(extra_context)

        return TemplateResponse(request, template_name, context)


def index(request, template_name='index.html',
          extra_context=None):
    context = {}
    if request.user.is_anonymous():
        return HttpResponseRedirect(reverse('login'))
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@never_cache
def twitter_link(request):
    request_token_url = 'https://twitter.com/oauth/request_token?oauth_callback=' + urllib.quote_plus(
        'http://127.0.0.1:8000/twitter_authenticated/')
    consumer = oauth.Consumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    authenticate_url = 'https://twitter.com/oauth/authenticate'
    client = oauth.Client(consumer)
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        print(content)
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(urlparse.parse_qsl(content))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
                                 request.session['request_token']['oauth_token'])
    return HttpResponseRedirect(url)


@login_required
def twitter_authenticated(request):
    consumer = oauth.Consumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    access_token_url = 'https://twitter.com/oauth/access_token'
    verifier_token = request.GET['oauth_verifier']
    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
                        request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    body = urllib.urlencode(dict(oauth_verifier=verifier_token))

    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "POST", body=body)
    if resp['status'] != '200':
        print(content)
        raise Exception("Invalid response from Twitter.")

    access_token = dict(cgi.parse_qsl(content))

    # Step 3. Lookup the user or create them if they don't exist.
    user = request.user

    # Save our permanent token and secret for later.
    profile = Twitter()
    profile.user = user
    profile.oauth_token = access_token['oauth_token']
    profile.oauth_secret = access_token['oauth_token_secret']
    profile.save()

    # Authenticate the user and log them in using Django's pre-built
    # functions for these things.

    return HttpResponseRedirect(reverse('index'))
