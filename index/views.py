from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, InvestmentForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages
from .models import User, Investment, Capitallog

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CapitallogSerializer, CapitalflowSerializer
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
import random


def index(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_active:
				login_user(request, user)
				return redirect(account)

			messages.error(request, 'Your account has been disabled')
			return redirect(index)
		
		messages.error(request, 'Invalid login')
		return redirect(index)

	return render(request, 'login.html', {
		'title': 'Jimnet account sign in'
		})

def profile(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			email = request.POST['email']
			currentpass = request.POST['currentpassword']
			newpass = request.POST['newpassword']
			newpass2 = request.POST['newpassword2']

			user = User.objects.get(username=request.user.username)
			if first_name and last_name and email:
				if user.check_password(currentpass):
					if newpass:
						if newpass==newpass2:
							user.set_password(newpass)
						else:
							messages.error(request, 'Password 1 does not match password 2')
							return redirect(profile)
					user.first_name = first_name
					user.last_name = last_name
					user.email = email
					user.save()
					messages.success(request, 'Profile updated')
					return redirect(profile)

				messages.error(request, 'Current password does not match the one specified')
				return redirect(profile)

			messages.error(request, 'Please fill the neccessary fields')
			return redirect(profile)

		return render(request, 'profile.html', {
			'title': 'Edit your profile',
			'user': User.objects.get(username=request.user.username)
		})

	return redirect(index)

# Compute the total input and output of a log
def totalInputOutput(log):
	totinput = 0; totoutput = 0;
	if log:
		for i in log.account_set.all():
			if i.accType=='input':
				totinput += i.amount
			else:
				totoutput += i.amount

	return [totinput, totoutput]
def account(request):
	if request.user.is_authenticated:
		lastlog = []
		if Capitallog.objects.count():
			lastlog = Capitallog.objects.all()[len(Capitallog.objects.all())-1]
			
		return render(request, 'index.html', {
			'title': 'Jimnet account',
			'lastlog': lastlog,
			'totinput': totalInputOutput(lastlog)[0],
			'totoutput': totalInputOutput(lastlog)[1],
			'logs': Capitallog.objects.all(),
			'user': User.objects.get(username=request.user.username)
			})

	return redirect(index)

def investments(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			form = InvestmentForm(request.POST)
			if form.is_valid():
				investment = form.save(commit=False)
				investment.investor = User.objects.get(pk=request.POST['investor'])
				investment.save()

				messages.success(request, 'Investment added')
				return redirect(investments)

			messages.error(request, 'Please fill all input')
			return redirect(investments)

		return render(request, 'investments.html', {
			'title': 'Jimnet investments',
			'investors': User.objects.all(),
			'user': User.objects.get(username=request.user.username)
		})

	return redirect(index)

def register(request):
	if request.method=='POST':
		form = UserForm(request.POST)
		if form.is_valid():
			if request.POST['password']==request.POST['password2']:

				if request.POST['pincode']=='inception':

					user = form.save(commit=False)
					username = form.cleaned_data['username']
					password = form.cleaned_data['password']
					user.set_password(password)

					user.save()
					user = authenticate(request, username=username, password=password)
					if user is not None:
						login_user(request, user)
						# user = User.objects.filter(user=request.user)
						messages.success(request, 'Registration successful.')
						return redirect(account)
				else:
					messages.error(request, 'Wrong creation pin')
					return redirect(register)
			else:
				messages.error(request, 'Password 1 does not match password 2')
				return redirect(register)
		
		messages.error(request, 'Please ensure the all the field are filled')
		return redirect(register)
	else:
		return render(request, 'register.html', {
			'title': 'Jimnet account sign up'
		})

def forgetpassword(request):
	if request.method=='POST':
		username = request.POST['username']
		if username:
			if User.objects.filter(username=username):
				user = User.objects.get(username=username)
				newpass = random.randint(100000, 1000000)

				message = 'Hello, your new password is ' + str(newpass)
				user.set_password(newpass)
				user.save()
				res = send_mail("Jim Account password reset", message, "support@Jimnet.com",[user.email], fail_silently=True)
				if res:
					messages.success(request, 'A mail has been sent to your mail, please check')
					return redirect(index)

				messages.error(request, 'Error sending mail to your email')
				return redirect(index)

			messages.error(request, 'Username specified does not exist')
			return redirect(index)
		messages.error(request, 'Please specify your username')
		return redirect(index)

	return redirect(index)

def logout(request):
	logout_user(request)
	return redirect(index)



class Createcapitallog(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		serializer = CapitallogSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response(False)

class CapitalFlow(APIView):
	permission_classes = (IsAuthenticated, )

	def post(self, request):
		serializer = CapitalflowSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response(False)


class AccountLog(APIView):
	permission_classes = (IsAuthenticated, )

	def get(self, request, pk):
		if Capitallog.objects.filter(pk=pk):
			data = Capitallog.objects.get(pk=pk).account_set.all()
			serializer = CapitalflowSerializer(data, many=True)
			val = [serializer.data, totalInputOutput(Capitallog.objects.get(pk=pk))]

			return Response(val)

		return Response(False)



		serializer = CapitalflowSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response(False)