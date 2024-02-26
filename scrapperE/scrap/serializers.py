from rest_framework import serializers
from .models import PostRaw,CommentRaw,ErrorPost,BitstampData,BitstampDataHour,BitstampDataMinute,ErrorLog

class PostRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostRaw
        fields = '__all__'


class BitstampDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitstampData
        fields = '__all__'

class BitstampDataHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitstampDataHour
        fields = '__all__'

class BitstampDataMinuteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BitstampDataMinute
        fields = '__all__'

class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'