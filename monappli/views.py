from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import ObjetDefectueux, JournalActivite, AnalyseIA
from .forms import ObjetDefectueuxForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .ai_utils import ObjectAnalyzer

def is_superuser(user):
    return user.is_superuser

@login_required
def accueil(request):
    objets = ObjetDefectueux.objects.filter(deleted_at__isnull=True).order_by('-date_inspection')
    paginator = Paginator(objets, 3)
    page = request.GET.get('page')
    objets = paginator.get_page(page)
    return render(request, 'accueil.html', {'objets': objets})

@user_passes_test(is_superuser)
def liste_utilisateurs(request):
    utilisateurs = User.objects.all().order_by('-date_joined')
    return render(request, 'monappli/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

@login_required
def ajouter_objet(request):
    if request.method == 'POST':
        form = ObjetDefectueuxForm(request.POST)
        if form.is_valid():
            objet = form.save()
            # Enregistrer l'action dans le journal
            JournalActivite.objects.create(
                utilisateur=request.user,
                action='ajout',
                objet=objet,
                details=f"Ajout de l'objet {objet.nom_produit}"
            )
            return render(request, 'success.html')
    else:
        form = ObjetDefectueuxForm()
    
    return render(request, 'ajouter_objet.html', {'form': form})

@login_required
def detail_objet(request, pk):
    objet = get_object_or_404(ObjetDefectueux, pk=pk)
    return render(request, 'detail_objet.html', {'objet': objet})

@login_required
def modifier_objet(request, pk):
    objet = get_object_or_404(ObjetDefectueux, pk=pk)
    if request.method == 'POST':
        form = ObjetDefectueuxForm(request.POST, instance=objet)
        if form.is_valid():
            objet = form.save()
            # Enregistrer l'action dans le journal
            JournalActivite.objects.create(
                utilisateur=request.user,
                action='modification',
                objet=objet,
                details=f"Modification de l'objet {objet.nom_produit}"
            )
            return redirect('detail_objet', pk=objet.pk)
    else:
        form = ObjetDefectueuxForm(instance=objet)
    
    return render(request, 'modifier_objet.html', {'form': form, 'objet': objet})

@login_required
def confirmer_suppression(request, pk):
    objet = get_object_or_404(ObjetDefectueux, pk=pk)
    return render(request, 'confirmer_suppression.html', {'objet': objet})

@login_required
def supprimer_objet(request, pk):
    if request.method == 'POST':
        objet = get_object_or_404(ObjetDefectueux, pk=pk)
        objet.deleted_at = timezone.now()
        objet.save()
        # Enregistrer l'action dans le journal
        JournalActivite.objects.create(
            utilisateur=request.user,
            action='suppression',
            objet=objet,
            details=f"Suppression de l'objet {objet.nom_produit}"
        )
        return redirect('corbeille')
    return redirect('confirmer_suppression', pk=pk)

@user_passes_test(is_superuser)
def corbeille(request):
    objets = ObjetDefectueux.objects.filter(deleted_at__isnull=False).order_by('-deleted_at')
    paginator = Paginator(objets, 3)
    page = request.GET.get('page')
    objets = paginator.get_page(page)
    return render(request, 'corbeille.html', {'objets': objets})

@user_passes_test(is_superuser)
def journal_activite(request):
    activites = JournalActivite.objects.all().order_by('-date_action')
    paginator = Paginator(activites, 10)
    page = request.GET.get('page')
    activites = paginator.get_page(page)
    return render(request, 'journal_activite.html', {'activites': activites})

@login_required
def analyser_objet(request, pk):
    print("Début de l'analyse pour l'objet", pk)
    objet = get_object_or_404(ObjetDefectueux, pk=pk)
    
    if not objet.image_url:
        print("Pas d'URL d'image trouvée pour l'objet", pk)
        return JsonResponse({
            'success': False,
            'message': "Aucune image n'est associée à cet objet"
        })

    print("URL de l'image:", objet.image_url)
    analyzer = ObjectAnalyzer()
    try:
        resultats = analyzer.analyze_image_url(objet.image_url)
        print("Résultats de l'analyse:", resultats)
    except Exception as e:
        print("Erreur lors de l'analyse:", str(e))
        return JsonResponse({
            'success': False,
            'message': f"Erreur lors de l'analyse: {str(e)}"
        })
    
    # Sauvegarder les résultats
    try:
        analyse = AnalyseIA.objects.create(
            objet=objet,
            resultats=resultats['detections'],
            succes=resultats['success'],
            message=resultats['message'],
            image_annotee=resultats.get('image_base64')
        )
        print("Analyse sauvegardée avec succès, ID:", analyse.id)
    except Exception as e:
        print("Erreur lors de la sauvegarde de l'analyse:", str(e))
        return JsonResponse({
            'success': False,
            'message': f"Erreur lors de la sauvegarde: {str(e)}"
        })
    
    return JsonResponse({
        'success': True,
        'message': resultats['message'],
        'detections': resultats['detections'],
        'image_base64': resultats.get('image_base64')
    })

