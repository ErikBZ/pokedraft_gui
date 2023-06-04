from rest_framework import viewsets
from .serializers import PokemonDraftListSerializer
from .models import PokemonDraftList

class PokmeonDraftListViewSet(viewsets.ModelViewSet):
    queryset = PokemonDraftList.objects.all()
    serializer_class = PokemonDraftListSerializer

