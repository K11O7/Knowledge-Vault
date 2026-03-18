from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Note
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title", "content"]

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)

        tag = self.request.query_params.get("tag")

        if tag:
            queryset = queryset.filter(tags__name=tag)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
