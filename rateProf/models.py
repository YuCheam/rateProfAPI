from django.db import models

class Professor(models.Model):
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    def __str__(self):
        return self.fname + " " + self.lname

class Module(models.Model):
    class Semester(models.IntegerChoices):
        FALL = 1
        SPRING = 2
    
    semester = models.IntegerField(choices=Semester.choices)
    moduleCode = models.CharField(max_length = 3)
    name = models.CharField(max_length = 40)
    year = models.CharField(max_length = 4)

    def __str__(self):
        return '%s %s, semester: %d' % (self.moduleCode, self.year, self.semester)

class Prof_Module(models.Model):
    profID = models.ManyToManyField(Professor)
    moduleID = models.ManyToManyField(Module)


class User(models.Model):
    userName = models.CharField(max_length = 15, unique = True)
    password = models.CharField(max_length = 15)
    email = models.CharField(max_length = 40, unique = True)

    def __str__(self):
        return self.userName

class Rating(models.Model):
    userID = models.ForeignKey('User', on_delete=models.CASCADE)
    moduleID = models.ForeignKey('Module', on_delete=models.CASCADE)
    profID = models.ForeignKey('Professor', on_delete=models.CASCADE)
    rating = models.IntegerField()

    
                    
    
