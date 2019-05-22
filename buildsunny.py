# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import re
import sqlite3
import random

#import GUI and database
Ui_MainWindow, QtBaseClass = uic.loadUiType("buildsunny.ui")
conn = sqlite3.connect('buildsunny.sqlite')
c = conn.cursor()
#create main class
class MainWindow(QMainWindow):

    #base def
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Fill boxes
        self.ui.continent.addItems(self.unique([nom[0] for nom in c.execute("SELECT Continent FROM SunnyData_zones")])) #Fill continent box
        self.ui.getregion.clicked.connect(self.checkregion) #Fill region box
        self.ui.getzone.clicked.connect(self.checkzone) #Fill zone box
        self.ui.go.clicked.connect(self.maketext) #Go button effect

    def unique(self,seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def checkregion(self):
        self.ui.region.clear()
        c.execute('SELECT Region FROM SunnyData_zones WHERE Continent=?',(self.ui.continent.currentText(),))
        reg = c.fetchall()
        reg2=self.unique(reg)
        for r in reg2:
            self.ui.region.addItem(r[0])

    def checkzone(self):
        self.ui.zone.clear()
        c.execute('SELECT Zone FROM SunnyData_zones WHERE Region=?',(self.ui.region.currentText(),))
        zone = c.fetchall()
        zone2=self.unique(zone)
        for z in zone2:
            self.ui.zone.addItem(z[0])

    def maketext(self):
        self.ui.output.setPlainText('')
        c.execute('SELECT * FROM SunnyData_zones WHERE Region=? AND Zone=?',(self.ui.region.currentText(),self.ui.zone.currentText()))
        zonedata = c.fetchone()
        if zonedata==None:
            msgBox1 = QMessageBox()
            msgBox1.setText('Noms inconnus')
            msgBox1.exec_()
        else:
            self.ui.output.appendPlainText("<div class='form_fond'><div class='secondlayer'><div class='form_titre_bg2'><div class='form_titredescri'><div class='form_titre_bg'>[size=12].: "+zonedata[3]+" :.[/size]</div></div></div>")
            if zonedata[7]!=None:
                self.ui.output.appendPlainText("<div class='soustitredescri'>[url="+zonedata[7]+"]Carte de la région[/url]</div>")
            if zonedata[5]==None:
                self.ui.output.appendPlainText("<div class='form_boite'><div class='form_boite_bg'>[i]\n"+"Description à faire !"+"[/i]")
            else:
                if zonedata[4]==None:
                    self.ui.output.appendPlainText("<div class='form_boite'><div class='form_boite_bg'>[i]\n"+zonedata[5]+"\n[/i]")
                else:
                    self.ui.output.appendPlainText("<div class='form_boite'><div class='form_boite_bg'>[center]"+zonedata[4]+"[/center]\n[i]"+zonedata[5]+"\n[/i]")

            if zonedata[6]=="Oui":
                places = ()
                c.execute('SELECT * FROM SunnyData_pokemon WHERE Zone=?',(zonedata[0],))
                for subzone in c.fetchall():
                    places = places + (subzone[5],)
                places2=self.unique(places)
                self.ui.output.appendPlainText("[center]")
                for thing in list(range(0,len(places2))):
                    c.execute('SELECT Level FROM SunnyData_pokemon WHERE Zone=? AND Place=?',(zonedata[0],places2[thing],))
                    lvl=c.fetchone()[0]
                    self.ui.output.appendPlainText("[b][u]"+places2[thing]+" :[/u][/b]")
                    self.ui.output.appendPlainText("[i][Niveau "+lvl+"][/i]\n")
                    rarity = ()
                    c.execute('SELECT * FROM SunnyData_pokemon WHERE Zone=? AND Place=?',(zonedata[0],places2[thing]))
                    for x in c.fetchall():
                        rarity = rarity + (x[3],)
                    rarity2 = self.unique(rarity)

                    for r in list(range(0,len(rarity2))):
                        if rarity2[r]!="Courant":
                            self.ui.output.appendPlainText("[b]"+rarity2[r]+" :[/b]\n")
                        c.execute('SELECT Pokemon,Pokemon_id FROM SunnyData_pokemon WHERE Zone=? AND Place=? AND Rarity=?',(zonedata[0],places2[thing],rarity2[r]))
                        for pokemon in c.fetchall():
                            self.ui.output.insertPlainText("[url=https://www.pokebip.com/pokedex/pokemon/"+str(pokemon[0])+"][img]http://sunrise-db.yo.fr/Sprites/"+str(pokemon[1])+".png[/img][/url]")
                self.ui.output.appendPlainText("[/center]\n</div></div>\n</div></div>")
            else:
                self.ui.output.appendPlainText("</div></div>\n</div></div>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
