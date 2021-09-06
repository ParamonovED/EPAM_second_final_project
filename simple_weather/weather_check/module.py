import math
import os
from collections import defaultdict
import requests
from django.db.models import Max, Min, Avg, Count
from .models import City


def get_info_from_site(request_data: dict):
    link = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx"
    secret_key = os.environ.get("API_KEY")
    payload = {
        "q": request_data["choosen_city"],
        "date": request_data["choosen_startdate"],
        "enddate": request_data["choosen_enddate"],
        "format": "json",
        "key": secret_key
    }
    response = requests.get(link, params=payload)
    return response


def upload_data_to_base(data: dict):
    city_name = data["data"]["request"][0]["query"]
    for date in data["data"]["weather"]:
        cc = City.objects.filter(city_name=city_name, date=date["date"]).count()
        if cc >= 1:
            continue
        hourly = date["hourly"]
        day = City()
        day.city_name = city_name
        day.date = str(date["date"])
        day.date_year = str(date["date"][:4])
        day.date_month = str(date["date"][5:7])
        day.date_day = str(date["date"][8:])

        day.avg_temp_of_day = date["avgtempC"]
        day.max_temp_of_day = date["maxtempC"]
        day.min_temp_of_day = date["mintempC"]

        day.precipMM = sum(
            [float(time["precipMM"])for time in hourly]) / len(hourly)

        day.most_common_weather = find_most_common_weather(
            [time["weatherDesc"][0]["value"] for time in hourly])

        day.wind_avg_direction = calculate_average_wind_direction(
            [int(time["winddirDegree"]) for time in hourly])

        day.wind_avg_velocity = sum(
            [int(time["windspeedKmph"])for time in hourly]) / len(hourly)

        day.save()


def calculate_data_to_show(request):
    context = {}
    city_name = request.POST["choosen_city"]
    start_date = request.POST["choosen_startdate"]
    end_date = request.POST["choosen_enddate"]
    data_to_show = City.objects.filter(
        city_name__startswith=city_name,
        date__range=(start_date, end_date),
    )
    context["city_name"] = city_name
    context["start_date"] = data_to_show.first().date
    context["end_date"] = data_to_show.last().date

    context["min_temp_per_period"] = data_to_show.aggregate(
        Min("min_temp_of_day"))["min_temp_of_day__min"]

    context["avg_temp_per_period"] = round(data_to_show.aggregate(
        Avg("avg_temp_of_day"))["avg_temp_of_day__avg"])

    context["max_temp_per_period"] = data_to_show.aggregate(
        Max("max_temp_of_day"))["max_temp_of_day__max"]

    if int(start_date[:4]) < int(end_date[:4]) + 2:
        context["years_avg_min"] = data_to_show.values("date_year").annotate(
            Avg("min_temp_of_day")
        ).order_by("date_year")
        context["years_avg_max"] = data_to_show.values("date_year").annotate(
            Avg("max_temp_of_day")
        ).order_by("date_year")

    days_without_precipitation = data_to_show.annotate(
        Count("precipMM")).filter(precipMM=0).count()

    context["percent_days_of_precipitation"] = round(
        days_without_precipitation / data_to_show.annotate(
            days=Count("precipMM")
        )
        .count() * 100
    )

    context["most_common_precipitations"] = data_to_show.values(
        "most_common_weather"
    ).annotate(
        count=Count("most_common_weather")).order_by("-count")[:2]

    context["avg_wind_speed"] = round(
        data_to_show.aggregate(
            Avg("wind_avg_velocity"
                )
        )["wind_avg_velocity__avg"])
    wind_directions = [day.wind_avg_direction for day in data_to_show]

    context["avg_wind_direction"] = round(
        calculate_average_wind_direction(wind_directions)
    )

    return context


def find_most_common_weather(descriptions):
    d = defaultdict(int)
    for value in descriptions:
        d[value] += 1
    result, _ = max(d.items(), key=lambda x: x[1])
    return result


def calculate_average_wind_direction(winds: list):  # without speed
    sin_m = []
    cos_m = []
    for i in range(len(winds)):
        sin_m.append(math.sin(winds[i]*math.pi/180))
        cos_m.append(math.cos(winds[i]*math.pi/180))
    atan_rad = math.atan2(sum(sin_m)/len(winds), sum(cos_m)/len(winds))
    return round(atan_rad*180/math.pi)
