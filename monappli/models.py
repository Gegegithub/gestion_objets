from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class ObjetDefectueux(models.Model):
    STATUS_CHOICES = [
        ('DEFECTUEUX', 'Défectueux'),
        ('OK', 'OK'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_produit = models.CharField(max_length=100, db_index=True)
    date_inspection = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, db_index=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_produit} ({self.status})"

class AnalyseIA(models.Model):
    objet = models.ForeignKey(ObjetDefectueux, on_delete=models.CASCADE, related_name='analyses')
    date_analyse = models.DateTimeField(auto_now_add=True)
    resultats = models.JSONField()
    succes = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    image_annotee = models.TextField(blank=True, null=True)  # Pour stocker l'image en base64

    class Meta:
        ordering = ['-date_analyse']
        verbose_name = "Analyse IA"
        verbose_name_plural = "Analyses IA"

    def __str__(self):
        return f"Analyse de {self.objet.nom_produit} - {self.date_analyse}"

class JournalActivite(models.Model):
    ACTION_CHOICES = [
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    objet = models.ForeignKey(ObjetDefectueux, on_delete=models.CASCADE)
    date_action = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_action']
        verbose_name = "Journal d'activité"
        verbose_name_plural = "Journaux d'activité"

    def __str__(self):
        return f"{self.utilisateur.username} - {self.action} - {self.objet.nom_produit} - {self.date_action}"
