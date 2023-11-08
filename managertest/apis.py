from rest_framework import generics
from .serializers import PersonSerializer
from .models import Person


class PersonActiveAPI(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.active_people.all()
