/**
 * Gestion des formulaires de contact avec Formspree (AJAX + Accept: application/json)
 * Pour recevoir les envois (localhost + en ligne) :
 * 1. Formspree : activer le formulaire (email de confirmation au 1er envoi)
 * 2. Formspree → Paramètres → Domaines autorisés : ajouter "localhost" pour les tests
 *    et "greensolarsun.com" (ou votre domaine) pour la prod. Vide = tout autoriser.
 */
(function() {
  function initContactForms() {
    document.querySelectorAll('form.contact-form').forEach(function(form) {
      if (form.action.indexOf('formspree') === -1) return;
      var responseEl = form.querySelector('.response');
      if (!responseEl) return;

      form.addEventListener('submit', function(e) {
        e.preventDefault();
        e.stopPropagation();

        var formData = new FormData(form);
        var submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
          submitBtn.disabled = true;
        }

        function showMessage(msg, type) {
          responseEl.textContent = msg;
          responseEl.className = 'response ' + (type || 'success');
          if (submitBtn) submitBtn.disabled = false;
        }

        fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: { 'Accept': 'application/json' },
          credentials: 'omit',
          redirect: 'manual'
        })
          .then(function(res) {
            if (res.type === 'opaqueredirect' || res.status === 302) {
              return { ok: true, status: res.status, data: { ok: true } };
            }
            return res.text().then(function(text) {
              try {
                return { ok: res.ok, status: res.status, data: JSON.parse(text) };
              } catch (err) {
                return { ok: res.ok, status: res.status, data: {} };
              }
            });
          })
          .then(function(result) {
            var ok = result.ok;
            var data = result.data || {};
            var status = result.status;

            if (ok && data.ok) {
              showMessage('Merci ! Votre message a bien été envoyé.', 'success');
              form.reset();
              return;
            }

            var errMsg = '';
            if (data.error && typeof data.error === 'string') {
              errMsg = data.error;
            } else if (data.errors && data.errors.length) {
              errMsg = data.errors.map(function(e) { return e.message || e; }).join(' ');
            }

            var hint = '';
            if (status === 403 || (errMsg && (errMsg.indexOf('host') !== -1 || errMsg.indexOf('domain') !== -1 || errMsg.indexOf('Form not active') !== -1))) {
              hint = ' Sur formspree.io : ajoutez "localhost" dans Paramètres → Domaines autorisés pour tester en local, et vérifiez que le formulaire est activé (email de confirmation).';
            }
            showMessage((errMsg || 'Envoi refusé.') + hint + ' Sinon contactez-nous au +212 664638883 ou +212 0660830110.', 'error');
          })
          .catch(function(err) {
            console.error('Formspree fetch error:', err);
            showMessage('Envoi impossible (réseau ou CORS). Vérifiez votre connexion. Si vous testez en local, utilisez un serveur (ex: python -m http.server 8080) et ajoutez "localhost" dans Formspree → Domaines autorisés. Sinon contactez-nous au +212 664638883 ou +212 0660830110.', 'error');
          });
      }, true);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initContactForms);
  } else {
    initContactForms();
  }
})();
