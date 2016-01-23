"""
Gokomu.
Kahden pelaajan ristinolla, tarkoituksena saada 5 suora.
https://en.wikipedia.org/wiki/Gomoku
"""

from tkinter import *
from tkinter.messagebox import showerror

class Laudankoko():
    def __init__(self):
        self.onnistuiko = False
        # Alustetaan ikkuna
        self.__ikkuna = Tk()

        # alustetaan kentät
        self.__ikkuna.title("Laudan määrittäminen")
        self.__kysymyslabel = Label(self.__ikkuna,
                                    text = "Kuinka suuri lauta tehdään?")
        self.__suuruusentry = Entry(self.__ikkuna)
        self.__okbutton = Button(self.__ikkuna,
                                 text="Ok", command= self.ota_koko)

        # alustetaan entry teksti
        self.__suuruusentry.insert(0,"20")

        # paikat
        self.__kysymyslabel.grid(row=0,column=0)
        self.__suuruusentry.grid(row=1,column=0)
        self.__okbutton.grid(row=2,column=0)

        # pikanäppäimet
        self.__suuruusentry.bind("<Return>",self.ota_koko)

        self.__ikkuna.mainloop()

    def ota_koko(self,event=""):
        """
        Ottaa entrystä koon vastaan, ja palauttaa sen pääohjelmalle
        :param event: pikanäppäimelle
        """
        #testaus
        try:
            # koko muuttuja joka palautetaan pää ohjelmalle
            self.koko = int(self.__suuruusentry.get())

            if self.koko in range(10,36):
                self.__ikkuna.destroy()
                self.onnistuiko = True
            else: raise
        except:
            # error ponnahdus
             showerror("VIRHE!","Virheellinen laudankoko! (Anna kokonaislukuna"
                                " väliltä 10-35)")

class Ristinolla():
    def __init__(self,koko):
        # Pääikkuna
        self.__pääikkuna = Tk()
        self.__pääikkuna.title("Ristinolla")

        # Muuttujia
        self.__laudankoko = koko
        self.__vuorolaskuri = 0
        self.__pelaaja = 1

        # Labelien luonti
        self.__tilannelabel = Label(self.__pääikkuna,text="Pelaajan {} vuoro"
                                    .format(self.__pelaaja))
        self.__vuorolaskurilabel = Label(self.__pääikkuna,text=
                            "{}. siirtoa tehty".format(self.__vuorolaskuri))

        # Labelien asettaminen
        self.__tilannelabel.grid(row=0,column=0,columnspan=4)
        self.__vuorolaskurilabel.grid(row=0,column=4,columnspan=4)

        # Pelilaudan luonti
        # Pelilauta on koostuu y suuntaa kuvaavasta listasta ja x suuntaa
        # kuvaavasta lsitasta, missä x listassa on nappuloita.
        self.__pelilauta = []
        for kokox in range(self.__laudankoko):
            self.__lautax = []
            for kokoy in range(self.__laudankoko):
                # Nappula luodaan
                merkkibutton = Button(self.__pääikkuna,width=2,height=1,
                                      command =(lambda y=kokoy,x=kokox:
                                                self.tee_vuoro(x,y)))
                # Nappula sijoitetaan ikkunaan
                merkkibutton.grid(row=kokoy+1,column=kokox,sticky =N+W+E+S)
                # Nappula tallennetaan x suuntaa kuvaavaan listaan
                self.__lautax.append(merkkibutton)
            self.__pelilauta.append(self.__lautax)

        self.__pääikkuna.mainloop()

    def tee_vuoro(self,x,y):
        """
        funktio suorittaa vuoro toimenpiteet eli laittaa nappiin X, tai O
        lukitsee napin ja antaa tietoa eteenpäin
        :param x: nappulan x koordinaatti
        :param y: nappulan y koordinaatti
        :return:
        """
        #suorittaa pelaajan 1 vuoron
        if self.__pelaaja == 1:
            self.__pelilauta[x][y].config(state = DISABLED,
                                          background="lightblue",text="X")
            # tarkistaa voittoa ja sen löytyessä lopettaa seuraavat vaiheet
            if self.voitontarkistu("lightblue",[x,y]): return
        # suorittaa pelaajan 2 vuoron
        elif self.__pelaaja == 2:
            self.__pelilauta[x][y].config(state = DISABLED,
                                          background="lightcoral",text="O")
            if self.voitontarkistu("lightcoral",[x,y]): return
        # päivittää nappulan näytölle
        self.__pelilauta[x][y].update()
        self.päätä_vuoro()

    def päätä_vuoro(self):
        """
        Funktio päivittää labeleiden tekstit vuorossa olevan pelaajan ja vuoron
        """
        self.__vuorolaskuri += 1
        # päivittää pelaajan
        self.__pelaaja %=2
        self.__pelaaja += 1
        self.__tilannelabel["text"] = "Pelaajan {} vuoro".format\
            (self.__pelaaja)
        self.__vuorolaskurilabel["text"]= "{}. siirtoa tehty".format\
            (self.__vuorolaskuri)
        self.__vuorolaskurilabel.update()

    def voitontarkistu(self,merkki,koordinaatti):
        """
        Funktio tarkistaa ratkaiseeko siirto pelin. Funktio antaa neljä
        vektoria: ylös oikea ja yläviistot eteenpäin seuraaville funktioille
        pohdittavaksi
        :param merkki: ruudun väri
        :param koordinaatti: lista missä koordinaatti
        :return: True jos voittaja löytyi
        """
        # jos mahdollista löytää  voittaja
        if self.__vuorolaskuri >= 8:
            # vektorit sivulle ja viistoon
            vek1=(1,0)
            vek2=(1,1)

            for suunta in range(2):
                if True == self.tarkista(merkki,vek1,koordinaatti):
                    self.voitonjulistus()
                    return True
                if True == self.tarkista(merkki,vek2,koordinaatti):
                    self.voitonjulistus()
                    return True

                # Vektorit käännetään osoittamaan eri suuntiin
                vek1 = -vek1[1], vek1[0]
                vek2 = -vek2[1], vek2[0]

        # tarkistaa tasapelin
        if self.__vuorolaskuri+1 == self.__laudankoko**2:
            self.__vuorolaskurilabel["text"] = "Tasapeli!"
            self.__tilannelabel["text"] = ""
            self.__tilannelabel.update()
            self.__vuorolaskurilabel.update()
            showerror("Tasapeli","tasapeli!")
            return True

    def tarkista(self, merkki,vektori ,koord):
        """
        Tarkista funktio ottaa vektorin ja tekee sille vasta vektorin.
        Antaa suuntafunktiolle vektorin ja sen vastavektorin joka sitten
        palauttaa osumien määrän. Jos osumia on riittävästi niin palauttaa True
        :param merkki: ruudun väri
        :param vektori: suunta vektori mitä mikä annetaan eteenpäin
        :param koord: napin koordinaatti
        :return: True jos löytyi 5 suora.
        """
        vastavektori = -vektori[0], -vektori[1]
        # lätee liikkumaan vektorin suuntaan, osumia 1.
        osumia = self.suunta(merkki,vektori,1,koord)
        if osumia == 5:
            return True
        # päähän tultuaan palaa aloituspisteeseen ja lähtee laskemaan eri
        # suuntaan, osumia tälläkertaa ensimmäisestä suunnasta löytynyt määrä
        osumia = self.suunta(merkki,vastavektori,osumia,koord)
        if osumia == 5:
            return True

    def suunta(self, merkki, vektori, osumia,koord):
        """
        Suunta funktio laskee vektorin suunnassa samanväristen nappuloiden
        määrän.
        :param merkki: napin väri
        :param vektori: suunta vektori
        :param osumia:  osumien määrä
        :param koord: napin koordinaatti
        :return:
        """
        try:
            # vektorin päässä oleva nappi
            uusix = koord[0]+vektori[0]
            uusiy = koord[1]+vektori[1]
            uusikoord = [uusix,uusiy]
            # tarkistetaan merkki ja tallennetaan se uutena merkkinä
            if self.__pelilauta[uusix][uusiy]["background"] == "lightcoral":
                uusimerkki = "lightcoral"

            elif self.__pelilauta[uusix][uusiy]["background"] == "lightblue":
                uusimerkki = "lightblue"

            else: uusimerkki = "tyhjä"

            # Jos vektorin päässä oleva merkki on annettua vastaava
            # niin lisätään osumiin 1 ja jatketaan seuraavaan koordinaattiin
            if uusimerkki == merkki:
                osumia = self.suunta(uusimerkki, vektori, osumia+1 ,uusikoord)
            # palautetaan osumat
            return osumia
        except IndexError:
            # jos vektorin pää on listan ulkona niin palautetaan osumat
            return osumia

    def voitonjulistus(self):
        """
        Funktion tarkoitus popata voitto julistus muuttaa labeleiden tekstit.
        Voittaja kunniaan
        """
        # Labelien määritys
        self.__vuorolaskurilabel["text"] = "Pelaaja {} voitti!".format\
            (self.__pelaaja)
        self.__tilannelabel["text"] = ""
        self.__tilannelabel.update()

        # Napit poistetaan käytöstä, peli loppui.
        for xnapit in range(len(self.__pelilauta)):
            for ynapit in range(len(self.__pelilauta)):
                self.__pelilauta[xnapit][ynapit].config(state=DISABLED)
        self.__vuorolaskurilabel.update()

        # popataan voittajan julistus
        showerror("Voittaja","Pelaaja {} voitti pelin!".format
        (self.__pelaaja))

def main():
    laudan_koko = Laudankoko()
    # Tämän ansiosta ei voi pelata sallittua laudankokoa suurempaa lautaa
    if laudan_koko.onnistuiko == True:
        Ristinolla(laudan_koko.koko)

main()