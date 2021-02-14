from kivy.app import App
from kivy.uix import label, gridlayout, button, boxlayout
import pandemic
import Cities
import pandas
from test_pandemic import init_standard_setting


def get_color(color):
    colors = {
        Cities.SCHWARZ: ["black", "yellow"],
        Cities.BLAU: ["blue", "yellow"],
        Cities.GELB: [[255, 255, 0], "black"]
    }
    return colors[color][0], colors[color][1]


class CityButton(button.Button):

    def __init__(self, city, **kwargs):
        super(CityButton, self).__init__(**kwargs)
        self.city = city
        self.city_button_text()
        self.background_color, self.color = get_color(self.get_color())

    def name(self):
        return self.city.name

    def phase(self, index=None):
        if index is None:
            return self.city.phase
        else:
            return self.city.phase[index]

    def get_color(self):
        return self.city.color

    def city_button_text(self):
        btn_text = self.name() + " " + str(self.phase())
        btn_text = str(self.phase(-2)) + btn_text.rjust(30)
        self.text = btn_text


class PandemicFrame(boxlayout.BoxLayout):

    def __init__(self, **kwargs):
        super(PandemicFrame, self).__init__(**kwargs)
        self.padding = 10
        self.EPIDEMY = False
        self.PLAYER_1 = True
        self.orientation = "vertical"
        self.pandemic = pandemic.Pandemic()
        self.city_buttons = self.create_city_buttons()
        self.epidemy_button = self.create_epidemy_button()
        self.draw_button = self.create_draw_button()
        self.arrange_buttons()

    def epidemy_text(self):
        number, rest = divmod(self.pandemic.get_probability() * 100, 1)
        return "EPIDEMIE " + \
             str(number) + "%"

    def create_epidemy_button(self):
        ret = button.Button()
        ret.text = self.epidemy_text()

        def epidemy_function(init=False):
            if self.EPIDEMY or init:
                self.EPIDEMY = False
                ret.background_color = [0, 1, 0, 1]
                ret.color = "black"
            else:
                self.EPIDEMY = True
                ret.background_color = "white"
                ret.color = "red"
        epidemy_function(True)
        ret.on_press = epidemy_function
        return ret

    def create_draw_button(self):
        ret = button.Button(text="Spieler 1")

        def draw_function(init=False):
            if not self.PLAYER_1 or init:
                self.PLAYER_1 = True
                ret.text = "Spieler 1"
            else:
                self.PLAYER_1 = False
                ret.text = "Spieler 2"
            self.pandemic.add_draw()
            if not init:
                self.arrange_buttons()
        draw_function(True)
        ret.on_press = draw_function
        return ret

    def city_buttons_data(self):
        ret = []
        for city_button in self.city_buttons:
            phase = 0
            for pos in range(2, len(city_button.phase())+1):
                phase += city_button.phase(-pos)*(10**(1-pos))
                pass

            ret.append([city_button.name(), city_button.get_color(), phase, city_button])
        return ret

    def arrange_buttons(self):
        self.clear_widgets()
        self.epidemy_button.text = self.epidemy_text()
        self.add_widget(self.epidemy_button)
        self.add_widget(self.draw_button)
        city_dataframe = pandas.DataFrame(data=self.city_buttons_data(), columns=["name", "color", "phase", "button"])
        for index, city_row in city_dataframe.sort_values("phase", ascending=False).iterrows():
            city_button = city_row["button"]
            city_button.city_button_text()
            self.add_widget(city_button)

    def create_single_city_button(self, city, city_buttons):
        single_button = CityButton(city)

        def callback_function():
            return self.action_city_press(city, single_button)

        single_button.on_press = callback_function
        city_buttons.append(single_button)

    def action_city_press(self, city, city_button):
        if self.EPIDEMY:
            self.pandemic.epidemie(city)
            self.epidemy_button.on_press()
        else:
            Cities.add_city(city)
        self.arrange_buttons()

    def create_city_buttons(self):
        city_buttons = []
        for city in Cities.ALL_CITIES:
            self.create_single_city_button(city, city_buttons)
        return city_buttons


class PandemicApp(App):

    def build(self):
        main_layout = PandemicFrame()
        return main_layout


if __name__ == '__main__':
    init_standard_setting()
    PandemicApp().run()
