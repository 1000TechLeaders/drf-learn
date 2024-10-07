from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Task, Category
from .utils import check_datetime, send_activation_email


class OwnerTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
        read_only_fields = fields


class CategoryTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'created_at')
        read_only_fields = ('created_at', )


class TaskSerializer(serializers.ModelSerializer):
    owner = OwnerTaskSerializer(read_only=True)
    created_at = serializers.DateTimeField(validators=[check_datetime], write_only=True)
    expired_at = serializers.DateTimeField(validators=[check_datetime], write_only=True)
    category = CategoryTaskSerializer()

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description',
            'completed', 'level', 'category', 'owner',
            'created_at', 'expired_at'
        ]
        read_only_fields = ['completed',]


    def validate_level(self, value):
        if value > 10 or value < 0:
            raise serializers.ValidationError(
                "Le niveau doit etre compris entre 0 et 10"
            )
        return value

    def validate_name(self, value):
        if Task.objects.filter(name=value).exists():
            raise serializers.ValidationError("Nom de tache unique")
        return value

    def validate(self, data):
        if data.get('created_at') and data.get('expired_at'):
            if data['created_at'] > data['expired_at']:
                raise serializers.ValidationError(
                    "La date d'expiration doit etre superieur a la date creation"
                )
        return data

    def create(self, validated_data):
        instance = Task.objects.create(**validated_data)
        # send_activation_email(user=instance.owner)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'created_at', 'tasks')
        read_only_fields = ['created_at', 'tasks']
