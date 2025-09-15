from django.db import models

class newslist(models.Model):
    newsname= models.CharField(max_length=100)
    newsid= models.CharField(max_length=100)
    newsaddress= models.CharField(max_length=100)
    
    def __str__(self):
        return self.newsname +"-"+self.newsid
    
class badNews(models.Model):
    badnewsname = models.CharField(max_length=100)
    badnewsid = models.CharField(max_length=100)
    badnewsaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.badnewsname +"-"+ self.badnewsid

class goodNews(models.Model):
    goodnewsname = models.CharField(max_length=100)
    goodnewsid = models.CharField(max_length=100)
    goodnewsaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.goodnewsname +"-"+ self.goodnewsid

class internationalNews(models.Model):
    internationalnewsname = models.CharField(max_length=100)
    internationalnewsid = models.CharField(max_length=100)
    internationalnewsaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.internationalnewsname +"-"+ self.internationalnewsid

class blogNews(models.Model):
    blognewstitle = models.CharField(max_length=100)
    blognewsid = models.CharField(max_length=100)
    blognewsdetails = models.CharField(max_length=100)
    
    def __str__(self):
        return self.blognewstitle +"-"+ self.blognewsid