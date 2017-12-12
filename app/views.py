from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
from . import permissions

class UserProfileViewSet(viewsets.ModelViewSet):
    """handles creating reading and updating model items"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)     #BELOW
    permission_classes = (permissions.UpdateOwnProfile,)    #BELOW


    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class LoginViewSet(viewsets.ViewSet):
    """checks email and password and returns an authtoken"""

    serializer_class = AuthTokenSerializer

    def create(self,request):
        """Use the ObtainAuthToken APIView to validate and create a token"""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating reading and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus,IsAuthenticatedOrReadOnly,)

    def perform_create(self,serializer):
        """sets the user profile to the logged in user"""

        serializer.save(user_profile = self.request.user)






    #querysets tells the viewset how to retrieve data from the database
    #authentication_classes adds TokenAuthentication as a tuple
    #permission_classes adds permissions

    #BELOW
    ## ENDING WITH A COMMA INSTRUCTS DJANGO TO CREATE AS TUPLE(immutable)
    ##filter_backends AND search_fields ALLOWS USE TO USE THE search filter backend TO FILTER BY name and email
