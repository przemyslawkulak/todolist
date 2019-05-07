import random
import string


class Car:

    def __init__(self, brand, tank_capacity, tanked_fuel):
        self.brand = brand
        self.tank_capacity = tank_capacity
        self.tanked_fuel = tanked_fuel
        tank_full_in = round(self.tanked_fuel / self.tank_capacity * 100, 1)
        print('New car of brand {}, with tank full in {}%'.format(self.brand, tank_full_in))

    def fill_tank(self, limit=None, liters=None):

        if limit is None and liters is None:
            tanked = self.tank_capacity - self.tanked_fuel
            self.tanked_fuel = self.tank_capacity
            print(f'zatankowano:{tanked} l do pełna')
            return tanked
        # fill tank with argument limit
        elif limit is not None and liters is None:
            if isinstance(limit, (int, float)) and 0 <= limit <= 1:
                if limit * self.tank_capacity > self.tanked_fuel:
                    tanked = limit * self.tank_capacity - self.tanked_fuel
                    self.tanked_fuel = limit * self.tank_capacity
                else:
                    tanked = 0
                print(f'zatankowano:{tanked} l do {limit * 100}%')
                return 0
            else:
                raise ValueError("limit musi być liczbą pomiędzy 0 and 1")
        # fill tank with argument liters
        elif limit is None and liters is not None:
            if isinstance(liters, (int, float)):
                if liters + self.tanked_fuel <= self.tank_capacity:
                    self.tanked_fuel = liters + self.tanked_fuel
                    print(f'zatankowano:{liters} l')
                    return liters
                else:
                    raise ValueError("bak nie zmieści takiej ilości paliwa, wejdzie maksymalnie {} l".format(
                        self.tank_capacity - self.tanked_fuel))

            else:
                raise ValueError("liters musi być liczbą")
        else:
            raise Exception("Nie możesz podać równocześnie limitu i liczby wlewanych litrów")

    def __repr__(self):
        return '<Car at {} of brand {}, with tank full in {}%>'.format(hex(id(self)), self.brand, round(
            self.tanked_fuel / self.tank_capacity * 100, 1))


class DieselCar(Car):

    def fill_tank(self, limit=None, liters=None):
        raise Exception('​ Diesel fuel not available due to environmental reasons')


def _random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_carpool(amount):
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
            print(f"był {brand}")


get_carpool(8)
c = Car("fiat", 30, 5)
c.fill_tank(limit=0.5)
c.fill_tank(liters=35)
c.fill_tank(liters=3)
c.fill_tank()
# c.fill_tank(limit=0.5, liters=5)
d = DieselCar("mercedes", 30, 10)
# d.fill_tank()