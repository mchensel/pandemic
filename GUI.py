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


def city_button_text(city, single_button):
    btn_text = city.name + " " + str(city.phase)
    btn_text = str(city.phase[-1]) + btn_text.rjust(25)
    single_button.text = btn_text


class PandemicFrame(boxlayout.BoxLayout):

    def __init__(self, **kwargs):
        super(PandemicFrame, self).__init__(**kwargs)
        self.padding = 10
        self.orientation = "vertical"
        self.city_buttons = self.create_city_buttons()
        self.arrange_buttons(False)

    def arrange_buttons(self, stop=True):
        self.clear_widgets()
        city_dataframe = pandas.DataFrame(data=self.city_buttons, columns=["name", "color", "phase", "button"])
        for index, city_row in city_dataframe.sort_values("phase", ascending=False).iterrows():
            self.add_widget(city_row["button"])
            print(city_row["name"])
            print(city_row["phase"])


    def create_single_city_button(self, city, city_buttons):
        single_button = button.Button()
        city_button_text(city, single_button)
        single_button.background_color, single_button.color = get_color(city.color)

        def callback_function():
            return self.action_city_press(city, single_button)

        single_button.on_press = callback_function
        city_buttons.append([city.name, city.color, city.phase[-1], single_button])

    def action_city_press(self, city, city_button):
        pandemic.add_city(city)
        city_button_text(city, city_button)
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
