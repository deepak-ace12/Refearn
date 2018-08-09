from rest_framework import serializers
from refearn.models import Customer
from django.db.models import Count

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerRefferalListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.annotate(number_of_children=Count('referral_id')).order_by('-number_of_children')
        return super(CustomerRefferalListSerializer, self).to_representation(data)


class CustomerRefferalSerializer(serializers.ModelSerializer):
    number_of_children = serializers.SerializerMethodField()

    def get_number_of_children(self, obj):
        referrals = Customer.objects.filter(referral_id=obj)
        if referrals.exists():
            return len(referrals)
        return 0
    
    class Meta:
        model = Customer
        list_serializer_class = CustomerRefferalListSerializer
        fields = '__all__'
