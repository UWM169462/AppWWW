from rest_framework import serializers
from django.utils import timezone
from .models import Category, Topic, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class TopicSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'category', 'category_name', 'created']
        read_only_fields = ['id', 'created']


class PostSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)
    category_name = serializers.CharField(source='topic.category.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'text',
            'topic',
            'topic_name',
            'category_name',
            'slug',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_username'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

        def validate_title(self, value):
            if not all(char.isalpha() or char.isspace() for char in value):
                raise serializers.ValidationError(
                    "Nazwa posta może zawierać tylko litery i spacje!"
                )
            return value

        def validate_created_at(self, value):
            if value > timezone.now():
                raise serializers.ValidationError(
                    "Data dodania nie może być z przyszłości!"
                )
            return value


# Serializator ogólny (nie dziedziczący po ModelSerializer)
class CategoryGeneralSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=60)
    description = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance