from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
import re
from SecondApplication import SecondApp

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

KV = """
CustomGrid:
    cols:1
    rows:3
    md_bg_color: 0,1,1,1
    MDFloatLayout :
        MDLabel:
            id: labh
            text: 'Height:'
            size_hint: None, None
            pos_hint: {'center_x':0.2, 'center_y':0.8}
        
        MDTextField:
            id: heightid
            height_txt: "190"
            text:self.height_txt
            #halign: 'center'
            pos_hint: {'center_x':0.6, 'center_y':0.8}
            size_hint: 0.3,None
            hint_text: "Helper text on focus"
            helper_text: "This will disappear when you click off"
            helper_text_mode: "on_focus"
            on_text: root.propertychanged(labh.text)
            

    MDFloatLayout:
        
        MDLabel:
            id: labw
            text: 'Weight:'
            size_hint: None, None
            pos_hint: {'center_x':0.2, 'center_y':0.6}

        MDTextField:
            id: weightid
            size_hint: 0.3, None
            weight_txt: "80"
            text: self.weight_txt
            pos_hint: {'center_x':0.6, 'center_y':0.6}
            hint_text: "Helper text on focus"
            helper_text: "This will disappear when you click off"
            helper_text_mode: "on_focus"
            on_text: root.propertychanged(labw.text)
    
    MDFloatLayout:
        
        MDRoundFlatIconButton:
            text:  'Enter'
            id: btn
            pos_hint: {"center_x": .2, "center_y": .9}
            on_press: root.onenter()

        MDLabel:

            id: resultid
            text: 'Result'
            size_hint: 0.3, None
            pos_hint: {'center_x':0.6, 'center_y':0.9}
    

"""


class CustomToolbar(ThemableBehavior, RectangularElevationBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class CustomGrid(GridLayout, EventDispatcher):
    height_txt = StringProperty("189")
    weight_txt = StringProperty("80")

    def __init__(self, **kwargs):
        super(CustomGrid, self).__init__(**kwargs)

    def propertychanged(self, value):

        if self.ids.heightid.text == "" or self.ids.weightid.text == "":
            self.ids.btn.disabled = True
            return
        elif re.findall("\\D+", self.ids.heightid.text) or re.findall("\\D+", self.ids.weightid.text):
            self.ids.btn.disabled = True
            return
        elif int(self.ids.heightid.text) > 400 or int(self.ids.weightid.text) > 400:
            self.ids.btn.disabled = True
            return
        self.ids.btn.disabled = False
        return

    def onenter(self):
        height = self.ids.heightid.text
        weight = self.ids.weightid.text

        self.ids.resultid.text = self.computeBMI(height, weight)

    def computeBMI(self, height, weight):
        height = float(height)
        weight = int(weight)

        bmi = (weight / (height * height)) * 10000

        if bmi < 18:
            message = f"your BMI: {bmi:.02f} -  Underweight"
        elif 18 <= bmi < 25:
            message = f"your BMI: {bmi:.02f} -  Normal weight"
        elif 25 <= bmi < 30:
            message = f"your BMI: {bmi:.02f} -  Overweightt"
        else:
            message = f"your BMI: {bmi:.02f} -  Obesity"

        return message


class BMIApplicationApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    # showbothwindow()
    # SecondApp().run()
    BMIApplicationApp().run()
