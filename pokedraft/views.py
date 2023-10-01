from django.http import JsonResponse, JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from .serializers import *
from .models import *
import uuid

def message(msg):
    return {"message": msg}

class PokmeonDraftListViewSet(viewsets.ModelViewSet):
    queryset = PokemonDraftSet.objects.all()
    serializer_class = PokemonDraftSetSerializer

class PokmeonDraftListSimple(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = PokemonDraftSet.objects.all()
    serializer_class = PokemonDraftSetSimpleSerializer


class PokemonListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

class DraftRuleListViewSet(viewsets.ModelViewSet):
    queryset = DraftRules.objects.all()
    serializer_class = DraftRulesSerializer

class DraftSessionView(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    queryset = DraftSession.objects.all()
    serializer_class = DraftSessionSerializer

    @action(methods=["post"], detail=True, url_path="create-user",
            url_name="create_user")
    def create_user(self, request, pk=None):
        session = self.get_session(pk)
        players = session.draftuser_set.all()
        player_names = [x.name for x in players]

        if session == None:
            return JsonResponse({"message": "Session does not exist"}, status=404)

        if "name" not in request.data or request.data["name"] == "":
            return JsonResponse({"message": "Name missing in post data"}, status=422)

        if request.data["name"] in player_names:
            return JsonResponse({"message": "Name already used"}, status=401)

        if len(players) >= session.max_num_players:
            return JsonResponse(message("Max number of player reached."), status=403)

        new_user = DraftUser(name=request.data["name"], session=session, key=str(uuid.uuid4()),
                             order_in_session=len(players)+1)
        new_user.save()
        players = session.draftuser_set.all()

        if len(players) == 1:
            session.current_player = new_user.id
            session.save()

        return_data = {
                "name": request.data["name"],
                "session_id": pk,
                "user_id": new_user.pk,
                "current_turn": new_user.is_current_turn(),
                "key": new_user.key
            }

        return JsonResponse(return_data, status=201)
    
    @action(methods=["post"], detail=True, url_path="select-pokemon",
            url_name="select_pokemon")
    def select_pokemon(self, request, pk=None):
        session = self.get_session(pk)
        if session == None:
            return JsonResponse(message("Session does not exist"), status=404)

        user_pk = request.data["user_id"]
        pokemon_id = request.data["pokemon_id"]
        action = request.data["action"]
        secret = request.data["secret"]
        user = None
        selected_pokemon = None
        try:
            user = session.draftuser_set.get(pk=user_pk)
        except:
            return JsonResponse(message("Draft User does not exist"), status=404)

        try:
            selected_pokemon = session.draft_set.pokemon_list.get(pk=pokemon_id)
        except:
            return JsonResponse(message("Selected Pokemon is not in the draft"), status=404)

        if not secret or secret != user.key:
            return JsonResponse(message("Access Denied"), status=401)
        if len(session.draftuser_set.all()) < session.min_num_players:
            return JsonResponse(message("Not enough players yet"), status=422)
        if session.current_player != str(user.id):
            return JsonResponse(message("It is not your turn"), status=422)
        if action != DraftSession.DraftPhase.BAN or action != DraftSession.DraftPhase.PICK:
            return JsonResponse(message("Action is not allowed"), status=422)
        if action != session.current_phase:
            return JsonResponse(message(f"Current action phase is {session.current_phase}"), status=422)
        if selected_pokemon in session.banned_pokemon:
            return JsonResponse(message("Pokemon can no longer be selected, please choose another"), status=201)

        user.pokemon_selected.add(selected_pokemon)
        session.banned_pokemon.add(selected_pokemon)

        # change next player here

        # check if draft has ended
        return JsonResponse({
            "selected_pokemon": user.pokemon_selected
        }, status=201)
    
    def get_session(self, pk):
        try:
            return DraftSession.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Page Not Found"}, 404)

    def get_players(self, pk):
        session = None
        try:
            session = DraftSession.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Page Not Found"}, 404)

        players = session.draftuser_set
        payload = [x.to_json() for x in players]

        return JsonResponse(payload, 200)

    def get_player(self, pk):
        session = None
        user_id = None
        try:
            session = DraftSession.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Page Not Found"}, 404)

        players = session.draftuser_set.get(user_id)
        return JsonResponse({}, 200)

class DraftUserView(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):
    queryset = DraftUser.objects.all()
    serializer_class = DraftUserSerializer
