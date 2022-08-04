from rest_framework import serializers
from core.users.models import User
from core.contributors.models import Contributor
from core.projects.models import Project
from core.issues.models import Issue
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer class for User objects"""

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer class for creating a project"""

    class Meta:
        model = Project
        fields = ['title', 'description', 'type']

    def create(self, validated_data):
        # Creating project
        project = Project.objects.create(
            title=validated_data.get('title'),
            description=validated_data.get('description', ''),
            type=validated_data.get('type', ''),
            author_user=self.context.get('request').user
        )
        project.save()
        # Creating initial Contributor
        first_contributor = Contributor.objects.create(user=project.author_user,
                                                       project=project,
                                                       permission='RW',
                                                       role='A')
        first_contributor.save()
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

class IssueSerializer(serializers.ModelSerializer):
    """Serializer class for Issues"""

    class Meta:
        model = Issue
        fields = ['title','desc','tag','priority','project','status','created_time']



