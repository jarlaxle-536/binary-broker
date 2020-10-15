from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers

from .models import *

class AssetSerializer(serializers.ModelSerializer):

    diff = serializers.ReadOnlyField()
    _diff = serializers.ReadOnlyField()

    class Meta:
        model = Asset
        fields = ('id', 'name', 'price', 'mean_price', 'diff', '_diff')
