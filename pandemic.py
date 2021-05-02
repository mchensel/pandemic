
import Cities

ALL = sum(Cities.for_all_cities(lambda c: c.gesamt))
CARDS_PER_EPIDEMY = (ALL-8) / 6


class Pandemic:

    def __init__(self):
        self.DRAWS = 0
        self.NUMBER_OF_EPIDEMIES = 0

    def add_draw(self):
        self.DRAWS += 1

    def epidemie(self, city):
        if city is None:
            return
        city.phase[-1] += 1
        city.phase[0] -= 1
        self.NUMBER_OF_EPIDEMIES += 1
        Cities.for_all_cities(lambda c: c.phase.append(0))

    def get_probability(self):
        rounds, number_in_stack = divmod(self.DRAWS * 2, CARDS_PER_EPIDEMY)
        next_round = CARDS_PER_EPIDEMY - number_in_stack
        if self.NUMBER_OF_EPIDEMIES * CARDS_PER_EPIDEMY > self.DRAWS * 2:
            if next_round == 1:
                return 1 / CARDS_PER_EPIDEMY
            if next_round == 0:
                return 2 / CARDS_PER_EPIDEMY
            return 0
        return min(2 / next_round, 1)


def get_stack_of_x_draws(draws, phase=-2, stack={}):
    def phasen_stapel(c):
        if c.name not in stack:
            stack[c.name] = 0
        stack[c.name] += c.phase[phase]
        return stack[c.name]

    all_cards = max(sum(Cities.for_all_cities(phasen_stapel)), 0)
    if all_cards < draws:
        return get_stack_of_x_draws(draws - all_cards, phase - 1, stack)
    return stack


def next_x_infects(x, city):
    stack = get_stack_of_x_draws(draws=x, stack={})
    return stack[city.name]


def draw(my_pandemic: Pandemic):
    """
    usage:
    [e,o] [<cityname:str>] [<next infection draws:int>] [<number of next draws for analyze>]
    detail:
    e <cityname:str> [<next infection draws>]: there is an epidemy with <cityname> as drawn city and
        optionally <next infection draws> as next infection draws
    o <number of next draws for analyze> : just return  <number of next draws for analyze>
    :return: City (obj) , int | False
    """
    def get_city():
        user = input("City/EPIDEMY:")
        if not user:
            return get_city()
        L = user.split()
        epi = False
        if len(L) > 1:
            if L[0] not in 'eo':
                print("nur 1 Wort oder e,o")
                return get_city()
            if L[0].lower() == "e":
                user_ = L[1]
                epi = True
            elif L[0].lower() == "o":
                return None, L[1]
        else:
            user_ = L[0].lower()
        for city in Cities.ALL_CITIES:
            if city.name.lower().startswith(user_):
                return city, epi
        print("not found.")
        return get_city()

    city, epi = get_city()
    if epi:
        my_pandemic.epidemie(city)
    else:
        my_pandemic.add_city(city)
    return city, epi


def output(stack):
    full_text = ["----------------"]
    for city in stack:
        if stack[city] > 0:
            ret_text = city + ": " + str(stack[city])
            full_text.append(ret_text)
    full_text.append("-------------------------------------------")
    return "\n".join(full_text)


def main():
    infection = 2
    old_infection = infection
    my_pandemic = Pandemic()
    while True:
        city, infects = draw(my_pandemic)
        if city is None:
            old_infection = infection
            try:
                infection = int(infects)
            except:
                pass
        print(output(get_stack_of_x_draws(infection, stack={})))
        if city is None:
            infection = old_infection


if __name__ == '__main__':
    main()
