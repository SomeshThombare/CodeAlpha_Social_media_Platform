/*  core/static/core/main.js
    Shared JavaScript for the Social Media App
*/

// ── Auto-dismiss Django messages after 4 seconds ──
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.message-alert, .alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.4s ease';
      alert.style.opacity = '0';
      setTimeout(function () { alert.remove(); }, 400);
    }, 4000);
  });
});

// ── Show selected filename in file input label ──
document.addEventListener('DOMContentLoaded', function () {
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      const label = input.closest('label');
      if (label && this.files.length > 0) {
        label.textContent = '📷 ' + this.files[0].name;
      }
    });
  });
});
