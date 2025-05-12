from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.accueil, name='accueil'),
    path('ajouter/', views.ajouter_objet, name='ajouter'),
    path('objet/<uuid:pk>/', views.detail_objet, name='detail_objet'),
    path('objet/<uuid:pk>/modifier/', views.modifier_objet, name='modifier_objet'),
    path('objet/<uuid:pk>/supprimer/', views.confirmer_suppression, name='confirmer_suppression'),
    path('objet/<uuid:pk>/supprimer/confirmer/', views.supprimer_objet, name='supprimer_objet'),
    path('objet/<uuid:pk>/analyser/', views.analyser_objet, name='analyser_objet'),
    path('corbeille/', views.corbeille, name='corbeille'),
    path('journal/', views.journal_activite, name='journal_activite'),
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
]

 