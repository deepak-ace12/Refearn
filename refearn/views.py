from rest_framework import viewsets, status, filters, generics
from rest_framework.response import Response
from refearn.models import Customer
from refearn.serializers import CustomerSerializer, CustomerRefferalSerializer
from copy import deepcopy
from django.db.models import Count
from django.template.response import TemplateResponse
from rest_framework.views import APIView


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    lookup_field = 'customer_id'
    serializer_class = CustomerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('customer_id',)

    def create(self, request):
        print request.data
        try:
            req_data = request.data
            serializer = self.serializer_class(
                data=req_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                instance = serializer.instance
                if instance.referral_id:
                    instance.referral_id.payback += 30
                    instance.referral_id.save()
            else:
                raise Exception(serializer.errors)
            return Response(serializer.data)
        except Exception, e:
            return Response({'status': 'error', 'response': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, customer_id):
        referrer = request.query_params.get('referrer')
        try:
            req_data = request.data.copy()
            customer = Customer.objects.get(customer_id=customer_id)
            if referrer:
                req_data['referral_id'] = referrer
            old_data = deepcopy(self.serializer_class(customer).data)
            serializer = self.serializer_class(
                customer, data=req_data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                instance = serializer.instance                    
                if instance.referral_id and instance.referral_id.customer_id is not old_data.get('referral_id'):
                    if old_data.get('referral_id'):
                        old_refferal = Customer.objects.get(customer_id=old_data.get('referral_id'))
                        old_refferal.payback -= 30
                        old_refferal.save()
                    instance.referral_id.payback += 30
                    instance.referral_id.save()
            else:
                raise Exception(serializer.errors)
            return Response(serializer.data)
        except Exception, e:
            return Response({'status': 'error', 'response': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomerChildrenView(generics.ListAPIView):

    def list(self, request, customer_id):
        try:
            children = Customer.objects.filter(referral_id=customer_id)
            serializer = self.serializer_class(children, many=True)
            return Response(serializer.data)
        except Exception, e:
            return Response({"status": "error", "response": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomerReferralView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    lookup_field = 'customer_id'
    serializer_class = CustomerRefferalSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering_fields = '__all__'
    ordering = ('-number_of_children',)
    
    def list(self, request):
        try:
            serializer = self.serializer_class(self.queryset, many=True)
            return Response(serializer.data)
        except Exception, e:
            return Response({"status": "error", "response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
