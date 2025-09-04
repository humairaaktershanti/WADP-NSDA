from django.db import models

class universitylist(models.Model):
    universityname= models.CharField(max_length=100)
    universityid= models.CharField(max_length=100)
    universityaddress= models.CharField(max_length=100)
    
    def __str__(self):
        return self.universityname +"-"+self.universityid
    
class badUniversity(models.Model):
    baduniversityname = models.CharField(max_length=100)
    baduniversityid = models.CharField(max_length=100)
    baduniversityaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.baduniversityname +"-"+ self.baduniversityid
    

class goodUniversity(models.Model):
    gooduniversityname = models.CharField(max_length=100)
    gooduniversityid = models.CharField(max_length=100)
    gooduniversityaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.gooduniversityname +"-"+ self.gooduniversityid

class universityStudent(models.Model):
    universitystudentname = models.CharField(max_length=100)
    universitystudentid = models.CharField(max_length=100)
    universitystudentaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.universitystudentname +"-"+ self.universitystudentid

class internationalUniversiy(models.Model):
    internationaluniversityname = models.CharField(max_length=100)
    internationaluniversityid = models.CharField(max_length=100)
    internationaluniversityaddress = models.CharField(max_length=100)
    
    def __str__(self):
        return self.internationaluniversityname +"-"+ self.internationaluniversityid

    
