
import Cities

global STAPEL


def add_city(city):
    city.phase[-1] += 1
    pos = -2
    while city.phase[pos] == 0:
        pos -= 1
    city.phase[pos] -= 1


def for_all_cities(f):
    ret = []
    for city in Cities.ALL_CITIES:
        ret.append(f(city))
    return ret


def epidemie(city):
    city.phase[-1] += 1
    city.phase[0] -= 1
    for_all_cities(lambda c: c.phase.append(0))


def next_x_infects(x, city):
    def gather_cards_in_phase(xx, phase=-2, stapel={}):
        def phasen_stapel(c):
            if c.name not in stapel:
                stapel[c.name] = 0
            stapel[c.name] += c.phase[phase]
            return stapel[c.name]

        all_cards = max(sum(for_all_cities(phasen_stapel)), 0)
        if all_cards < xx:
            return gather_cards_in_phase(xx-all_cards, phase - 1, stapel)
        return stapel
    stapel = gather_cards_in_phase(x)

    return stapel[city.name]


def main():
    pass


if __name__ == '__main__':
    main()
