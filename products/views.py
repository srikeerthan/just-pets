from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.
@permission_classes((IsAuthenticated,))
class ProductsView(ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()

        # Applying pagination on products data
        paginator = Paginator(products, 40)
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        product_serializer = ProductSerializer(products, many=True)

        return Response(data=product_serializer.data, status=status.HTTP_200_OK)

    @permission_classes((IsAdminUser,))
    def post(self, request, *args, **kwargs):
        product_data = {
            "title": request.data.get('title'),
            "brand": request.data.get("brand"),
            "selling_price": request.data.get("selling_price"),
            "offering_price": request.data.get("offering_price"),
            "description": request.data.get("description"),
            "image": request.data.get("image")
        }
        product = Product.objects.create(**product_data)
        product.save()
        data = {
            "success": True,
            "message": "Product created Successfully"
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
