from rest_framework.views import APIView
from rest_framework.response import Response
from .scraper import MPLIDStandingsScraper, MPLIDTeamScraper, MPLIDTeamDetailScraper, MPLIDTransferScraper, MPLIDStatsScraper
from .serializers import MPLIDStandingSerializer, MPLTeamIDSerializer, MPLIDTeamDetailSerializer, MPLIDTransferSerializer, MPLIDTeamStatSerializer, MPLIDPlayerStatsSerializer
from rest_framework import status

class MPLIDStandingsAPIView(APIView):
    def get(self, request):
        scraper = MPLIDStandingsScraper()
        data = scraper.get_standings()
        serializer = MPLIDStandingSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDTeamAPIView(APIView):
    def get(self, request):
        scraper = MPLIDTeamScraper()
        data = scraper.get_teams()
        serializer = MPLTeamIDSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDTeamDetailAPIView(APIView):
    def get(self, request, team_id):
        scraper = MPLIDTeamDetailScraper(team_id)
        data = scraper.get_team_details()
        serializer = MPLIDTeamDetailSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MPLIDTransferAPIView(APIView):
    def get(self, request):
        scraper = MPLIDTransferScraper()
        data = scraper.get_transfers()
        serializer = MPLIDTransferSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDStatsAPIView(APIView):
    def get(self, request):
        scraper = MPLIDStatsScraper()
        data = scraper.parse_team_stats(scraper.fetch_html())
        serializer = MPLIDTeamStatSerializer(data, many=True)
        return Response(serializer.data)

class MPLIDPlayerStatsAPIView(APIView):
    def get(self, request):
        scraper = MPLIDStatsScraper()
        data = scraper.parse_player_stats(scraper.fetch_html())
        serializer = MPLIDPlayerStatsSerializer(data, many=True)
        return Response(serializer.data)