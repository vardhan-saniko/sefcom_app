from django.shortcuts import render

# Create your views here.

import re
import json
import base64
import requests

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.template import loader

from globus_sdk import ConfidentialAppAuthClient
from sefcom_auth.models import Profile
from globus_sdk import AuthClient, AccessTokenAuthorizer

CLIENT_ID = "47c16d66-ec8f-417c-9cfa-6d15b8deb0f6"
CLIENT_SECRET = "ya72FHPPSARQWwwDNQegNWKqHAqaK3Kcc93gPviBmsk="

def index(request):
    user = User.objects.first()
    profile = Profile.objects.filter(user=user).last()
    tokens = ""
    client = ConfidentialAppAuthClient(CLIENT_ID, CLIENT_SECRET)
    profile_data = {}
    template = loader.get_template('index.html')
    if profile:
        profile_data = profile.__dict__
        tokens = json.loads(profile.tokens)
    is_active = client.oauth2_validate_token(tokens['access_token']) if profile else {"active": False}
    context = {"tokens": tokens, "is_active": "yes" if is_active['active'] else "No", "profile": profile_data}
    print(context)

    return HttpResponse(template.render(context, request))

def vishnu(request):
    return HttpResponse("Hello, vishnu.")

def auth(request):
    redirect_uri = "http://localhost:8000/authcallback"
    client = ConfidentialAppAuthClient(CLIENT_ID, CLIENT_SECRET)
    client.oauth2_start_flow(redirect_uri, refresh_tokens=True, requested_scopes=["openid", "profile", "email", "urn:globus:auth:scope:transfer.api.globus.org:all"],)
    auth_uri = client.oauth2_get_authorize_url()
    print(auth_uri)
    return redirect(auth_uri)

def auth_callback(request):
    redirect_uri = "http://localhost:8000/authcallback"
    url = request.get_full_path()
    code = re.search("code=(.*?)&state", url).group(1)
    # client = ConfidentialAppAuthClient(CLIENT_ID, CLIENT_SECRET)
    # client.oauth2_start_flow(redirect_uri, refresh_tokens=True, requested_scopes=["openid", "profile", "email", "urn:globus:auth:scope:transfer.api.globus.org:all"], )
    # tokens = dict(client.oauth2_exchange_code_for_tokens(code))
    # print(tokens)
    auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
    auth_b64 = base64.b64encode(auth_str.encode('ascii'))
    headers = {'Authorization': 'Basic {}'.format(auth_b64.decode("utf-8"))}
    # id_token = tokens.decode_id_token()
    response = requests.post("https://auth.globus.org/v2/oauth2/token?grant_type=authorization_code&code={}&redirect_uri={}".format(code, redirect_uri), headers=headers)

    data = json.loads(response.content)
    user = User.objects.first()
    print(data)
    ac = AuthClient(authorizer=AccessTokenAuthorizer(data['access_token']))
    info = ac.oauth2_userinfo()
    print(info)
    profile = Profile.objects.filter(email=info.get('email')).last()
    if profile:
        profile.tokens=json.dumps(data)
        profile.is_authenticated=True
        profile.save()
    else:
        profile = Profile.objects.create(user=user, is_authenticated=True, name=info.get('name'),email=info.get('email'), institution=info.get('organization'), primary_identity=info.get('sub'), tokens=json.dumps(data))
    return redirect("/")

def refresh_token(request):
    client = ConfidentialAppAuthClient(CLIENT_ID, CLIENT_SECRET)
    user = User.objects.first()
    profile = Profile.objects.filter(user=user).last()
    token = json.loads(profile.tokens)['refresh_token']
    token_data = client.oauth2_refresh_token(token)
    profile.tokens=json.dumps(token_data.data)
    profile.save()
    return redirect("/")

def revoke_token(request):
    client = ConfidentialAppAuthClient(CLIENT_ID, CLIENT_SECRET)
    user = User.objects.first()
    profile = Profile.objects.filter(user=user).last()
    token = json.loads(profile.tokens)['access_token']
    client.oauth2_revoke_token(token)
    return redirect("/")