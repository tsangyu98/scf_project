from rest_framework import serializers
from answers.models import Label


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label
        fields = ('id', 'label_name')
