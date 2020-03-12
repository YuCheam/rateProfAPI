from django.db import models

class Professor(models.Model):
    
    fname = models.CharField(max_length=40)
    lname = models.CharField(max_length=40)
    prof_id = models.CharField(max_length=3, primary_key=True, default='0')

    
    def __str__(self):
        return self.fname + " " + self.lname

class Module(models.Model):
    moduleCode = models.CharField(max_length = 3)
    name = models.CharField(max_length = 40)

    def __str__(self):
        return self.name

class moduleInstance(models.Model):
    class Semester(models.IntegerChoices):
        One = 1
        Two = 2
    
    semester = models.IntegerField(choices=Semester.choices)
    year = models.CharField(max_length = 4)
    professor = models.ManyToManyField(Professor)
    module = models.ForeignKey('Module', on_delete = models.CASCADE)

    def __str__(self):
        return '%s %s, semester: %d' % (self.module.name, self.year, self.semester)
    

class User(models.Model):
    userName = models.CharField(max_length = 15, unique = True)
    password = models.CharField(max_length = 15)
    email = models.CharField(max_length = 40, unique = True)

    def __str__(self):
        return self.userName

class Rating(models.Model):
    userID = models.ForeignKey('User', on_delete=models.CASCADE)
    moduleID = models.ForeignKey('moduleInstance', on_delete=models.CASCADE)
    profID = models.ForeignKey('Professor', on_delete=models.CASCADE)
    rating = models.IntegerField()

    
                    
    
