from abc import ABC, abstractmethod


# Семейство классов для Hotel
class HotelBooking:
    @staticmethod
    def book():
        print('Hotel book work')


class HotelСancellater:
    pass


class HotelСhanger:
    pass


# Семейство классов для Flight
class FlightBooking:
    @staticmethod
    def book():
        print('Flight book work')


class FlightСancellater:
    pass


class FlightСhanger:
    pass


# Семейство классов для Carrental
class CarrentalBooking:
    @staticmethod
    def book():
        print('Carrental book work')


class CarrentalСancellater:
    pass


class CarrentalСhanger:
    pass


class AbstractFactory(ABC):

    @staticmethod
    def create_factory(sphere_name):
        SPHERES = {
            'Hotel': HotelFactory,
            'Flight': FlightFactory,
            'Carrental': CarrentalFactory
        }

        return SPHERES[sphere_name]()

    @abstractmethod
    def create_booking(self):
        pass

    @abstractmethod
    def create_cancellater(self):
        pass

    @abstractmethod
    def create_changer(self):
        pass


class HotelFactory(AbstractFactory):
    def create_booking(self):
        return HotelBooking()

    def create_cancellater(self):
        return HotelСancellater()

    def create_changer(self):
        return HotelСhanger()


class FlightFactory(AbstractFactory):
    def create_booking(self):
        return FlightBooking()

    def create_cancellater(self):
        return FlightСancellater()

    def create_changer(self):
        return FlightСhanger()


class CarrentalFactory(AbstractFactory):
    def create_booking(self):
        return CarrentalBooking()

    def create_cancellater(self):
        return CarrentalСancellater()

    def create_changer(self):
        return CarrentalСhanger()


sphere_name = input("Введите сферу услуг")
factory = AbstractFactory.create_factory(sphere_name)
booking = factory.create_booking()
cancellater = factory.create_cancellater()
changer = factory.create_changer()
booking.book()
