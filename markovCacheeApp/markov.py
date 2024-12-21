from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib
import librosa
import numpy as np 
def modelcachee(url):
    model_filename="markovCacheeApp\hmm_model2.pkl"
    data_filename="markovCacheeApp\data2.pkl"
    if os.path.exists(model_filename) and os.path.exists(data_filename):
        print(f"Chargement du modèle depuis {model_filename}...")
        model_loaded = joblib.load(model_filename)
        data_loaded = joblib.load(data_filename)
        X_test = data_loaded["X_test"]
        y_test = data_loaded["y_test"]
        metadata_test = data_loaded["metadata_test"]
        signal_test, sr_test = librosa.load(url, sr=None)
        mfcc_test = librosa.feature.mfcc(y=signal_test, sr=sr_test, n_mfcc=13)
        mfcc_test_mean = np.mean(mfcc_test.T, axis=0)
        similarities = cosine_similarity([mfcc_test_mean], X_test)
        # Trouver l'échantillon avec la similarité cosinus maximale
        closest_index = np.argmax(similarities)  # Trouver l'indice de l'échantillon le plus similaire
        max_similarity = similarities[0][closest_index]
        
        # Afficher la similarité cosinus maximale
        print(f"Similarité cosinus maximale : {max_similarity:.4f}")
        
        # Tolérance pour considérer un échantillon comme appartenant à un accent connu
        tolerance = 0.9 # Cette tolérance peut être ajustée selon tes besoins
        
        # Vérifier si la similarité cosinus dépasse la tolérance
        if max_similarity >= tolerance:
            predicted_accent = y_test[closest_index]
            predicted_metadata = metadata_test[closest_index]  # Obtenir les informations associées
            print(f"Genre prédit pour l'audio de test : {predicted_metadata['gender']}")
            return f"Accent prédit pour l'audio de test : {predicted_accent}"
        else:
            return f"L'échantillon de test ne correspond pas à un accent connu (similarité cosinus = {max_similarity:.4f})"
    else:
        return f"Modèle non trouvé"
        