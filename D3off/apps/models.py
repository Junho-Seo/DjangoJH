from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    isDone = models.BooleanField()

    # 자동으로 호출되는 메서드(매직 메서드)
    # __str__: print 할 때 자동으로 호출되는 매직 메서드
    def __str__(self):
        return self.title