

class City:
    """
    Eine Stadt mit Info über:
    Infektionskarten und deren Status
    """
    def __init__(self, city_name, color, gesamt=4):
        self.color = color
        self.name = city_name
        self.gesamt = gesamt
        self.phase = self.reset()

    def reset(self):
        self.phase = [self.gesamt, 0]
        return self.phase


SCHWARZ = "Schwarz"
GELB = "Gelb"
BLAU = "Blau"

ISTANBUL = City("ISTANBUL", SCHWARZ)
KAIRO = City("KAIRO", SCHWARZ)
TRIPOLIS = City("TRIPOLIS", SCHWARZ)

LAGOS = City("LAGOS", GELB)
SAO_PAOLO = City("SAO PAOLO", GELB)
JACKSONVILLE = City("JACKSONVILLE", GELB)

LONDON = City("LONDON", BLAU)
NEW_YORK = City("NEW_YORK", BLAU)
WASHINGTON = City("WASHINGTON", BLAU)
CHICAGO = City("CHICAGO", BLAU, 2)

SCHWARZE_CITIES = [
    ISTANBUL,
    KAIRO,
    TRIPOLIS]

GELBE_CITIES = [
    LAGOS,
    SAO_PAOLO,
    JACKSONVILLE
]
BLAUE_CITIES = [
    LONDON,
    NEW_YORK,
    WASHINGTON,
    CHICAGO
]

CITIES = {SCHWARZ: SCHWARZE_CITIES, GELB: GELBE_CITIES, BLAU: BLAUE_CITIES}
ALL_CITIES = set([])
for color_city in CITIES.values():
    for l_city in color_city:
        ALL_CITIES.add(l_city)


def add_city(city):
    if city is None:
        return
    pos = -2
    while city.phase[pos] == 0:
        pos -= 1
        if abs(pos) > len(city.phase):
            return
    city.phase[-1] += 1
    city.phase[pos] -= 1


def for_all_cities(f):
    ret = []
    for city in ALL_CITIES:
        ret.append(f(city))
    return ret
