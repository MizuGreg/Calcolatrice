"""
A simple calculator. Supports the main four operations,  plus the use of unlimited brackets.
Fase 1: creare l'intera interfaccia grafica iniziale, e le due righe. FATTO
Fase 2: collegare i tasti alla riga di input, e l'uguale alla linea di output.
Fase 3: implementare il codice vero e proprio della calcolatrice, cioè quello che crea il file,
lo compila e salva il risultato. FATTO
Fase 4: collegare il codice alle linee di I/O.
Fase 5: rifinire il progetto e predisporre il codice e la GUI all'ampliamento.
"""
from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '1024')

import kivy
kivy.require('1.10.1')
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from py_expression_eval import Parser
parser = Parser()
# from kivy.properties import StringProperty, NumericProperty
# from pathlib import Path
import CalcFunction # CALCULATOR !!!

class CalcolatriceGame(Widget):
    diz_bott = {"log":"log(", "ln":"log(", "e":"E", "sin":"sin(", "cos":"cos(", "tan": "tan(", u"\u03c0":"PI", u"a\u00b2": "^2", u"a\u00b3":"^3", u"a\u207f":"^", u"\u221a":"^0.5", "7":"7", "8":"8", "9":"9", "(":"(", ")":")", "4":"4", "5":"5", "6":"6", u"\u00d7":"*", u"\u00f7":"/", "1":"1", "2":"2", "3":"3", "+":"+", "-":"-", "0":"0", ",":".", u"\u00d710\u207f":"10^("}
    blocchi_cifre = [] # sono i pulsanti premuti, in ordine
    cursore = 0 # indica la posiz. del cursore nella lista blocchi_cifre
    espress = "" # l'input
    ans = "0.0" # l'output
    nest_level = 0

    def __init__(self, **kwargs):
        super(CalcolatriceGame, self).__init__(**kwargs)
    def cursore_blink(self, dt):
        print(CalcolatriceGame.cursore, CalcolatriceGame.espress, CalcolatriceGame.ans)
    def update_input(self, dt):
        espressione = ""
        for blocco in CalcolatriceGame.blocchi_cifre:
            espressione += blocco[1]
        CalcolatriceGame.espress = espressione
        self.ids.riga_input.text = CalcolatriceGame.espress
        self.ids.riga_output.text = CalcolatriceGame.ans
    def update_output(self):
        try:
            CalcolatriceGame.ans = str(parser.parse(CalcolatriceGame.espress).evaluate({}))
        except:
            CalcolatriceGame.ans = "Error :$"
        
    def bott_funz(self, text):
        for key in CalcolatriceGame.diz_bott.keys():
            if text == key:
                value = CalcolatriceGame.diz_bott[text]
                if (CalcolatriceGame.blocchi_cifre != []) and (value[-1] in ["(", "I", "E"]) and (CalcolatriceGame.blocchi_cifre[CalcolatriceGame.cursore-1][1][-1] not in "+*-/("): 
                    CalcolatriceGame.bott_funz(self, u"\u00d7") # aggiunge moltiplicazione ai bottoni speciali
                CalcolatriceGame.blocchi_cifre.append((key, value))
                if value[-1] == "(":
                    CalcolatriceGame.nest_level += 1
                elif value[-1] == ")":
                    CalcolatriceGame.nest_level -= 1
                CalcolatriceGame.cursore += 1
    def shift(self):
        pass
    def sx(self):
        pass
    def dx(self):
        pass
    def delete(self):
        if CalcolatriceGame.cursore > 0:
            CalcolatriceGame.blocchi_cifre.pop(CalcolatriceGame.cursore-1)
            CalcolatriceGame.cursore -= 1

    def ac(self):
        if CalcolatriceGame.blocchi_cifre != []:
            CalcolatriceGame.blocchi_cifre = []
            CalcolatriceGame.cursore = 0
            CalcolatriceGame.nest_level = 0
            CalcolatriceGame.ans = "0"
            CalcolatriceGame.espress = ""

        
class CalcolatriceApp(App):
    def build(self):
        self.root = CalcolatriceGame()
        Clock.schedule_interval(self.root.cursore_blink, 1.75) # dovrà diventare 0.75
        Clock.schedule_interval(self.root.update_input, 0.03)
        return self.root

if __name__ == '__main__':
    CalcolatriceApp().run()