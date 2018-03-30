from rest_framework import serializers
from .models import *


class IdiomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idioms
        exclude = []
