from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ChooseCity, ChooseStartDate, ChooseEndDate
from .module import get_info_from_site, upload_data_to_base, calculate_data_to_show


def main(request):
    city_name = ChooseCity()
    start_date = ChooseStartDate()
    end_date = ChooseEndDate()
    return render(request, "main_page.html", {
        "city_name": city_name,
        "start_date": start_date,
        "end_date": end_date
    })


def city(request):
    if request.method == "POST":
        city_name_form = ChooseCity(request.POST)
        start_date_form = ChooseStartDate(request.POST)
        end_date_form = ChooseEndDate(request.POST)
        if city_name_form.is_valid() and\
                start_date_form.is_valid() and\
                end_date_form.is_valid():
            info_from_site = get_info_from_site(request.POST)
            upload_data_to_base(info_from_site.json())
            context = calculate_data_to_show(request)
            return render(request, "city.html", context)
    else:
        city_name = ChooseCity()
        start_date = ChooseStartDate()
        end_date = ChooseEndDate()
        return HttpResponseRedirect(reverse("main/", {
            "city_name": city_name,
            "start_date": start_date,
            "end_date": end_date
        }))

