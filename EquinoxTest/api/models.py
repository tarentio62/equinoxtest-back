from django.db import models

class Test(models.Model):

    titre = models.CharField(max_length=250)
    json = models.TextField()
    pyUrl = models.CharField(max_length=500)
    dateCreation = models.DateTimeField(auto_now_add=True)
    dateModification = models.DateTimeField(auto_now=True)
    urlDepart = models.CharField(max_length=500)
    etapes = []
    def loadFromRecord(self,dataJson):
        if dataJson is not None:
           self.urlDepart = dataJson['startUrl']
           self.json=dataJson
           self.titre = dataJson['title']


class Etape(models.Model):

    cible = models.CharField(max_length=500)
    commande = models.CharField(max_length=50)
    valeur = models.TextField()
    sequence = models.IntegerField()
    test = models.ForeignKey(Test)

    def loadFromRecord(self,test,dataJson):
        if dataJson is not None:
            self.cible = dataJson['target']          
            self.commande = dataJson['command']
            self.sequence = dataJson['sequence']
            self.valeur = dataJson['value']
            self.test = test

class TestHistorique(models.Model):

    resultat = models.BooleanField(default=False)
    tempsExecution = models.DurationField()
    dateExecution = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test)


class EtapeHistorique(models.Model):

    resultat = models.CharField(max_length=250)
    dateExecution = models.DateTimeField(auto_now=True)
    tempsExecution = models.DurationField()