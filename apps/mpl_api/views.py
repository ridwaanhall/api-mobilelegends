from rest_framework.views import APIView
from rest_framework.response import Response
from .scraper import MPLStandingsScraper
from .serializers import MPLStandingSerializer

class MPLStandingsAPIView(APIView):
    def get(self, request):
        scraper = MPLStandingsScraper()
        data = scraper.get_standings()
        serializer = MPLStandingSerializer(data, many=True)
        return Response(serializer.data)