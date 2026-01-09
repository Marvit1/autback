from django.db import models

class Car(models.Model):
    class Status(models.TextChoices):
        ARMENIA = 'armenia', 'ՀՀ-ում'
        TRANSIT = 'transit', 'Ճանապարհին'
        AUCTION = 'auction', 'Աճուրդում'
 
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    fuel = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AUCTION,
        verbose_name="Կարգավիճակ"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

    def get_translation(self, lang_code: str):
        fallback_order = [lang_code, 'hy', 'ru', 'en']
        for code in fallback_order:
            trans = self.translations.filter(language=code).first()
            if trans:
                return trans
        return None


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    
    def __str__(self):
        return f"Image for {self.car.make} {self.car.model}"


class CarTranslation(models.Model):
    LANG_CHOICES = [
        ('hy', 'Armenian'),
        ('ru', 'Russian'),
        ('en', 'English'),
    ]

    car = models.ForeignKey(Car, related_name='translations', on_delete=models.CASCADE)
    language = models.CharField(max_length=5, choices=LANG_CHOICES)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ('car', 'language')

    def __str__(self):
        return f"{self.car} [{self.language}]"