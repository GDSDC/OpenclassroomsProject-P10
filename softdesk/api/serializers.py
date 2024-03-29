from rest_framework import serializers

from core.comments.models import Comment
from core.contributors.models import Contributor
from core.issues.models import Issue
from core.projects.models import Project
from core.users.models import User


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
                                                       role='AUTHOR')
        first_contributor.save()
        return project

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer class for contributors"""

    user_email = serializers.CharField(read_only=True, source='user.email')

    class Meta:
        model = Contributor
        fields = ['user_email', 'role_name']


class IssueSerializer(serializers.ModelSerializer):
    """Serializer class for Issues"""

    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'status', 'assignee_user']

    def validate(self, attrs):
        # check for assignee_user in contributors of the project
        if attrs["assignee_user"] not in [contributor.user for contributor in
                                          Contributor.objects.filter(project_id=self.context.get("project_id"))]:
            raise serializers.ValidationError({"assignee_user": "assignee_user not contributor of project."})
        # check if title is not already used for another issue of the project
        if attrs["title"] in [issue.title for issue in
                                          Issue.objects.filter(project_id=self.context.get("project_id"))]:
            raise serializers.ValidationError(
                {"title": "title already used for this project. please chose a different title."})
        return attrs

    def create(self, validated_data):
        # Creating Issue
        issue = Issue.objects.create(
            title=validated_data.get('title'),
            desc=validated_data.get('desc', ''),
            tag=validated_data.get('tag'),
            priority=validated_data.get('priority'),
            project=Project.objects.get(id=self.context.get('project_id')),
            status=validated_data.get('status'),
            author_user=self.context.get('request').user,
            assignee_user=User.objects.get(id=validated_data.get('assignee_user').id),
        )
        issue.save()
        return issue

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.assignee_user = validated_data.get('assignee_user', instance.assignee_user)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    """Serializer class for Comments"""

    class Meta:
        model = Comment
        fields = ['description']

    def create(self, validated_data):
        # Creating Comment
        comment = Comment.objects.create(
            description=validated_data.get('description'),
            author_user=self.context.get('request').user,
            issue=Issue.objects.get(id=self.context.get('issue_id')),
        )
        comment.save()
        return comment

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
