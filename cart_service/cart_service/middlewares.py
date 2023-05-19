# from django.http import JsonResponse
# from django.contrib.auth import authenticate
# from django.conf import settings
# import requests
#
#
# class UserAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if not request.user.is_authenticated:
#             token = request.headers.get('Authorization')
#             print(token)
#             headers = {
#                 'Authorization': token,
#                 'Content-Type': 'application/json'
#             }
#             response = authenticate(request=requests.get("http://127.0.0.1:8000/api/authenticate", headers=headers))
#             print(response)
#             if response is None:
#                 return JsonResponse({'error': 'Authentication failed'}, status=401)
#
#         response = self.get_response(request)
#         return response
