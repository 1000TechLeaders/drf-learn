from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Task
from .utils import check_datetime, send_activation_email


class TaskSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source='owner.first_name', read_only=True,
    )
    created_at = serializers.DateTimeField(validators=[check_datetime])
    expired_at = serializers.DateTimeField(validators=[check_datetime])

    class Meta:
        model = Task
        fields = [
            'name', 'first_name', 'description',
            'completed', 'level',
            'created_at', 'expired_at'
        ]
        read_only_fields = ['completed', ]

    def validate_level(self, value):
        if value > 10 or value < 0:
            raise serializers.ValidationError(
                "Le niveau doit etre compris entre 0 et 10"
            )
        return value

    def validate_name(self, value):
        if Task.objects.filter(name=value).exists():
            raise serializers.ValidationError("")
        return value

    def validate(self, data):
        if data['created_at'] > data['expired_at']:
            raise serializers.ValidationError(
                "La date d'expiration doit etre superieur a la date creation"
            )
        return data

    def create(self, validated_data):
        instance = Task.objects.created(**validated_data)
        send_activation_email(user=instance.owner)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance
