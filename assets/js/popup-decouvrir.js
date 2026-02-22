(function() {
    var STORAGE_KEY = 'popupDecouvrirShown';
    var DELAY_MS = 45000; // 45 secondes
    var INSTAGRAM_REEL_URL = 'https://www.instagram.com/reel/DUPIPo6jvHb/';
    var INSTAGRAM_EMBED_URL = 'https://www.instagram.com/reel/DUPIPo6jvHb/embed/';

    function showPopup() {
        try {
            if (sessionStorage.getItem(STORAGE_KEY)) return;
            sessionStorage.setItem(STORAGE_KEY, '1');
        } catch (e) {}

        var overlay = document.getElementById('popup-decouvrir-overlay');
        if (overlay) {
            overlay.classList.add('is-visible');
            document.body.style.overflow = 'hidden';
        }
    }

    function hidePopup() {
        var overlay = document.getElementById('popup-decouvrir-overlay');
        if (overlay) {
            overlay.classList.remove('is-visible');
            document.body.style.overflow = '';
        }
    }

    function createPopup() {
        if (document.getElementById('popup-decouvrir-overlay')) return;

        var overlay = document.createElement('div');
        overlay.id = 'popup-decouvrir-overlay';
        overlay.innerHTML =
            '<div id="popup-decouvrir-box">' +
                '<button type="button" class="popup-decouvrir-close" aria-label="Fermer">&times;</button>' +
                '<h2 class="popup-decouvrir-title">Quand le savoir-faire rencontre l\'énergie solaire</h2>' +
                '<div class="popup-decouvrir-video-wrap">' +
                    '<iframe src="' + INSTAGRAM_EMBED_URL + '" allowfullscreen scrolling="no" allow="encrypted-media"></iframe>' +
                '</div>' +
                '<div class="popup-decouvrir-link-wrap">' +
                    '<a href="' + INSTAGRAM_REEL_URL + '" target="_blank" rel="noopener">Voir sur Instagram</a>' +
                '</div>' +
            '</div>';

        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) hidePopup();
        });

        var closeBtn = overlay.querySelector('.popup-decouvrir-close');
        if (closeBtn) closeBtn.addEventListener('click', hidePopup);

        var box = overlay.querySelector('#popup-decouvrir-box');
        if (box) box.addEventListener('click', function(e) { e.stopPropagation(); });

        document.body.appendChild(overlay);
    }

    function init() {
        createPopup();
        setTimeout(showPopup, DELAY_MS);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
