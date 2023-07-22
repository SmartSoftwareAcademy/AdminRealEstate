from django.db import models
from landlords.models import PropertyOwner
from django.urls import reverse
from tinymce.models import HTMLField

class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('commercial', 'Commercial'),
    ]
    PROPERTY_STATUSES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('unavailable', 'Unavailable'),
    ]
    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=255,default='addr')
    city= models.CharField(max_length=255,default='Oyugis')
    country= models.CharField(max_length=255,default='Kenya')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES,default='apartment')
    property_name = models.CharField(max_length=255,default='amase')
    units = models.ManyToManyField("Units", blank=True, null=True)
    description = HTMLField()
    amenities = HTMLField()
    property_status = models.CharField(max_length=20, choices=PROPERTY_STATUSES,default='available')
    year_built = models.PositiveIntegerField(default=2023)
    square_footage = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name_plural = "Properties"
        managed = True
        db_table = "properties"

    def get_absolute_url(self):
        return reverse("property-detail", kwargs={"pk": self.pk})


class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    image = models.ImageField(upload_to="property/images")

    def __str__(self):
        return self.image.url or None

    class Meta:
        verbose_name_plural = "Property Images"
        managed = True
        db_table = "property_images"


class PropertyUnitImages(models.Model):
    property_unit = models.ForeignKey("Units", on_delete=models.CASCADE, related_name='unit_images')
    image = models.ImageField(upload_to="property_units/images")

    def __str__(self):
        return self.image.url or None

    class Meta:
        verbose_name_plural = "Property Unit Images"
        managed = True
        db_table = "property_unit_images"


class Units(models.Model):
    UNIT_TYPES = [
        ('studio', 'Studio'),
        ('1br', '1 Bedroom'),
        ('2br', '2 Bedrooms'),
        ('3br', '3 Bedrooms'),
        ('penthouse', 'Penthouse'),
        ('office', 'Office Space'),
    ]
    title = models.CharField(max_length=100,default='test')
    unit_code = models.CharField(max_length=100, default='001')
    description = HTMLField()
    rental_price = models.DecimalField(max_digits=8, decimal_places=2)
    property_unit_images=models.ManyToManyField(PropertyUnitImages, blank=True, null=True)
    square_footage = models.PositiveIntegerField(default=2)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    is_featured=models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.unit_code}"

    class Meta:
        verbose_name_plural = "Units"
        managed = True
        db_table = "units"
