from rest_framework.views import APIView
from rest_framework.response import Response
from .scraper import MPLStandingsIDScraper, MPLTeamIDScraper
from .serializers import MPLStandingIDSerializer, MPLTeamIDSerializer

class MPLStandingsIdAPIView(APIView):
    def get(self, request):
        scraper = MPLStandingsIDScraper()
        data = scraper.get_standings()
        serializer = MPLStandingIDSerializer(data, many=True)
        return Response(serializer.data)


class MPLTeamIdAPIView(APIView):
    def get(self, request):
        scraper = MPLTeamIDScraper()
        data = scraper.get_teams()
        serializer = MPLTeamIDSerializer(data, many=True)
        return Response(serializer.data)