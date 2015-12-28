from django.db import models

##class Stream(models.Model):
##    name = models.CharField(max_length=3, unique= True)
##
##    def __unicode__(self):
##		return self.id

class StudyStream(models.Model):
    name = models.CharField(max_length=3, unique= True)

    def __unicode__(self):
		return self.name
        
