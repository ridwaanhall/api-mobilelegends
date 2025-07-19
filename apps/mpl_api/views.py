from rest_framework.views import APIView
from rest_framework.response import Response
from .scraper import MPLIDStandingsScraper, MPLIDTeamScraper, MPLIDTeamDetailScraper, MPLIDTransferScraper, MPLIDStatisticsScraper
from .serializers import MPLIDStandingSerializer, MPLTeamIDSerializer, MPLIDTeamDetailSerializer, MPLIDTransferSerializer, MPLIDStatisticsSerializer
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

class MPLIDStatisticsAPIView(APIView):
    def get(self, request):
        scraper = MPLIDStatisticsScraper()
        data = scraper.parse_team_statistics(scraper.fetch_html())
        serializer = MPLIDStatisticsSerializer(data, many=True)
        return Response(serializer.data)