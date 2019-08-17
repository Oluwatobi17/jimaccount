from django import forms
from .models import User, Investment


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password', 'email', 'role']


class InvestmentForm(forms.ModelForm):
	class Meta:
		model = Investment
		fields = ['interest_rate', 'amount', 'investmentDate']
