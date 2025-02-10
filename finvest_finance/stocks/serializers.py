from rest_framework import serializers
from stocks.models import Stock, StockValue
from datetime import datetime, timedelta


class StockSerializer(serializers.ModelSerializer):
    delta = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = '__all__'

    def get_delta(self, obj: Stock):
        # Get the current date and time
        now = datetime.now()

        # Calculate the start of the current week (Monday at 00:00)
        start_of_current_week = now - timedelta(days=now.weekday())
        start_of_current_week = start_of_current_week.replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        # Calculate the start of the previous week (Monday of last week)
        start_of_last_week = start_of_current_week - timedelta(weeks=1)

        # Fetch the StockValue objects for the start of the current and previous weeks
        stock_values = StockValue.objects.filter(
            stock=obj,
            created_at__gte=start_of_last_week,
            created_at__lt=start_of_current_week,
        ).order_by('created_at')

        if len(stock_values) == 2:
            # If two values are found, calculate the difference
            return stock_values.last().value - stock_values.first().value
        elif len(stock_values) == 1:
            # If one value is found, return it
            return stock_values[0].value
        else:
            # If no values are found, return 0
            return 0


class StockValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockValue
        fields = '__all__'
