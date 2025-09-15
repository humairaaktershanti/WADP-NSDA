from django.db import models

class computerlist(models.Model):
    computername= models.CharField(max_length=100)
    computerid= models.CharField(max_length=100)
    computeraddress= models.CharField(max_length=100)
    
    def __str__(self):
        return self.computername +"-"+self.computerid
    
class badcomputer(models.Model):
    badcomputername = models.CharField(max_length=100)
    badcomputerid = models.CharField(max_length=100)
    badcomputeraddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.badcomputername +"-"+ self.badcomputerid

class goodcomputer(models.Model):
    goodcomputername = models.CharField(max_length=100)
    goodcomputerid = models.CharField(max_length=100)
    goodcomputeraddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.goodcomputername +"-"+ self.goodcomputerid

class internationalcomputer(models.Model):
    internationalcomputername = models.CharField(max_length=100)
    internationalcomputerid = models.CharField(max_length=100)
    internationalcomputeraddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.internationalcomputername +"-"+ self.internationalcomputerid

class blogcomputer(models.Model):
    blogcomputertitle = models.CharField(max_length=100)
    blogcomputerid = models.CharField(max_length=100)
    blogcomputerdetails = models.CharField(max_length=100)
    
    def __str__(self):
        return self.blogcomputertitle +"-"+ self.blogcomputerid