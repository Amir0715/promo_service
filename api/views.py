from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import ParticipantSerializer, PrizeSerializer, PromotionFullDetailSerializer, PromotionWithoutDetailSerializer, ResultSerializer
from .models import Promotion, Result
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from random import shuffle

class PromoViewSet(viewsets.ViewSet):
    queryset = Promotion.objects.all()
    @extend_schema(
        responses={
            200: PromotionWithoutDetailSerializer
        }
    )
    def list(self, request):
        """Получение краткой информации (без информации об участниках и призах) обо всех промоакциях
        """
        serializer = PromotionWithoutDetailSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=PromotionWithoutDetailSerializer,
        responses={
            201: int,
            422: OpenApiResponse(response=dict)
        }
    )
    def create(self, request):
        """Добавление промоакции с возможностью указания названия (name), описания (description) 
        Описание – не обязательный параметр, название – обязательный
        """
        serializer = PromotionWithoutDetailSerializer(data=request.data)
        if serializer.is_valid():
            promo = serializer.save()
            return Response(promo.id, status=201)
        else:
            return Response({"detail": serializer.errors}, status=422)

    @extend_schema(
        responses={
            200: PromotionFullDetailSerializer
        }
    )
    def retrieve(self, request, pk):
        """Получение полной информации (с информацией об участниках и призах) о промоакции по идентификатору
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        serializer = PromotionFullDetailSerializer(promo)
        return Response(serializer.data)

    @extend_schema(
        request=PromotionWithoutDetailSerializer,
        responses={
            206: PromotionWithoutDetailSerializer
        }
    )
    def update(self, request, pk):
        """Редактирование промо-акции по идентификатору промо-акции
        Редактировать можно только свойства name, description
        Удалить имя таким образом нельзя, описание – можно
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        serializer = PromotionWithoutDetailSerializer(promo, data=request.data, partial=True)
        if serializer.is_valid():
            promo = serializer.save()
            return Response(status=206)
        else:
            return Response({"detail": serializer.errors}, status=422)

    def destroy(self, request, pk):
        """Удаление промоакции по идентификатору
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        promo.delete()
        return Response(status=204)

    @extend_schema(
        request=ParticipantSerializer,
        responses={
            201: int,
            422: OpenApiResponse(response=dict)
        }
    )
    @action(detail=True, methods=['post'], url_path='participant')
    def add_participant(self, request, pk):
        """Добавление участника в промоакцию по идентификатору промоакции
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save()
            print(participant)
            promo.participants.add(participant)
            return Response(participant.id, status=204)
        else:
            return Response({"detail": serializer.errors}, status=422)

    @action(detail=True, methods=['delete'], url_path='participant/(?P<participant_id>[^/.]+)')
    def remove_participant(self, request, pk, participant_id):
        """Удаление участника из промоакции по идентификаторам промоакции и участника
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        participant = get_object_or_404(promo.participants.all(), pk=participant_id)
        promo.participants.remove(participant)
        return Response(status=200)

    @extend_schema(
        request=PrizeSerializer,
        responses={
            204: int,
            422: OpenApiResponse(response=dict)
        }
    )
    @action(detail=True, methods=['post'], url_path='prize')
    def add_prize(self, request, pk):
        """Добавление приза в промоакцию по идентификатору промоакции
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        
        serializer = PrizeSerializer(data=request.data)
        if serializer.is_valid():
            prize = serializer.save()
            print(prize)
            promo.prizes.add(prize)
            return Response(prize.id, status=204)
        else:
            return Response({"detail": serializer.errors}, status=422)

    @action(detail=True, methods=['delete'], url_path='participant/(?P<prize_id>[^/.]+)')
    def remove_prize(self, request, pk, prize_id):
        """Удаление приза из промоакции по идентификаторам промоакции и приза
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        prize = get_object_or_404(promo.prizes.all(), pk=prize_id)
        promo.prizes.remove(prize)
        return Response(status=200)
    
    @action(detail=True, methods=['post'], url_path='rafle')
    def rafle(self, request, pk):
        """Проведение розыгрыша призов в промоакции по идентификатору промоакции
        """
        promo = get_object_or_404(self.queryset, pk=pk)
        prizes = promo.prizes.all()
        participants = promo.participants.all()
        if len(prizes) == len(participants):
            shuffle(prizes)
            shuffle(participants)
            results = []
            for prize, participant in zip(prizes, participants):
                result = Result.objects.create(winner=participant, prize=prize)
                results.append(result)
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data, status=201)
        else:
            return Response(status=409)