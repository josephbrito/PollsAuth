from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.username

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text