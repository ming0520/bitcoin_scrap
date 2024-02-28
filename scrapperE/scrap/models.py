from django.db import models
from django.utils import timezone

# Create your models here.

class PostRaw(models.Model):
    post_id = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    raw_text = models.TextField()
    created_at = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True)
    platform_source = models.CharField(max_length=10)
    post_url = models.URLField()
    author_name = models.CharField(max_length=300)
    author_id = models.CharField(max_length=50)
    post_score = models.IntegerField()
    status = models.CharField(default='PENDING',max_length=10)

    def __str__(self):
        return self.title
    
class CommentRaw(models.Model):
    comment_id = models.CharField(max_length=50)
    post_id = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True)
    comment_url = models.URLField()
    comment_score = models.IntegerField()
    comment_body = models.TextField()
    author_name = models.CharField(max_length=100)
    author_id = models.CharField(max_length=50)
    status = models.CharField(default='PENDING',max_length=10)

    def __str__(self):
        return f"Comment on {self.post.title}"
    
class ErrorPost(models.Model):
    post_id = models.CharField(max_length=50)
    error_message = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_id
    
class BitstampData(models.Model):
    unix = models.IntegerField()
    date = models.DateTimeField()
    local_date = models.DateTimeField(default=timezone.now)
    symbol = models.CharField(max_length=50)
    open = models.DecimalField(max_digits=20, decimal_places=10)
    high = models.DecimalField(max_digits=20, decimal_places=10)
    low = models.DecimalField(max_digits=20, decimal_places=10)
    close = models.DecimalField(max_digits=20, decimal_places=10)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=10)
    volume_usd = models.DecimalField(max_digits=20, decimal_places=10)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.date}"
    
class BitstampDataHour(models.Model):
    unix = models.IntegerField()
    date = models.DateTimeField()
    local_date = models.DateTimeField(default=timezone.now)
    symbol = models.CharField(max_length=50)
    open = models.DecimalField(max_digits=20, decimal_places=10)
    high = models.DecimalField(max_digits=20, decimal_places=10)
    low = models.DecimalField(max_digits=20, decimal_places=10)
    close = models.DecimalField(max_digits=20, decimal_places=10)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=10)
    volume_usd = models.DecimalField(max_digits=20, decimal_places=10)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.date}"
    
class BitstampDataMinute(models.Model):
    unix = models.IntegerField()
    date = models.DateTimeField()
    local_date = models.DateTimeField(default=timezone.now)
    symbol = models.CharField(max_length=50)
    open = models.DecimalField(max_digits=20, decimal_places=10)
    high = models.DecimalField(max_digits=20, decimal_places=10)
    low = models.DecimalField(max_digits=20, decimal_places=10)
    close = models.DecimalField(max_digits=20, decimal_places=10)
    volume_btc = models.DecimalField(max_digits=20, decimal_places=10)
    volume_usd = models.DecimalField(max_digits=20, decimal_places=10)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.date}"


class ErrorLog(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    error_source = models.CharField(max_length=200)
    error_type = models.CharField(max_length=200)
    error_content = models.TextField()
    error_message = models.TextField()

    def __str__(self):
        return self.post_id