import json
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

kv = """
<CustomScreen@Screen>:
    canvas:
        Color:
            rgba: 255, 255, 255, 1
        Rectangle:
            pos: self.pos
            size: self.size
       
           

CustomScreen:
    id: mainsccreen
    GridLayout:
        rows: 4
        cols: 2
        Label: 
            text: "UserName"
            color: "black"
        TextInput:
            id: username
            text: ""
            on_text: root.on_property_changed()
        Label: 
            text: "IP Address"
            text: ""
            color: "black"
        TextInput:
            id: ip
            text: ""
            on_text: root.on_property_changed()
        Label:
            text: "PORT"
            color: "black"
        TextInput:
            id: port
            text: ""
            on_text: root.on_property_changed()
           
        Button:
            text: "Save Config"
            on_press: root.save()
        Button: 
            id: btn
            text: "Continue"      
            
"""


class CustomScreen(Screen):
    data = dict()

    def on_property_changed(self):
        if self.ids.username.text == "" or self.ids.ip.text == "" or self.ids.port.text == "":
            self.ids.btn.disabled = True
        else:
            self.ids.btn.disabled = False

    def save(self):
        print(type(self.ids.username.text))
        self.data["Username"] = self.ids.username.text
        self.data["Ip"] = self.ids.ip.text
        self.data["Port"] = self.ids.port.text
        # Serializing json
        json_object = json.dumps(self.data)
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
            print("Saved...")


class TestJsonApp(App):
    data = {'Username': '', 'Ip': '', 'Port': ''}

    def build(self):
        if os.path.exists("sample.json"):
            with open('sample.json') as f:
                self.data = json.load(f)

        box = Builder.load_string(kv)
        box.ids.username.text = self.data["Username"]
        box.ids.ip.text = self.data["Ip"]
        box.ids.port.text = self.data["Port"]
        return box


if __name__ == "__main__":
    TestJsonApp().run()
