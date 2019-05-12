import datetime

from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Task
from main.serializers import TaskSerializer


def get_author_ip(request):
    """
    function to autofill author's address IP
    :param request:
    :return: author's IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        author_ip = x_forwarded_for.split(',')[0]
    else:
        author_ip = request.META.get('REMOTE_ADDR')
    return author_ip


class TaskList(APIView):
    """
    '/todolist/'
    Method Get - List of all Tasks:
    Method Post - Creating new Task, return JSON {"task_id": <task_id>}
    - field "title" is necessary
    - fields "done" and "done_date" are optional

    if field "done" is empty task is set as "False"
    if fields "done" and "done_date" are not empty set as is specify
    if field "done" is "True" and "done_date" is empty, current time is used as "done_date"
    if field "done" is "False" and "done_date" is not empty, return HTTP 400
    """
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            if 'done' in serializer.validated_data.keys() and serializer.validated_data['done']:
                if 'done_date' in serializer.validated_data.keys() and serializer.validated_data['done_date']:
                    obj = serializer.save()
                    obj.author_ip = get_author_ip(request)
                    obj.save()
                    return Response({"task_id": obj.id}, status=status.HTTP_201_CREATED)
                else:
                    obj = serializer.save()
                    obj.done_date = datetime.datetime.now()
                    obj.author_ip = get_author_ip(request)
                    obj.save()
                    return Response({"task_id": obj.id}, status=status.HTTP_201_CREATED)
            else:
                if 'done_date' in serializer.validated_data.keys() and serializer.validated_data['done_date']:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = serializer.save()
                    obj.author_ip = get_author_ip(request)
                    obj.save()
                    return Response({"task_id": obj.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):
    """
    ​'/todolist/<task_id>/'
    if ID doesn't exist return HTTP 404
    Method Get - details of Task with <task_id>
    Method Delete - deleting Task with <task_id> - return HTTP 204
    Method Patch - partial update of Task with <task_id>:
    - Only fields: ​ 'title'​, 'done', 'done_date' can be changed

    - if field 'done' is 'true'and field 'done_date' is empty, current time is used as "done_date"
    - if field "done" is "False" and "done_date" is not empty, return HTTP 400
    - if field 'done' is 'false' and "done_date" is empty, 'done_date' is erasing
    - if field "done" is "True" and "done_date" is not empty, set values
    """

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, id):
        task = self.get_object(id)
        serializer = TaskSerializer(task, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, id):
        task = self.get_object(id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        task = self.get_object(id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            if 'done' in serializer.validated_data.keys() and serializer.validated_data['done']:
                if 'done_date' in serializer.validated_data.keys() and serializer.validated_data['done_date']:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    obj = serializer.save()
                    obj.done_date = datetime.datetime.now()
                    obj.save()
                    return Response(obj)
            elif 'done' in serializer.validated_data.keys() and serializer.validated_data['done'] is False:
                if 'done_date' in serializer.validated_data.keys() and serializer.validated_data['done_date']:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    obj = serializer.save()
                    obj.done_date = None
                    obj.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serializer.save()
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)