from rest_framework import serializers
from api.models import *


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ('id','titre', 'dateCreation', 'dateModification','urlDepart')