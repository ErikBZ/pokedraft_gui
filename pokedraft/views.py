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
        try:
            session = DraftSession.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Page Not Found"}, 404)

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

        if not session.accepting_players:
            return JsonResponse(message("Draft Session is no longer accepting players"), status=403)

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
        try:
            session = DraftSession.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Page Not Found"}, 404)

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
        if action != DraftPhase.BAN and action != DraftPhase.PICK:
            return JsonResponse(message("Action is not allowed"), status=422)
        if action != session.current_phase:
            return JsonResponse(message(f"Current action phase is {session.current_phase}"), status=422)
        if selected_pokemon in session.banned_pokemon.all():
            return JsonResponse(message("Pokemon can no longer be selected, please choose another"), status=201)
        if len(user.pokemon_selected.all()) >= session.draft_rules.max_pokemon:
            return JsonResponse(message("Maximum pokemon selected. Can no longer selecte more."), status=201)

        if session.current_phase == DraftPhase.PICK:
            user.pokemon_selected.add(pokemon_id)

        session.banned_pokemon.add(pokemon_id)

        rules = session.draft_rules
        session.current_player = self.get_next_player(session, user_pk)
        session.current_phase = self.get_next_phase(session.turn_ticker,
                                    session.draftuser_set,
                                    rules.phase_start,
                                    rules.bans_per_round,
                                    rules.picks_per_round)

        if session.accepting_players:
            session.accepting_players = False

        session.save()
        return JsonResponse({
            "selected_pokemon": [x.id for x in user.pokemon_selected.all()],
            "banned_pokemon": [x.id for x in session.banned_pokemon.all()],
            "phase": session.current_phase
        }, status=201)
    
    def get_next_player(self, draft_session, current_user_id):
        player_ids = [x.id for x in draft_session.draftuser_set.all().order_by('order_in_session')]
        i = player_ids.index(current_user_id)
        draft_session.turn_ticker += 1

        if draft_session.draft_rules.turn_type == DraftRules.TurnType.ROUND_ROBIN:
            i = (i+1) % len(player_ids)
        elif draft_session.draft_rules.turn_type == DraftRules.TurnType.SNAKE:
            ds_round = draft_session.turn_ticker // len(player_ids)
            i = i + 1 if ds_round % 2 == 0 else i - 1

        return player_ids[i]

    def get_next_phase(self, turns, players, starting_phase, bans_per_round, picks_per_round):
        num_of_players = len(players.all())
        full_round = bans_per_round + picks_per_round
        rounds = turns // num_of_players

        # this could probably look nicer
        if starting_phase == DraftPhase.BAN:
            curr_round = (rounds % full_round) - bans_per_round
            if curr_round < 0:
                return DraftPhase.BAN
            else:
                return DraftPhase.PICK
        elif starting_phase == DraftPhase.PICK:
            curr_round = (rounds & full_round) - picks_per_round
            if curr_round < 0:
                return DraftPhase.PICK
            else:
                return DraftPhase.BAN

    @action(methods=["get"], detail=True, url_path="update", url_name="update")
    def session_update(self, request, pk=None):
        data = {}
        try:
            session = DraftSession.objects.get(pk=pk)
        except:
            return JsonResponse({"message": "Page Not Found"}, status=404)

        data['current_phase'] = session.current_phase
        data['banned_pokemon'] = [x.id for x in session.banned_pokemon.all()]
        data['current_player'] = session.draftuser_set.get(pk=session.current_player).name

        players = session.draftuser_set.all()
        player_map = []
        for p in players:
            player_map.append({
                "name": p.name,
                "pokemon": [{"name": x.name, "type1": x.type1, "type2": x.type2, "id": x.id} for x in p.pokemon_selected.all()]
            })

        data['players'] = player_map

        return JsonResponse(data, status=200)

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
