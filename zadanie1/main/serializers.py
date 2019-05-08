from rest_framework import serializers

from main.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    done_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ("id", "title", "done", "author_ip", "done_date", 'created_date')
        read_only_fields = ("id", "author_ip", 'created_date')

        extra_kwargs = {
            'id': {'read_only': True},
            'author_ip': {'read_only': True},
            'created_date': {'read_only': True},
        }