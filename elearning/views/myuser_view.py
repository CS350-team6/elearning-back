# # Standard Library imports
# import json

# # Core Django imports


# # Third-party imports
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.views import TokenObtainPairView


# # App imports
# from ..services import user_service
# from ..django_customizations.drf_customizations import AccountCreation
# from ..django_customizations.drf_jwt_customizations import CustomTokenObtainPairSerializer

# class User(APIView):
#     permission_classes = (AccountCreation,)
#     def post(self, request):
#         username = request.data.get("username", "")
#         email_address = request.data.get("email_address", "")
#         password = request.data.get("password", "")

#         try:
#             user_model, auth_token = user_service.create_user_account(
#                 username,
#                 email_address,
#                 password,
#             )
#         except:
#             return Response(data=json.dumps({'result': 'fail'}), status=400)
        
#         resp = { "data": { "auth_token": auth_token } }
#         return Response(data=resp, status=201)

#     def get(self, request):
#         user_profile_dict = user_service.get_user_profile_from_user_model(request.user)
        
#         resp = { "data": { "user_profile": user_profile_dict }}
#         return Response(data=resp, status=200)
    
#     def login(self, request):
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")

#         try:
#             user_model, auth_token = user_service.login(
#                 username,
#                 password,
#             )
#         except:
#             return Response(data=json.dumps({'result': 'fail'}), status=400)
        
#         resp = { "data": { "auth_token": auth_token } }
#         return Response(data=resp, status=201)
    
#     def logout(self, request):
#         try:
#             user_service.logout(request.user)
#         except:
#             return Response(data=json.dumps({'result': 'fail'}), status=400)
        
#         resp = { "data": { "result": "success" } }
#         return Response(data=resp, status=201)

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
