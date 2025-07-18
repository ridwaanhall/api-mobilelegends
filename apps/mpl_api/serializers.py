from rest_framework import serializers

class MPLIDStandingSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    team_name = serializers.CharField()
    team_logo = serializers.URLField()
    match_point = serializers.IntegerField()
    match_wl = serializers.CharField()
    net_game_win = serializers.IntegerField()
    game_wl = serializers.CharField()
    
class MPLTeamIDSerializer(serializers.Serializer):
    team_url = serializers.URLField()
    team_logo = serializers.URLField()
    team_name = serializers.CharField()

class MPLIDTeamPlayerSerializer(serializers.Serializer):
    player_image = serializers.URLField(allow_null=True)
    player_name = serializers.CharField(allow_null=True)
    player_role = serializers.CharField(allow_null=True)

class MPLIDTeamSocialMediaSerializer(serializers.Serializer):
    facebook = serializers.URLField(required=False, allow_null=True)
    instagram = serializers.URLField(required=False, allow_null=True)
    youtube = serializers.URLField(required=False, allow_null=True)

class MPLIDTeamDetailSerializer(serializers.Serializer):
    team_logo = serializers.URLField(allow_null=True)
    team_name = serializers.CharField(allow_null=True)
    social_media = MPLIDTeamSocialMediaSerializer()
    roster = MPLIDTeamPlayerSerializer(many=True)