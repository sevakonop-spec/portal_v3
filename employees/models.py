from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
    )
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.full_path()

    def full_path(self):
        if self.parent:
            return f'{self.parent.full_path()} / {self.name}'
        return self.name

    def get_ancestors(self):
        ancestors = []
        node = self.parent
        while node:
            ancestors.insert(0, node)
            node = node.parent
        return ancestors

    def get_depth(self):
        depth = 0
        node = self.parent
        while node:
            depth += 1
            node = node.parent
        return depth


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(
        Department, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='employees',
    )
    job_title = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def display_name(self):
        return self.user.get_full_name() or self.user.username

    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None