# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
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
    author = serializers.CharField()

    class Meta:
        model = Menu
        fields = ['id', 'meals', 'scheduled_at', 'author']


class MealModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = '__all__'

    many = True
