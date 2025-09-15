from django.db import models

class progrmmingList(models.Model):
    programmingname=models.CharField(max_length=100)
    programmingid=models.CharField(max_length=100)
    programmingcategory=models.CharField(max_length=100)

    def __str__(self):
        return self.programmingname +"-"+ self.programmingid

class popularProgramming(models.Model):
    popularprogramname=models.CharField(max_length=100)
    popularprogramid=models.CharField(max_length=100)
    popularprogramcountry=models.CharField(max_length=100)

    def __str__(self):
        return self.popularprogramname +"-"+ self.popularprogramid
    
class frontendProgramming(models.Model):
    frontendprogramname=models.CharField(max_length=100)
    frontendprogramid=models.CharField(max_length=100)
    frontendpopularcountry=models.CharField(max_length=100)

    def __str__(self):
        return self.frontendprogramname +"-"+ self.frontendprogramid

class badProgramming(models.Model):
    badprogramname=models.CharField(max_length=100)
    badprogramid=models.CharField(max_length=100)

    def __str__(self):
        return self.badprogramname +"-"+ self.badprogramid

class backendProgramming(models.Model):
    backendprogramname=models.CharField(max_length=100)
    backendprogramid=models.CharField(max_length=100)
    backendpopularcountry=models.CharField(max_length=100)

    def __str__(self):
        return self.backendprogramname +"-"+ self.backendprogramid
    