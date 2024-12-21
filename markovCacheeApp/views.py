from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .markov import *
# Create your views here.
def index(request):
    context={}
    context["audio"]=0
    return render(request, 'index.html',context)

def genre(request):
    context = {"audio": 0}  # Initialiser le contexte
    if request.method == "POST" and 'file-upload' in request.FILES:
        # print("je suis ici hhh")
        file_uploaded = request.FILES['file-upload']  # Récupérer l'audio uploadée
        files = os.listdir(settings.IMAGE_UPLOAD_PATH)

        if file_uploaded:
            try:
                # Obtenir l'extension du fichier uploadé
                file_extension = os.path.splitext(file_uploaded.name)[1]

                # Créer un nouveau nom de fichier basé sur le nombre de fichiers existants
                new_filename = f'{len(files)}{file_extension}'

                # Sauvegarder l'audio dans le dossier 'audios' avec le nouveau nom
                fs = FileSystemStorage(location=settings.IMAGE_UPLOAD_PATH)
                fs.save(new_filename, file_uploaded)

                # Construire l'URL correcte de l'audio
                audio_url = os.path.join(settings.MEDIA_URL, 'images', new_filename)
                context["file"] = audio_url
                
                # Convertir l'URL en chemin système pour mpimg
                url_path = os.path.join(settings.MEDIA_ROOT, 'images', new_filename)
                print(f"url_path est {url_path}")
                context["genre"] = modelcachee(url_path)  # Passer le chemin correct à la fonction typeDeGenre
                context["audio"] = 1  # Indiquer qu'une audio a été chargée
                print("resulta est :",context["genre"])
            except Exception as e:
                pass

    return render(request, 'index.html',context)