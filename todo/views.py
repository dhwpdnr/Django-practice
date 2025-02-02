from rest_framework import generics
from rest_framework.response import Response
from .serializers import TaskSerializer, CommentSerializer
from .models import Task, Comment


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.prefetch_related("comments").all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # prefetch_related cache 삭제
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
