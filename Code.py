from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
import datetime

class Next_Class:
    def __init__(self,i,p):
        self.date_obj=datetime.datetime.now()
        self.connected=False
        self.id=i
        self.pwd=p
        self.req()



    def req(self):
        s=Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=s,options=options)

        driver.get("https://ent.univ-paris13.fr/")

        inputs=driver.find_elements(By.TAG_NAME,"input")

        inputs[0].send_keys(self.id)
        inputs[1].send_keys(self.pwd)

        driver.find_element(By.ID,"submit").click()
        driver.get("https://ent.univ-paris13.fr/applications/emploidutemps/")


        soup = BeautifulSoup(driver.page_source,"html.parser")

        driver.close()
        driver.quit()

        div=soup.find("div",{"id":"CalendarCreation"})
        if (div ==None):
            print("Erreur de connexion veuillez Réessayer")
        else:
            self.connected=True
            a=div.find("script").text
            b=a.split("[")

            self.obj=b[3][3:].replace("\t\t],\n\t\teventClick: function(info) {\n\t\t\taJourTexte = ","").split(",\n")

            for ui in self.obj:
                self.obj[self.obj.index(ui)] = json.loads(ui.replace("title","\"title\"").replace("start","\"start\"").replace("end","\"end\""))

            print("Vous êtes connecté")

    def Launch(self):
        if self.connected:
            a=self.date_obj
            L=[]
            verif_date=f"{a.year}-{str(a.month).zfill(2)}-{str(a.day).zfill(2)}"
            verif_time=f"{str(a.hour).zfill(2)}:{str(a.minute).zfill(2)}:00"
            for ui in obj:
                # print(ui["start"])
                if verif_date in ui["start"]:
                    L.append(ui)
            nn=[]
            if L != []:
                nn= sorted(L, key=lambda d: d['start'].split("T")[1])
                for ui in nn:
                    if ui["start"].split("T")[1]>verif_time:
                        return ui
                nn=[]
                if nn==[]:
                    tom=a+datetime.timedelta(days=1)
                    tom=tom.replace(hour=3)
                    return self.Launch(tom)
            else:
                tom=a+datetime.timedelta(days=1)
                tom=tom.replace(hour=3)
                return self.Launch(tom)
        else:
            print("Vous n'êtes pas connecté")
            return Falses





#Exemple

a=Next_Class("id","pwd")
Next_Class_obj = a.Launch()
