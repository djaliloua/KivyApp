import re

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.screen import MDScreen

kv = """
Screen:
    #orientation: "vertical"
    MDBoxLayout:
        orientation: "vertical"
        size_hint: 1, 0.1
        pos_hint: {"top": 1}
        md_bg_color: app.theme_cls.primary_light
        MDTopAppBar:
            title: "MDToolbar"
        
    MDBoxLayout:
        orientation: "vertical"
        #md_bg_color: app.theme_cls.primary_color
    
"""
kv1 = """
<CustumBox>:
    orientation: "vertical"
    MDBoxLayout:
        orientation: "vertical"
        size_hint: 1, 0.1
        md_bg_color: "teal"
        MDLabel:
            id: lbl
            text: "0"
            size_hint: 1, 0.5
            pos_hint: {"center_x":1}
            
    MDBoxLayout:
        orientation: "vertical"
        GridLayout:
            rows: 5
            cols: 4
            MDRaisedButton:
                text: "AC"
                id: AC
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.deleteall()
            MDRaisedButton:
                text: "del"
                #text_color: "red"
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.delete(lbl.text)
            MDRaisedButton:
                text: "%"
                id: percentage
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.computepercentage()
            MDRaisedButton:
                text: "/"
                id: div
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "7"
                id: n7
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "8"
                id: n8
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "9"
                id: n9
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "*"
                id: X
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "4"
                id: n4
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "5"
                id: n5
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "6"
                id: n6
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "-"
                id: subs
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "1"
                id: n1
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "2"
                id: n2
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "3"
                id: n3
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "+"
                id: plus
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "("
                id: parenthesis
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.addparenthesis(self.text)
                
            MDRaisedButton:
                text: "0"
                id: n0
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                text: "."
                id: dot
                size_hint: 1/4,1/5
                md_bg_color: "blue"
                on_press: root.signs(self.text)
            MDRaisedButton:
                id: equality
                text: "="
                size_hint: 1/4,1/5
                md_bg_color: "green"
                on_press: root.compute()
                
<CustomGrid>:
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
    
<ItemDrawer>:
    theme_text_color: "Custom"
    #on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color


<ContentNavigationDrawer>:
    ScrollView:
        MDList:
            ItemDrawer:
                text: "Home"
                icon: "home"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Home"
            ItemDrawer:
                text: "BMI Application"
                icon: "weight-kilogram"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "bmi"
            ItemDrawer:
                text: "Calculator"
                icon: "calculator"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "calculator"
            ItemDrawer:
                text: "send message"
                icon: "message"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "message"
            ItemDrawer:
                text: "download yt video"
                icon: "download"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "download"
MDScreen:
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: toolbar
            pos_hint: {"top": 1}
            title: "Menu"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        Widget:
    MDNavigationLayout:
        x: toolbar.height
        ScreenManager:
            id: screen_manager
            MDScreen:
                name: "Home"
                MDFloatLayout:
                    #orientation:"vertical"
                    MDLabel:
                        text: "Welcome to Lynn Application.\\n Go to Menu and select an application"
                        size_hint: dp(0.5), dp(.4)
                        pos_hint: {"center_x": 0.4, "center_y": 0.8}
                        #md_bg_color: app.theme_cls.primary_light
                
            MDScreen:
                name: "bmi"
                MDFloatLayout:
                    #orientation:"vertical"
                    CustomGrid:
                        #size_hint: None, 0.3
                        pos_hint: {"center_x": 0.5, "center_y": 0.3}
                        #md_bg_color: app.theme_cls.primary_light
            MDScreen:
                name: "calculator"
                MDFloatLayout:
                    CustumBox:
                        pos_hint: {"center_x": 0.5, "center_y": 0.425}
                        size_hint: 1, .85
                    
            MDScreen:
                name: "message"
                MDFloatLayout:
                    #orientation:"vertical"
                    MDLabel:
                        text: "ToDo: send message App"
                        #size_hint: None, 0.3
                        pos_hint: {"center_x": 0.5, "center_y": 0.3}
                        #md_bg_color: app.theme_cls.primary_light
            MDScreen:
                name: "download"
                MDFloatLayout:
                    #orientation:"vertical"
                    MDLabel:
                        text: "ToDo: Download youtube video"
                        #size_hint: None, 0.3
                        pos_hint: {"x": 0.5, "center_y": 0.3}
                        #md_bg_color: app.theme_cls.primary_light
                
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
    
"""


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class CustumBox(MDBoxLayout):
    def compute(self):
        try:
            self.ids.lbl.text = str(eval(self.ids.lbl.text))
        except Exception as ex:
            self.ids.lbl.text = str(ex)

    def deleteall(self):
        self.ids.lbl.text = "0"
        self.ids.AC.text = "AC"
        if self.ids.parenthesis.text == ")":
            self.ids.parenthesis.text = "("

    def delete(self, value):
        if value == "0":
            self.ids.AC.text = "AC"
            return
        if len(value) == 1:
            self.ids.lbl.text = "0"
            self.ids.AC.text = "AC"
            return
        self.ids.lbl.text = value[:-1]

    def signs(self, value):
        if self.ids.lbl.text == "0":
            self.ids.lbl.text = value
            self.ids.AC.text = "C"
            return
        self.ids.lbl.text += value

    def ischeck(self, value):
        sign = ["*", "/", "-", "+"]
        for s in sign:
            if s in value:
                return True
        return False

    def computepercentage(self):
        if self.ids.lbl.text != "0" and not self.ischeck(self.ids.lbl.text):
            self.ids.lbl.text = str(float(self.ids.lbl.text) / 100)
            return
        head = self.ids.lbl.text[:-1]
        tail = self.ids.lbl.text[len(self.ids.lbl.text) - 1]
        self.ids.lbl.text = head + str(float(tail) / 100)

    def addparenthesis(self, value):
        if self.ids.lbl.text == "0":
            if value == "(":
                self.ids.AC.text = "C"
                self.ids.lbl.text += value
                self.ids.parenthesis.text = ")"
                self.ids.lbl.text = value
                return
        if value == "(":
            self.ids.lbl.text += value
            self.ids.parenthesis.text = ")"
            return

        if value == ")":
            self.ids.lbl.text += value
            self.ids.parenthesis.text = "("
            return


class CustomGrid(GridLayout):
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
        elif int(self.ids.heightid.text) > 250 or int(self.ids.weightid.text) > 500:
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


class CustomScreen(MDScreen):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class DesignApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(kv1)


mainApp = DesignApp()
mainApp.run()

