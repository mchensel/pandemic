
import Cities


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
    for city in Cities.ALL_CITIES:
        ret.append(f(city))
    return ret


def epidemie(city):
    if city is None:
        return
    city.phase[-1] += 1
    city.phase[0] -= 1
    for_all_cities(lambda c: c.phase.append(0))


def get_stack_of_x_draws(draws, phase=-2, stack={}):
    def phasen_stapel(c):
        if c.name not in stack:
            stack[c.name] = 0
        stack[c.name] += c.phase[phase]
        return stack[c.name]

    all_cards = max(sum(for_all_cities(phasen_stapel)), 0)
    if all_cards < draws:
        return get_stack_of_x_draws(draws - all_cards, phase - 1, stack)
    return stack


def next_x_infects(x, city):
    stack = get_stack_of_x_draws(draws=x, stack={})
    return stack[city.name]


def draw():
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
        epidemie(city)
    else:
        add_city(city)
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
    while True:
        city, infects = draw()
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
