# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
# from rest_framework_recaptcha.fields import ReCaptchaField
from dashboard.models import (
    Menu,
    Meal,
)


class MenuModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = '__all__'


class MealLinkedModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Meal
        fields = ['id', 'title']
        

class MenuModelListSerializer(serializers.ModelSerializer):
    
    id = serializers.CharField()
    meals = MealLinkedModelSerializer(read_only=True, many=True)
    scheduled_at = serializers.DateField()
    
    class Meta:
        model = Menu
        fields = ['id', 'meals', 'scheduled_at']
    

class MealModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = '__all__'

    many = True


