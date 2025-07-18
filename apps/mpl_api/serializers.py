from rest_framework import serializers

class MPLStandingSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    team_name = serializers.CharField()
    team_logo = serializers.URLField()
    match_point = serializers.IntegerField()
    match_wl = serializers.CharField()
    net_game_win = serializers.IntegerField()
    game_wl = serializers.CharField()