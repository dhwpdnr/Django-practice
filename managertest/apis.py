from rest_framework import generics
from .serializers import PersonSerializer
from .models import Person


class PersonActiveAPI(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.active_people

    def get_queryset(self):
        queryset = self.queryset
        target = self.request.query_params.get("target", "")
        if target == "author":
            queryset = queryset.author()
        elif target == "editor":
            queryset = queryset.editor()
        return queryset


class PersonAPI(generics.ListAPIView):
    serializer_class = PersonSerializer
    def get_queryset(self):
        target = self.request.query_params.get("target", "")
        if target == "author":
            queryset = Person.people.author()
        elif target == "editor":
            queryset = Person.people.editor()
        else:
            queryset = Person.objects.all()
        return queryset
