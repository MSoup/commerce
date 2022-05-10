from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    wishlist = models.ManyToManyField("Listing", blank=True, related_name="users")

    def __str__(self):
        return self.username

class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return self.tag

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    max_bid = models.DecimalField(default=0,decimal_places=2, max_digits=5)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    tag = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.jpeg', null=True, blank=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(decimal_places=2, max_digits=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} bid {self.price} for {self.listing}'

class Comment(models.Model):
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'ON {self.listing}: {self.id}: {self.comment}'

