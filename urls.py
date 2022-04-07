from datetime import date
from views import Index, About, Hotels, Flights, Carrental, CreateCategory, CategoryList, HotelsList, FlightsList, \
    CarrentalsList, CreateHotel, CreateFlight, CreateCarrental, CopyHotel, CopyFlight, CopyCarrental


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/hotels/': Hotels(),
    '/flights/': Flights(),
    '/carrental/': Carrental(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/hotels-list/': HotelsList(),
    '/flights-list/': FlightsList(),
    '/carrentals-list/': CarrentalsList(),
    '/create-hotel/': CreateHotel(),
    '/create-flight/': CreateFlight(),
    '/create-carrental/': CreateCarrental(),
    '/copy-hotel/': CopyHotel(),
    '/copy-flight/': CopyFlight(),
    '/copy-carrental/': CopyCarrental(),
}

