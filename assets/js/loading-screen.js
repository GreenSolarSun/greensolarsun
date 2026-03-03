/**
 * Loading Screen Script Professional - GreenSolarSun
 * Gère l'affichage et la disparition de l'écran de chargement
 * Animation plus longue pour une meilleure visibilité
 */

(function() {
    'use strict';
    
    // Fonction pour masquer l'écran de chargement
    function hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        
        if (!loadingScreen) {
            return;
        }
        
        // Ajouter la classe pour l'animation de disparition
        loadingScreen.classList.add('loaded');
        
        // Supprimer complètement après l'animation
        setTimeout(function() {
            if (loadingScreen && loadingScreen.parentNode) {
                loadingScreen.remove();
            }
            // Permettre le scroll
            document.body.style.overflow = '';
        }, 1000); // Même durée que la transition CSS
    }
    
    // Empêcher le scroll pendant le chargement
    document.body.style.overflow = 'hidden';
    
    // Attendre que toutes les ressources soient chargées
    if (document.readyState === 'complete') {
        // La page est déjà chargée - délai minimum pour voir l'animation (plus long)
        setTimeout(hideLoadingScreen, 1500); // Délai minimum de 1.5 secondes
    } else {
        // Attendre le chargement complet
        window.addEventListener('load', function() {
            setTimeout(hideLoadingScreen, 1500); // Délai minimum de 1.5 secondes pour voir l'animation
        });
    }
    
    // Sécurité : masquer après 8 secondes maximum (plus long)
    setTimeout(function() {
        hideLoadingScreen();
    }, 8000);
})();