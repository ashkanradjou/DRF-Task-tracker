from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .permissions import IsOwner
from .serializers import RegisterSerializer, TaskSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'id': user.id, 'username': user.username},
            status=status.HTTP_201_CREATED,
        )


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response(
            {'token': token.key, 'user_id': token.user_id, 'username': token.user.username}
        )


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)

        is_done_param = self.request.query_params.get('is_done')
        if is_done_param is not None:
            normalized = is_done_param.lower()
            if normalized in ['true', '1', 'yes']:
                queryset = queryset.filter(is_done=True)
            elif normalized in ['false', '0', 'no']:
                queryset = queryset.filter(is_done=False)

        priority_param = self.request.query_params.get('priority')
        if priority_param is not None:
            try:
                priority_value = int(priority_param)
                if priority_value in [Task.LOW, Task.MEDIUM, Task.HIGH]:
                    queryset = queryset.filter(priority=priority_value)
            except ValueError:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
