from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('brand-identity', 'Brand & Visual Identity'),
        ('communication-kits', 'Company Communication Kits'),
        ('events', 'Events Experience'),
        ('rollouts', 'Rollouts & Merchandise'),
    ]

    SUBCATEGORY_CHOICES = [
        # Brand & Visual Identity subcategories
        ('full-brand', 'Full Brand Identity'),
        ('visual-identity', 'Visual Identity'),
        ('logofolio', 'Logofolio'),
        # Company Communication Kits subcategories
        ('company-profiles', 'Company Profiles'),
        ('presentations', 'Presentations'),
        ('internal-coms', 'Internal Coms & SOPs'),
        ('stationery', 'Stationery'),
        ('social-media', 'Social Media Kits'),
    ]

    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Validate subcategory based on category
        if self.category in ['brand-identity', 'communication-kits']:
            if not self.subcategory:
                raise ValueError(f"Subcategory is required for {self.get_category_display()}")
        else:
            self.subcategory = None  # Clear subcategory for other categories
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')
    order = models.PositiveIntegerField(default=0)
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"
