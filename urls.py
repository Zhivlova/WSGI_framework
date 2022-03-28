from datetime import date
from views import Index, About, Hotels, Flights, Carrental


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
}

