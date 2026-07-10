    let mybutton = document.getElementById("btn-back-to-top");

    window.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }

    mybutton.addEventListener("click", backToTop);

    function backToTop() {
        window.scrollTo({
            top: 0,
            behavior: "smooth" 
        });
    }
    function cargarResumen() {
    const myModal = new bootstrap.Modal(document.getElementById('resumenModal'));
    myModal.show();
    
    const content = document.getElementById('modal-body-content');
    content.innerHTML = '<div class="text-center"><div class="spinner-border text-danger"></div><p>Consultando...</p></div>';

    const desde = document.querySelector('input[name="desde"]').value;
    const hasta = document.querySelector('input[name="hasta"]').value;

    fetch(`/obtener_resumen?desde=${desde}&hasta=${hasta}`)
        .then(response => response.json())
        .then(res => {
            if (res.status === 'success') {
                let html = '<div class="list-group list-group-flush">';
                res.data.forEach(item => {
                    html += `
                        <div class="list-group-item">
                            <h6 class="fw-bold text-uppercase" style="color: var(--gob-guinda);">${item.cuenta || 'Sin cuenta'} (${item.cantidad_recibos || '0'})</h6>
                            <div class="d-flex justify-content-between">
                                <span>Total Neto:</span>
                                <span class="fw-bold text-success">$${parseFloat(item.total_neto).toLocaleString('en-US', {minimumFractionDigits: 2})}</span>
                            </div>
                            <div class="d-flex justify-content-between text-muted small">
                                <span>Total Descuento:</span>
                                <span>$${parseFloat(item.total_descuento).toLocaleString('en-US', {minimumFractionDigits: 2})}</span>
                            </div>
                        </div>`;
                });
                html += '</div>';
                content.innerHTML = html;
            } else {
                content.innerHTML = `<div class="alert alert-warning">${res.message}</div>`;
            }
        })
        .catch(err => {
            content.innerHTML = `<div class="alert alert-danger">Error de conexión: ${err}</div>`;
        });
}

function switchView(viewType) {
    const cards = document.getElementById('container-cards');
    const table = document.getElementById('container-table');
    const btnCards = document.getElementById('btn-view-cards');
    const btnTable = document.getElementById('btn-view-table');

    if (viewType === 'cards') {
        cards.classList.remove('view-hidden');
        table.classList.add('view-hidden');
        btnCards.classList.replace('btn-outline-secondary', 'btn-guinda-active'); 
    } else {
        cards.classList.add('view-hidden');
        table.classList.remove('view-hidden');
    }
}

document.addEventListener("DOMContentLoaded", function() {
    if (window.innerWidth >= 768) {
        switchView('table');
    } else {
        switchView('cards');
    }
});