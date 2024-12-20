from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category
from .models import Task
from .tasks import send_notification_email
from .utils import check_datetime
# from .utils import send_activation_email


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
    created_at = serializers.DateTimeField(validators=[check_datetime])
    expired_at = serializers.DateTimeField(validators=[check_datetime])
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
        if not (0 < value <= 10):
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
                    "La date d'expiration doit etre superieur a la date "
                    "creation"
                )
        return data

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.create(**category_data)
        instance = Task.objects.create(**validated_data, category=category)
        # asycn execution
        if instance.owner:
            send_notification_email.apply_async(kwargs={
                'email': instance.owner.email,
                'first_name': instance.owner.first_name,
                'last_name': instance.owner.last_name
            })
        # sync execution
        # send_notification_email(
        #     instance.owner.email,
        #     instance.owner.first_name,
        #     instance.owner.last_name
        # )
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.save()

        return instance


class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'created_at', 'tasks')
        read_only_fields = ['created_at', 'tasks']
