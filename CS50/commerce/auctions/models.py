from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    categoryName = models.CharField(max_length=256)

    def __str__(self):
        """
        We define this so we can see category name in the table, instead of Category 1, Category 2...
        """
        return self.categoryName


class Listing(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    starting_bid = models.FloatField(default=0.0)
    image_url = models.URLField(
        blank=True
    )  # If True, the field is allowed to be blank. Default is False
    is_active = models.BooleanField(default=True)
    # Set Listing Category to null if Category is deleted

    # Copied from stackoverflow: related_name will be the attribute of the related object that allows you to go 'backwards'
    # to the model with the foreign key on it.
    # For example, if ModelA has a field like: model_b = ForeignKeyField(ModelB, related_name='model_as'),
    # this would enable you to access the ModelA instances that are related to your ModelB instance
    # by going model_b_instance.model_as.all().
    # Note that this is generally written with a plural for a Foreign Key,
    # because a foreign key is a one to many relationship, and the many side of that
    # equation is the model with the Foreign Key field declared on it.
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )
    # Delete Listing if user is deleted
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    usersWatching = models.ManyToManyField(User, related_name="watchedListings")

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField(blank=False)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    commentor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    date = models.DateField()

    class Meta:
        ordering = ["-date"]  # order by descending date


class Bids(models.Model):
    bid = models.FloatField(default=0.0)

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    class Meta:
        ordering = ["-bid"]  # order by descending bids
