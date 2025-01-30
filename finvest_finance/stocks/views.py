# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from stocks.models import Stock, StockValue
# from .serializers import StockSerializer, StockValueSerializer

# # Stock CRUD Operations
# class StockListCreateAPIView(APIView):
#     """Handles GET (list) and POST (create) operations for Stock."""
#     def get(self, request):
#         stocks = Stock.objects.all()
#         serializer = StockSerializer(stocks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = StockSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StockDetailAPIView(APIView):
#     """Handles GET, PUT, PATCH, and DELETE operations for a specific Stock."""
#     def get_object(self, pk):
#         try:
#             return Stock.objects.get(pk=pk)
#         except Stock.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         stock = self.get_object(pk)
#         if stock is None:
#             return Response({"error": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StockSerializer(stock)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         stock = self.get_object(pk)
#         if stock is None:
#             return Response({"error": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StockSerializer(stock, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         stock = self.get_object(pk)
#         if stock is None:
#             return Response({"error": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StockSerializer(stock, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         stock = self.get_object(pk)
#         if stock is None:
#             return Response({"error": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)
#         stock.delete()
#         return Response({"message": "Stock deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# # StockValue CRUD Operations
# class StockValueListCreateAPIView(APIView):
#     """Handles GET (list) and POST (create) operations for StockValue."""
#     def get(self, request):
#         stock_values = StockValue.objects.all()
#         serializer = StockValueSerializer(stock_values, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = StockValueSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StockValueDetailAPIView(APIView):
#     """Handles GET, PUT, PATCH, and DELETE operations for a specific StockValue."""
#     def get_object(self, pk):
#         try:
#             return StockValue.objects.get(pk=pk)
#         except StockValue.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         stock_value = self.get_object(pk)
#         if stock_value is None:
#             return Response({"error": "StockValue not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StockValueSerializer(stock_value)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         stock_value = self.get_object(pk)
#         if stock_value is None:
#             return Response({"error": "StockValue not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StockValueSerializer(stock_value, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         stock_value = self.get_object(pk)
#         if stock_value is None:
#             return Response({"error": "StockValue not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = StockValueSerializer(stock_value, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         stock_value = self.get_object(pk)
#         if stock_value is None:
#             return Response({"error": "StockValue not found."}, status=status.HTTP_404_NOT_FOUND)
#         stock_value.delete()
#         return Response({"message": "StockValue deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets, status
from rest_framework.response import Response
from stocks.models import Stock, StockValue
from .serializers import StockSerializer, StockValueSerializer

# Stock ViewSet
class StockViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for Stock."""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

# StockValue ViewSet
class StockValueViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for StockValue."""
    queryset = StockValue.objects.all()
    serializer_class = StockValueSerializer