# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import datetime
from django.contrib.messages import error

#========================================================================#
#                               RENDER METHODS                           #
#========================================================================#

def index(request):
    return render(request, "login/index.html")

def signin(request):
    return render(request, "login/signin.html")

def logout(request):
    del request.session['user_id']
    return redirect('/signin')

def register(request):
    return render(request, 'login/register.html')

def new(request):
    context = {
        "user_level" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'login/new.html', context)

def edit(request, id):
    context = {
        "user" : User.objects.get(id=id),
        "user_level" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'login/edit.html', context)

def show(request, id):
    context = {
        "users" : User.objects.get(id=id),
        "user_messages" : Message.objects.filter(user_id = id),
        "user_level" : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'login/show.html', context)

def destroy(request, id):
    User.objects.get(id=id).delete()
    return redirect('/dashboard/admin')

#========================================================================#
#                                PROCESS METHODS                         #
#========================================================================#

def edit_process(request, action):
    if request.method == "POST":
        if action == "info":
            info_user = User.objects.edit_info_validator(request.POST)
            if info_user['status'] == "bad":
                for error in info_user['data']:
                    messages.error(request, error)
                return redirect('/login/edit/' + str(request.POST['user_id']))
            else:
                messages.add_message(request, messages.INFO, "Profile successfully updated!")
                print (request.POST['user_type'])
                return redirect('/login/edit/' + str(request.POST['user_id']))

        elif action == "password":
            pass_user = User.objects.edit_password_validator(request.POST)
            if pass_user['status'] == "bad":
                for error in pass_user['data']:
                    messages.error(request, error)
                return redirect('/login/edit/' + str(request.POST['user_id']))
            else:
                messages.add_message(request, messages.INFO, "Profile successfully updated!")
                return redirect('/login/edit/' + str(request.POST['user_id']))

        elif action == "description":
            description_user = User.objects.edit_description_validator(request.POST)
            if description_user['status'] == "bad":
                messages.error(request, description_user['data'])
                return redirect('/login/edit/' + str(request.POST['user_id']))
            else:
                messages.add_message(request, messages.INFO, "Profile successfully updated!")
                return redirect('/login/edit/' + str(request.POST['user_id']))
    else:
        return redirect('/dashboard')


def process(request, action):
    if request.method == "POST":
        if action == "register":
            reg_user = User.objects.registration_validator(request.POST)
            if reg_user['status'] == "bad":
                for error in reg_user['data']:
                    messages.error(request, error)
                return redirect('/register')
            else:
                request.session['user_id'] = reg_user['data'].id
                if reg_user['data'].user_level == 9000:
                    return redirect('/dashboard/admin')
                else:
                    return redirect('/dashboard')

        elif action == "signin":
            log_user = User.objects.signin_validator(request.POST)
            if log_user['status'] == "bad":
                    messages.error(request, log_user['data'])
                    return redirect('/signin')
            else:
                request.session['user_id'] = log_user['data'].id
                if log_user['data'].user_level == 9000:
                    return redirect('/dashboard/admin')
                else:
                    return redirect('/dashboard')

        elif action == "new":
            new_user = User.objects.registration_validator(request.POST)
            if new_user['status'] == "bad":
                for error in new_user['data']:
                    messages.error(request, error)
                    return redirect('/login/new')
            else:
                return redirect('/dashboard/admin')

        elif action == "message":
            new_message = Message.objects.message_validator(request.POST)
            if new_message['status'] == "bad":
                messages.error(request, new_message['data'])
                return redirect('/login/show/' + str(new_message['data'].user_id))
            else:
                return redirect('/login/show/' + str(new_message['data'].user_id))

        elif action == "comment":
            new_comment = Comment.objects.comment_validator(request.POST)
            if new_comment['status'] == "bad":
                messages.error(request, new_comment['data'])
                return redirect('/login/show/' + str(request.POST['user_id']))
            else:
                return redirect('/login/show/' + str(request.POST['user_id']))
    else:
        return redirect('/signin')

