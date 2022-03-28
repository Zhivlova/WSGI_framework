from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'


class Hotels:
    def __call__(self, request):
        return '200 OK', 'hotels'


class Flights:
    def __call__(self, request):
        return '200 OK', 'flights'


class Carrental:
    def __call__(self, request):
        return '200 OK', 'carrental'


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
