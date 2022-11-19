from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

KV = """
CustumBox:
    orientation: "vertical"
    BoxLayout:
        orientation: "vertical"
        size_hint: 1, 0.1
        
        Label:
            id: lbl
            text: "0"
            size_hint: 1, 1
            font_size: "40sp"
            pos_hint: {"center_x":0.5}
            
    BoxLayout:
        orientation: "vertical"
        GridLayout:
            rows: 5
            cols: 4
            Button:
                text: "AC"
                id: AC
                font_size: "40sp"
                size_hint: 1/4,1/5
                on_press: root.deleteall()
            Button:
                text: "del"
                #text_color: "red"
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.delete(lbl.text)
            Button:
                text: "%"
                id: percentage
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.computepercentage()
            Button:
                text: "/"
                id: div
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "7"
                id: n7
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "8"
                id: n8
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "9"
                id: n9
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "*"
                id: X
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "4"
                id: n4
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "5"
                id: n5
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "6"
                id: n6
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "-"
                id: subs
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "1"
                id: n1
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "2"
                id: n2
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "3"
                id: n3
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "+"
                id: plus
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "("
                id: parenthesis
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.addparenthesis(self.text)
                
            Button:
                text: "0"
                id: n0
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                text: "."
                id: dot
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.signs(self.text)
            Button:
                id: equality
                text: "="
                size_hint: 1/4,1/5
                font_size: "40sp"
                on_press: root.compute()
                

"""


class CustumBox(BoxLayout):
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
                self.ids.lbl.text += value
                self.ids.AC.text = "C"
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


class CalculatorApp(App):
    def build(self):
        return Builder.load_string(KV)


CalculatorApp().run()

