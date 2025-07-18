from rest_framework.views import APIView
from rest_framework.response import Response
from .scraper import MPLStandingsIDScraper
from .serializers import MPLStandingIDSerializer

class MPLStandingsIdAPIView(APIView):
    def get(self, request):
        scraper = MPLStandingsIDScraper()
        data = scraper.get_standings()
        serializer = MPLStandingIDSerializer(data, many=True)
        return Response(serializer.data)