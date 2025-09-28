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

class MPLIDTransferSerializer(serializers.Serializer):
    transfer_date = serializers.CharField(allow_null=True)
    player_name = serializers.CharField(allow_null=True)
    player_role = serializers.CharField(allow_null=True)
    from_team_name = serializers.CharField(allow_null=True)
    from_team_logo = serializers.URLField(allow_null=True)
    to_team_name = serializers.CharField(allow_null=True)
    to_team_logo = serializers.URLField(allow_null=True)

class MPLIDTeamStatSerializer(serializers.Serializer):
    team_name = serializers.CharField(allow_null=True)
    team_logo = serializers.URLField(allow_null=True)
    kills = serializers.IntegerField()
    deaths = serializers.IntegerField()
    assists = serializers.IntegerField()
    gold = serializers.IntegerField()
    damage = serializers.IntegerField()
    lord = serializers.IntegerField()
    tortoise = serializers.IntegerField()
    tower = serializers.IntegerField()

class MPLIDPlayerStatsSerializer(serializers.Serializer):
    player_name = serializers.CharField(allow_null=True)
    player_logo = serializers.URLField(allow_null=True)
    lane = serializers.CharField(allow_null=True)
    total_games = serializers.IntegerField()
    total_kills = serializers.IntegerField()
    avg_kills = serializers.FloatField()
    total_deaths = serializers.IntegerField()
    avg_deaths = serializers.FloatField()
    total_assists = serializers.IntegerField()
    avg_assists = serializers.FloatField()
    avg_kda = serializers.FloatField()
    kill_participation = serializers.CharField(allow_null=True)

class MPLIDHeroStatsSerializer(serializers.Serializer):
    hero_name = serializers.CharField(allow_null=True)
    hero_logo = serializers.URLField(allow_null=True)
    pick = serializers.IntegerField()
    ban = serializers.IntegerField()
    win = serializers.IntegerField()
    win_rate = serializers.FloatField()
    
class MPLIDHeroPoolHeroSerializer(serializers.Serializer):
    hero_logo = serializers.URLField(allow_null=True)
    pick = serializers.IntegerField()
    pick_rate = serializers.FloatField()

class MPLIDHeroPoolsSerializer(serializers.Serializer):
    player_name = serializers.CharField(allow_null=True)
    team_logo = serializers.URLField(allow_null=True)
    lane = serializers.CharField(allow_null=True)
    total_heroes = serializers.IntegerField()
    hero_pool = MPLIDHeroPoolHeroSerializer(many=True)
    
class MPLIDPlayerPoolPlayerSerializer(serializers.Serializer):
    player_logo = serializers.URLField(allow_null=True)
    player_info = serializers.CharField(allow_null=True)
    pick = serializers.IntegerField()
    pick_rate = serializers.FloatField()

class MPLIDPlayerPoolsSerializer(serializers.Serializer):
    hero_name = serializers.CharField(allow_null=True)
    hero_logo = serializers.URLField(allow_null=True)
    total = serializers.IntegerField()
    players = MPLIDPlayerPoolPlayerSerializer(many=True)
    
class MPLIDStandingsMVPSerializer(serializers.Serializer):
    rank = serializers.IntegerField(allow_null=True)
    player_name = serializers.CharField(allow_null=True)
    player_logo = serializers.URLField(allow_null=True)
    team_logo = serializers.URLField(allow_null=True)
    point = serializers.IntegerField(allow_null=True)


class MPLIDScheduleTeamSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    logo = serializers.URLField(allow_null=True)
    score = serializers.IntegerField(allow_null=True)


class MPLIDScheduleMatchSerializer(serializers.Serializer):
    match_id = serializers.IntegerField(allow_null=True)
    match_time = serializers.CharField(allow_null=True)
    team1 = MPLIDScheduleTeamSerializer()
    team2 = MPLIDScheduleTeamSerializer()
    replay_link = serializers.URLField(allow_null=True)
    status = serializers.CharField(allow_null=True)


class MPLIDScheduleDateGroupSerializer(serializers.Serializer):
    match_date = serializers.CharField(allow_null=True)
    matches = MPLIDScheduleMatchSerializer(many=True)


class MPLIDScheduleWeekSerializer(serializers.Serializer):
    week = serializers.IntegerField()
    matches = MPLIDScheduleDateGroupSerializer(many=True)


class MPLIDScheduleAllSerializer(serializers.Serializer):
    """Serializer for all weeks schedule data"""
    def to_representation(self, instance):
        # instance is a dict with week_1, week_2, etc. keys
        return instance
