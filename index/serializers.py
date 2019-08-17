from rest_framework import serializers
from .models import Capitallog, Account

class CapitallogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Capitallog
		fields = '__all__' 

class CapitalflowSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = '__all__' 