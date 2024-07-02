from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Movies(models.Model):
    owner = models.ForeignKey(Profile, null= True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=5000, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    trailer_link = models.CharField(max_length=3000, null=True, blank=True)
    source_link = models.CharField(max_length=3000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('tags')
    vote_total= models.IntegerField(default=0, null=True, blank=True)
    vote_ratio= models.IntegerField(default=0, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    

    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='Up').count()
        totalVotes = reviews.count()

        print(f"Total reviews: {reviews}")
        print(f"Up votes: {upVotes}")
        print(f"Total votes: {totalVotes}")

        ratio = (upVotes / totalVotes) * 100

        print(f"Vote ratio: {ratio}%")

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

        print(f"Saved vote_total: {self.vote_total}, vote_ratio: {self.vote_ratio}")



class Review(models.Model):
    VOTE_TYPE= (
        ('Up', 'Up Vote'),
        ('Down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    body = models.TextField(max_length=5000, null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'movie']]

    def __str__(self):
        return self.value

class Tags(models.Model):
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name



