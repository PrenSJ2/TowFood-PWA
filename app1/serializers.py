from app1.models import Product
from rest_framework import serializers
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # queryset = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["url","id", "brand", "name", "barcode","category","allergens", "weight", "quantity", "footprint","perishable"]

    # def get_queryset(self, obj):
    #     barcode = self.context['request'].query_params.get('barcode', None)
    #     print("get_queryset", barcode)
    #     if barcode:
    #         queryset = obj.filter(barcode=barcode)
    #     return ProductSerializer(queryset, many=True).data