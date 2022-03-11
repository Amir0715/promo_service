from rest_framework import serializers
from .models import Promotion, Prize, Participant, Result

class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ('id', 'description')
        read_only = ('id', )

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name')
        read_only = ('id', )

class PromotionFullDetailSerializer(serializers.ModelSerializer):
    prizes = PrizeSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Promotion
        fields = ('id', 'name', 'description', 'prizes', 'participants')

class PromotionWithoutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('id', 'name', 'description')
        read_only = ('id', )
        optional_fields = ('description', )

class ResultSerializer(serializers.ModelSerializer):
    winner = ParticipantSerializer()
    prize = PrizeSerializer()
    
    class Meta: 
        model = Result
        fields = ('winner', 'prize')