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
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if serializer.validated_data['done']:
                    obj = serializer.save()
                    obj.author_ip = get_author_ip(request)
                    obj.save()
                    response = {"task_id": obj.id}
                    return Response(response, status=status.HTTP_201_CREATED)
            except KeyError:
                Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskView(APIView):

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        book = self.get_object(id)
        serializer = TaskSerializer(book, context={"request": request})
        return Response(serializer.data)
