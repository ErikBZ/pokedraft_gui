from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from .serializers import *
from .models import *
import json
import uuid

class PokmeonDraftListViewSet(viewsets.ModelViewSet):
    queryset = PokemonDraftSet.objects.all()
    serializer_class = PokemonDraftSetSerializer

class PokmeonDraftListSimple(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PokemonDraftSet.objects.all()
    serializer_class = PokemonDraftSetSimpleSerializer


class PokemonListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

class DraftSessionView(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    queryset = DraftSession.objects.all()
    serializer_class = DraftSessionSerializer

    @action(methods=["post"], detail=True, url_path="create-user",
            url_name="create_user")
    def create_user(self, request, pk=None):
        session = self.get_session(pk)
        if session == None:
            return HttpResponse("Session does not exist", status=404)

        if "name" not in request.data:
            return HttpResponse("Name missing in post data", status=422)

        new_user = DraftUser(name=request.data["name"], current_turn=False,
                             session_id=session, key=str(uuid.uuid4()))
        new_user.save()
        if session.starting_player == None or session.starting_player == "":
            session.starting_player = new_user.pk
        else:
            tail = self.get_tail_player(session.starting_player)
            tail.next = new_user.pk
            new_user.prev = tail.pk

        return_data = json.dumps(
            {
                "name": request.data["name"],
                "session_id": pk,
                "user_id": new_user.pk,
                "key": new_user.key
            }
        )
        return HttpResponse(return_data, 201)
    
    def get_tail_player(self, starting_player):
        try:
            current_player = Pokemon.objects.get(starting_player)
            while current_player.next != None or current_player.next != "":
                current_player = Pokemon.objects.get(current_player.next)
            return current_player
        except:
            return None

    
    @action(methods=["post"], detail=True, url_path="select-pokemon",
            url_name="select_pokemon")
    def select_pokemon(self, request, pk=None):
        session = self.get_session(pk)
        if session == None:
            return HttpResponse("Session does not exist", status=404)

        user_pk = request.data["user_id"]
        pokemon_id = request.data["pokemon_id"]
        action = request.data["action"]
        secret = request.data["secret"]
        user = None
        selected_pokemon = None
        try:
            user = session.draftuser_set.get(pk=user_pk)
        except:
            return HttpResponse("Draft User does not exist", status=404)

        try:
            selected_pokemon = session.draft_used.pokemon_list.get(pk=pokemon_id)
        except:
            return HttpResponse("Selected Pokemon is not in the draft", status=404)

        if len(session.draftuser_set.all()) < session.min_player:
            return HttpResponse("Not enough players yet", 422)
        if not user.current_turn:
            return HttpResponse("It is not your turn", 422)
        if not secret or secret != user.key:
            return HttpResponse("Secret does not match", 401)
        if "select" not in action or "ban" not in action:
            return HttpResponse("Action is not allowed", 422)
        if action != session.current_phase:
            return HttpResponse(f"Current action phase is {session.current_phase}", 422)
        if selected_pokemon in session.banned_pokemon:
            return HttpResponse("Pokemon can no longer be selected, please choose another", 200)

        user.pokemon_selected.add(selected_pokemon)
        session.banned_pokemon.add(selected_pokemon)

        # change next player here

        # check if draft has ended
    
    def get_session(pk):
        try:
            return DraftSession.objects.get(pk=pk)
        except:
            return None
            

class DraftUserView(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):
    queryset = DraftUser.objects.all()
    serializer_class = DraftUserSerializer
