from django.shortcuts import render
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from todolist.models import TodoItem
from todolist.serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class TodoItemview(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,format=None):
        todos = TodoItem.objects.filter(author=request.user)
        serializer =TodoItemSerializer(todos,many=True)
        return Response(serializer.data)
