from django.db import models
from django.contrib.auth.models import User



# Create your models here.
# Table to store user interests with companies
class UserInterest(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the ID field
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

# Table to store article data
class ArticleData(models.Model):
    interest = models.ForeignKey(UserInterest, on_delete=models.CASCADE)
    link = models.URLField(max_length=500)
    date = models.DateField()
    text = models.TextField()
    source = models.CharField(max_length=50)  # New field to store the API name

    def __str__(self):
        return f"Article for {self.interest.company_name} on {self.date} from {self.source}"