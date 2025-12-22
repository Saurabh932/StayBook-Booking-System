import { setFlash } from "./script.js";

(() => {
  'use strict';

  const forms = document.querySelectorAll('.needs-validation');

  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      event.preventDefault();

      if (!form.checkValidity()) {
        event.stopPropagation();
        form.classList.add('was-validated');
        return;
      }

      form.classList.add('was-validated');

      // Notify feature code that the form is valid
      form.dispatchEvent(
        new CustomEvent('form:valid', { bubbles: true })
      );
    });
  });
})();
