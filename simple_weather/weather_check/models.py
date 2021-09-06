from django.db import models


class City(models.Model):
    city_name = models.CharField("City name", max_length=100)
    date = models.DateField()
    date_year = models.IntegerField(verbose_name="weather year")  # maybe expand to year/month/day/time
    date_month = models.IntegerField(verbose_name="weather month")
    date_day = models.IntegerField(verbose_name="weather day")
    min_temp_of_day = models.FloatField(null=True)
    avg_temp_of_day = models.FloatField(null=True)
    max_temp_of_day = models.FloatField(null=True)
    precipMM = models.FloatField(null=True)
    most_common_weather = models.CharField(max_length=100)
    wind_avg_velocity = models.FloatField(null=True)
    wind_avg_direction = models.FloatField(null=True)

    def __str__(self):
        return self.city_name
