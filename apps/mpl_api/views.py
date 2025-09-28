from rest_framework.views import APIView
from rest_framework.response import Response
from . import scraper
from . import serializers
from rest_framework import status

class MPLIDApiListAPIView(APIView):
    def get(self, request):
        api_list = [
            {"name": "Standings", "url": request.build_absolute_uri('/api/mplid/standings/')},
            {"name": "Teams", "url": request.build_absolute_uri('/api/mplid/teams/')},
            {"name": "Team Detail", "url": request.build_absolute_uri('/api/mplid/teams/<team_id>/')},
            {"name": "Transfers", "url": request.build_absolute_uri('/api/mplid/transfers/')},
            {"name": "Team Stats", "url": request.build_absolute_uri('/api/mplid/team-stats/')},
            {"name": "Player Stats", "url": request.build_absolute_uri('/api/mplid/player-stats/')},
            {"name": "Hero Stats", "url": request.build_absolute_uri('/api/mplid/hero-stats/')},
            {"name": "Hero Pools", "url": request.build_absolute_uri('/api/mplid/hero-pools/')},
            {"name": "Player Pools", "url": request.build_absolute_uri('/api/mplid/player-pools/')},
            {"name": "Standings MVP", "url": request.build_absolute_uri('/api/mplid/standings-mvp/')},
            {"name": "Schedule (All)", "url": request.build_absolute_uri('/api/mplid/schedule/')},
            {"name": "Schedule by Week", "url": request.build_absolute_uri('/api/mplid/schedule/week/<week_number>/')},
            {"name": "All Weeks", "url": request.build_absolute_uri('/api/mplid/schedule/week/')},
        ]
        return Response(api_list, status=status.HTTP_200_OK)

class MPLIDStandingsAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStandingsScraper().get_standings()
        serializer = serializers.MPLIDStandingSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDTeamAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDTeamScraper().get_teams()
        serializer = serializers.MPLTeamIDSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDTeamDetailAPIView(APIView):
    def get(self, request, team_id):
        data = scraper.MPLIDTeamDetailScraper(team_id).get_team_details()
        serializer = serializers.MPLIDTeamDetailSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MPLIDTransferAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDTransferScraper().get_transfers()
        serializer = serializers.MPLIDTransferSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDTeamStatsAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStatsScraper().parse_team_stats(scraper.MPLIDStatsScraper().fetch_html())
        serializer = serializers.MPLIDTeamStatSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDPlayerStatsAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStatsScraper().parse_player_stats(scraper.MPLIDStatsScraper().fetch_html())
        serializer = serializers.MPLIDPlayerStatsSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDHeroStatsAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStatsScraper().parse_hero_stats(scraper.MPLIDStatsScraper().fetch_html())
        serializer = serializers.MPLIDHeroStatsSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDHeroPoolsAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStatsScraper().parse_hero_pools(scraper.MPLIDStatsScraper().fetch_html())
        serializer = serializers.MPLIDHeroPoolsSerializer(data, many=True)
        return Response(serializer.data)
    
class MPLIDPlayerPoolsAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStatsScraper().parse_player_pools(scraper.MPLIDStatsScraper().fetch_html())
        serializer = serializers.MPLIDPlayerPoolsSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDStandingsMVPAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDStatsScraper().parse_mvp_standings(scraper.MPLIDStatsScraper().fetch_html())
        serializer = serializers.MPLIDStandingsMVPSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDScheduleAPIView(APIView):
    def get(self, request):
        data = scraper.MPLIDScheduleScraper().parse_schedule(scraper.MPLIDScheduleScraper().fetch_html())
        serializer = serializers.MPLIDScheduleAllSerializer(data)
        return Response(serializer.data)


class MPLIDScheduleWeekAPIView(APIView):
    def get(self, request, week_number):
        try:
            week_num = int(week_number)
            schedule_scraper = scraper.MPLIDScheduleScraper()
            html = schedule_scraper.fetch_html()
            all_data = schedule_scraper.parse_schedule(html)
            
            week_key = f"week_{week_num}"
            if week_key not in all_data:
                return Response(
                    {"error": f"Week {week_num} not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            data = all_data[week_key]
            serializer = serializers.MPLIDScheduleWeekSerializer(data)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"error": "Invalid week number"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class MPLIDScheduleAllWeeksAPIView(APIView):
    def get(self, request):
        schedule_scraper = scraper.MPLIDScheduleScraper()
        html = schedule_scraper.fetch_html()
        all_data = schedule_scraper.parse_schedule(html)
        
        # Convert dict values to list for serialization
        data = list(all_data.values())
        serializer = serializers.MPLIDScheduleWeekSerializer(data, many=True)
        return Response(serializer.data)