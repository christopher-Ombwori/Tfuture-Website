from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    icon_svg = models.TextField(blank=True)  # Store the full SVG icon
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)  # For the main hero service card
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})

class Project(models.Model):
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('brand-identity', 'Brand & Visual Identity'),
        ('communication-kits', 'Company Communication Kits'),
        ('events', 'Events Experience'),
        ('rollouts', 'Rollouts & Merchandise'),
    ])
    subcategory = models.CharField(max_length=50, choices=[
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
    ], null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Categories that require subcategory
        categories_requiring_subcategory = ['brand-identity', 'communication-kits']
        
        if self.category in categories_requiring_subcategory:
            if not self.subcategory:
                raise ValidationError({
                    'subcategory': f'Subcategory is required for {self.get_category_display()} projects.'
                })
        else:
            # Prevent subcategory for categories that don't support it
            if self.subcategory:
                raise ValidationError({
                    'subcategory': f'{self.get_category_display()} projects do not accept subcategories. Please remove the subcategory selection.'
                })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Run validation before saving
        self.full_clean()
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

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('contacted', 'Contacted'),
        ('completed', 'Completed'),
        ('spam', 'Spam'),
        ('cancelled', 'Cancelled'),
    ]
    
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='requests')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True, help_text='Internal notes for this request')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name} ({self.get_status_display()})"
