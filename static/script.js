document.addEventListener('DOMContentLoaded', function() {
    // Sync offline invoices when online
    if (navigator.onLine) {
        const pendingInvoice = localStorage.getItem('pendingInvoice');
        if (pendingInvoice) {
            fetch('/invoices/sync/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                },
                body: pendingInvoice
            }).then(response => {
                if (response.ok) {
                    localStorage.removeItem('pendingInvoice');
                    alert('Factura offline sincronizada.');
                }
            });
        }
    }
});