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
                    if instance.referral_id.referral_id:
                        root = instance.referral_id.referral_id
                        while(root is not None):
                            if root.is_ambassador:
                                root.payback += 10
                                root.save()
                            root = root.referral_id
            else:
                raise Exception(serializer.errors)
            return Response(serializer.data, status=status.HTTP_200_OK)
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
                    if instance.referral_id.referral_id:
                        root = instance.referral_id.referral_id
                        while(root is not None):
                            if root.is_ambassador:
                                root.payback += 10
                                root.save()
                            root = root.referral_id
            else:
                raise Exception(serializer.errors)
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class AmbassadorView(APIView):
    queryset = Customer.objects.filter(is_ambassador=True)
    lookup_field = 'customer_id'
    serializer_class = CustomerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('customer_id',)

    def get(self, request, customer_id, level=0):
        level_order_children = {}
        children_list = []
        try:
            root = Customer.objects.filter(customer_id=customer_id)
            i = 0
            while(True):
                children = Customer.objects.filter(referral_id__in=root)
                if (len(children) > 0):
                    level_order_children[i] = [child.customer_id for child in children]
                    root = Customer.objects.filter(customer_id__in=level_order_children[i])
                    i = i+1
                else:
                    break
            if level:
                if level_order_children.has_key(int(level)-1):
                    children_list = list(
                        set(level_order_children.get(int(level)-1)))
                else:
                    return Response("The Ambassador {0} doesn't have any child at level {1}".format(customer_id, level),
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                for level in level_order_children.values():
                    children_list = children_list + level
                children_list = list(set(children_list))
            data = Customer.objects.filter(customer_id__in=children_list)
            serializer = self.serializer_class(data, many=True)
            return Response(serializer.data)
        except Exception, e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
