import json
from django.http import JsonResponse

class CustomResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if not response.get('error'):
                data = response.content.decode('utf-8')
                json_data = json.loads(data)
                json_data['error'] = ''
                response.content = json.dumps(json_data)
            return response
        except Exception as e:
            return JsonResponse({'error': '内部错误'}, status=500)