import random
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render
from tours import data


def reformat_price(tours):
    for item in tours.items():
        item[1]["price"] = '{:,}'.format(item[1]["price"]).replace(',', ' ')


reformat_price(data.tours)


def main_view(request):
    randomed_tours = dict()
    while len(randomed_tours) <= 5:
        key = random.randint(1, len(data.tours.items()))
        randomed_tours[key] = data.tours.setdefault(key)
    context = {"subtitle": data.subtitle, "description": data.description, "randomed_tours": randomed_tours,
               "departures": data.departures}

    return render(request, "index.html", context=context)


def departure_view(request, departure):
    num_tours_by_departure = 0
    tours_by_departure = dict()
    for item in data.tours.items():
        if item[1]["departure"] == departure:
            num_tours_by_departure += 1
            tours_by_departure[item[0]] = data.tours.setdefault(item[0])
    if departure not in data.departures:
        raise Http404()

    max_price = tours_by_departure[max(tours_by_departure, key=lambda x: tours_by_departure[x]["price"]
                                       )]["price"]
    min_price = tours_by_departure[min(tours_by_departure, key=lambda x: tours_by_departure[x]["price"]
                                       )]["price"]
    max_nights = tours_by_departure[max(tours_by_departure, key=lambda x: tours_by_departure[x]["nights"]
                                        )]["nights"]
    min_nights = tours_by_departure[min(tours_by_departure, key=lambda x: tours_by_departure[x]["nights"]
                                        )]["nights"]

    dep = data.departures.get(departure)
    dep = dep[0].lower() + dep[1:]
    context = {"departure_to_lower": dep,
               "num_tours_by_departure": num_tours_by_departure,
               "tours_by_departure": tours_by_departure,
               "max_price": max_price,
               "min_price": min_price,
               "max_nights": max_nights,
               "min_nights": min_nights,
               "departures": data.departures,
               "departure_as_url": departure
               }

    return render(request, "departure.html", context=context)


def tour_view(request, id):
    tour = data.tours.get(id)
    if tour is not None:
        dep = data.departures.get(tour.get("departure"))
        dep = dep[0].lower() + dep[1:]
    else:
        raise Http404()
    context = {"tour": data.tours.get(id), "departure": data.departures.get(tour.get("departure")),
               "departures": data.departures, "departure_to_lower": dep}
    return render(request, "tour.html", context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound("Страница не найдена!")


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
