import datetime

from django.http import Http404

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Task
from main.serializers import TaskSerializer


def get_author_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        author_ip = x_forwarded_for.split(',')[0]
    else:
        author_ip = request.META.get('REMOTE_ADDR')
    return author_ip


class TaskList(APIView):
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