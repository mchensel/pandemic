from kivy.app import App
from kivy.uix import label, gridlayout
import pandemic
import Cities


class Pandemic_App(App):
    def build(self):
        pandemic.add_city(Cities.ISTANBUL)
        ret = pandemic.output(pandemic.get_stack_of_x_draws(2, stack={}))
        return label.Label(text=ret)


if __name__ == '__main__':
    Pandemic_App().run()
