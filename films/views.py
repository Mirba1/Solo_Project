from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .serializer import *
from .models import *
from django_filters import rest_framework as filters
from .permissions import *
from django_filters import rest_framework as rest_filters



class FilmFilter(filters.FilterSet):
    class Meta:
        model = Film
        fields = ('genre', )


from rest_framework import filters


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    filter_backends = [rest_filters.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    filterset_class = FilmFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'likes']:
            return [IsAdminUser()]
        return []


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'like']:
            return [IsAuthorOrIsAdmin()]
        elif self.action in ['like']:
            return [IsAuthenticated()]
        return []

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        comment = self.get_object()
        user = request.user
        like_obj, created = Like.objects.get_or_create(comment=comment, user=user)
        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('disliked')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('liked')


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthorOrIsAdmin]





class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthorOrIsAdmin, IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer