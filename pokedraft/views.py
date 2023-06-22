from rest_framework import viewsets
from .serializers import PokemonDraftListSerializer, PokemonSerializer, PokemonDraftListSimpleSerializer
from .models import PokemonDraftList, Pokemon

class PokmeonDraftListViewSet(viewsets.ModelViewSet):
    queryset = PokemonDraftList.objects.all()
    serializer_class = PokemonDraftListSerializer

class PokmeonDraftListSimple(viewsets.ModelViewSet):
    queryset = PokemonDraftList.objects.all()
    serializer_class = PokemonDraftListSimpleSerializer


class PokemonListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
