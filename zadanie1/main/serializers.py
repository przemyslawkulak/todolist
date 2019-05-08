from rest_framework import serializers

from main.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    done_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ("id", "title", "done", "author_ip", "done_date", 'created_date')

    # def create(self, validated_data):
    #     the_task = Task.objects.create(
    #         title=validated_data['title'],
    #         done=validated_data['done'],
    #         done_date=validated_data['done_date']
    #     )
    #     return the_task
