STARTING_NUMBER_OF_COINS = 1_000_000
PART_TO_GIVE = 1000

class City:
    def __init__(self, x: int, y: int, balance: dict):
        self.x = x
        self.y = y
        self.balance = balance
        self.neighbors: list[City] = []
        self.new_balance = {}

    def add_new_balance(self):
        for k, v in self.new_balance.items():
            if k in self.balance:
                self.balance[k] += v
            else: 
                self.balance[k] = v
        
        self.new_balance = {}

    def is_completed(self) -> bool:
        return len(self.balance) == countries_number

class Country:
    def __init__(self, name: str, xl: int, yl: int, xh: int, yh: int):
        self.name = name
        self.cities = [
            City(x, y, {self.name: STARTING_NUMBER_OF_COINS})
            for y in range(yl, yh + 1)
            for x in range(xl, xh + 1)
        ]

        self.comletion_date = -1

    def is_completed(self) -> bool:
        return all([c.is_completed() for c in self.cities])

class DaysGoBy:
    def __init__(self, countries: list[Country]):
        self.countries: list[Country] = countries
        self.cities: list[City] = []
        self.days = 0

    def init_neighbors(self):
        for country in self.countries:
            for city in country.cities:
                self.cities.append(city)
                for neighbor_country in self.countries:
                    for neighbor_city in neighbor_country.cities:
                        if (abs(city.x - neighbor_city.x) + abs(city.y - neighbor_city.y)) == 1:
                            city.neighbors.append(neighbor_city)

    def next_day(self):
        for c in self.cities:
            money_to_give = {}

            for k, v in c.balance.items():
                if v // PART_TO_GIVE > 0:
                    money_to_give[k] = v // PART_TO_GIVE
            
            for k, v in money_to_give.items():
                if k in c.new_balance:
                    c.new_balance[k] -= v * len(c.neighbors)
                else:
                    c.new_balance[k] = -v * len(c.neighbors)

                for n in c.neighbors:
                    if k in n.new_balance:
                        n.new_balance[k] += v
                    else:
                        n.new_balance[k] = v

        for c in self.cities:
            c.add_new_balance()

        self.days +=1

    def check_complitions(self) -> bool:
        for c in self.countries:
            if c.is_completed() and c.comletion_date == -1:
                c.comletion_date = self.days

        return all([c.is_completed() for c in self.countries])

    def run(self):
        while (not self.check_complitions()) and self.days < 100000:
            self.next_day()


def validate_coordinates(xl: int, yl: int, xh: int, yh: int):
    if xl > xh or yl > yh:
        raise ValueError("xl > xh or yl > yh")
    if xl < 0 or yl < 0 or xh < 0 or yh < 0:
        raise ValueError("xl < 0 or yl < 0 or xh < 0 or yh < 0")

def read_case(lines, current_line, num_lines):
    countries: list[Country] = []
    for i in range(num_lines):
        line: str = lines[current_line + i]
        vals = line.rstrip().split(' ')
        validate_coordinates(int(vals[1]), int(vals[2]), int(vals[3]), int(vals[4]))
        countries.append(Country(vals[0], int(vals[1]), int(vals[2]), int(vals[3]), int(vals[4])))
    return countries


cases = []
countries_number = 0
input_file = open("input.txt", "r")

lines = input_file.readlines()

line = 0
num = int(lines[line])

while num != 0:
    cases.append(read_case(lines, line + 1, num))
    line += num + 1
    num = int(lines[line])
    
case_n = 1
for c in cases:
    countries_number = len(c)
    game = DaysGoBy(c)
    game.init_neighbors()
    game.run()
    print('Case Number %i' % (case_n))
    case_n += 1
    game.countries.sort(key=lambda c : c.name)
    game.countries.sort(key=lambda c : c.comletion_date)
    for c in game.countries:
        print("%s %i" % (c.name, c.comletion_date))


    