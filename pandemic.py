
import Cities

global STAPEL


def add_city(city):
    city.phase[-1] += 1


def for_all_cities(f):
    ret = []
    for city in Cities.ALL_CITIES:
        ret.append(f(city))
    return ret


def epidemie(city):
    city.phase[-1] += 1
    city.epidemie[-1] = 1
    for_all_cities(lambda c: c.phase.append(0))
    for_all_cities(lambda c: c.epidemie.append(0))


def next_x_infects(x, city):
    def gather_cards_in_phase(xx, phase=-1, stapel={}):
        def f(c):
            if c.name not in stapel:
                stapel[c.name] = -c.phase[-1]
                return -c.phase[-1]
            if len(c.phase) + phase < 0:
                stapel[c.name] = max(stapel[c.name] + c.gesamt, c.gesamt)
                return stapel[c.name]
            ret = c.phase[phase]
            stapel[c.name] += ret
            return stapel[c.name]

        all_cards = max(sum(for_all_cities(f)),0)
        if all_cards < xx:
            return gather_cards_in_phase(xx-all_cards, phase - 1, stapel)
        return stapel
    stapel = gather_cards_in_phase(x)

    return stapel[city.name]


def main():
    pass


if __name__ == '__main__':
    main()
