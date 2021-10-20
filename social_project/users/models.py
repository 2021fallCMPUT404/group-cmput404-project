from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class username(models.Model):
    username = models.CharField(max_length = 32, unique = True)

    def __str__(self):
        return self.username

class user_profile(models.Model):
    user = models.ForeignKey(username, on_delete=models.DO_NOTHING)
    bio = models.CharField(max_length = 256, unique = False)
    url = models.URLField(unique = True)
    profile_picture = models.ImageField(upload_to = user_directory_path)

    def __str__(self):
        return self.bio

class edit_history(models.Model):
    name = models.ForeignKey(user_profile, on_delete=models.DO_NOTHING)
    edit_date = models.DateField()

    def __str__(self):
        return self.edit_date