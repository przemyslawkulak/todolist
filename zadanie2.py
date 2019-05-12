import random
import string


class Car:

    def __init__(self, brand, tank_capacity, tanked_fuel):
        """

        :param brand: string: Car's brand
        :param tank_capacity: number:maximum tank volume in liters
        :param tanked_fuel: the number of liters of fuel in the tank
        tank_full_in: percentage filling of the tank
        """
        self.brand = brand
        self.tank_capacity = tank_capacity
        self.tanked_fuel = tanked_fuel
        tank_full_in = round(self.tanked_fuel / self.tank_capacity * 100, 1)
        print('New car of brand {}, with tank full in {}%'.format(self.brand, tank_full_in))

    def fill_tank(self, limit=None, liters=None):
        """
        without parameters: method fills full tank
        :param limit: number between 0 and 1: Fills the tank with fuel to this limit
        :param liters: number: fills the tank with the number of liters fuel.
        :return: amount of filled tank
        """
        if limit is None and liters is None:
            tanked = self.tank_capacity - self.tanked_fuel
            self.tanked_fuel = self.tank_capacity
            return tanked
        # fill tank with argument limit
        elif limit is not None and liters is None:
            if isinstance(limit, (int, float)) and 0 <= limit <= 1:
                if limit * self.tank_capacity > self.tanked_fuel:
                    tanked = limit * self.tank_capacity - self.tanked_fuel
                    self.tanked_fuel = limit * self.tank_capacity
                else:
                    tanked = 0
                return tanked
            else:
                raise ValueError("limit must be number between 0 and 1")
        # fill tank with argument liters
        elif limit is None and liters is not None:
            if isinstance(liters, (int, float)):
                if liters + self.tanked_fuel <= self.tank_capacity:
                    self.tanked_fuel = liters + self.tanked_fuel
                    return liters
                else:
                    raise ValueError("The tank will not fit that amount of fuel, it will go up to maximum {} l".format(
                        self.tank_capacity - self.tanked_fuel))

            else:
                raise ValueError("liters must be number")
        else:
            raise Exception("You can not specify both the limit and the number of liters you want tank")

    def __repr__(self):
        return '<Car at {} of brand {}, with tank full in {}%>'.format(hex(id(self)), self.brand, round(
            self.tanked_fuel / self.tank_capacity * 100, 1))


class EnvironmentalError(Exception):
    """
    custom Exception
    """
    pass


class DieselCar(Car):

    def fill_tank(self, limit=None, liters=None):
        """
        overwritten method fill_tank
        :param limit:
        :param liters:
        :return: raise EnvironmentalError
        """
        raise EnvironmentalError(" Diesel fuel not available due to environmental reasons")


def _random_string(length=8):
    """
    function to create random brand name
    :param length: length of word
    :return: random string
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_carpool(amount):
    """
    function to create list of Car's class instances
    :param amount: number of random car
    :return: list of Car class instances with random brand, tank_capacity and tanked_fuel
    """
    car_number = 0
    car = []
    all_brands = []
    while car_number < amount:
        brand = _random_string()
        capacity = random.randint(1, 101)
        if brand not in all_brands:
            car.append(Car(brand, capacity, capacity * random.random()))
            car_number += 1
            all_brands.append(brand)

        else:
            print("{} brand was already used".format(brand))


get_carpool(8)
c = Car("fiat", 30, 5)
c.fill_tank(limit=0.5)
c.fill_tank(liters=5)
c.fill_tank(liters=3)
c.fill_tank()
# c.fill_tank(limit=0.5, liters=5)
d = DieselCar("mercedes", 30, 10)
d.fill_tank()
