// Worker Portal Logic

document.addEventListener('DOMContentLoaded', () => {
    // Populate simple bar chart
    const chartBars = document.querySelectorAll('.chart-bar-fill');
    if (chartBars.length > 0) {
        setTimeout(() => {
            chartBars[0].style.height = '40%';
            chartBars[1].style.height = '60%';
            chartBars[2].style.height = '30%';
            chartBars[3].style.height = '80%';
            chartBars[4].style.height = '50%';
            chartBars[5].style.height = '90%';
            chartBars[6].style.height = '70%'; // Today
        }, 100);
    }
});

function acceptJob(btn, elId) {
    btn.innerHTML = '<i class="fas fa-check"></i> Accepted';
    btn.classList.replace('btn-primary', 'btn-success');
    btn.style.backgroundColor = 'var(--success)';
    btn.style.borderColor = 'var(--success)';
    btn.disabled = true;
    
    // Hide the reject button next to it
    const rejectBtn = btn.nextElementSibling;
    if (rejectBtn && rejectBtn.classList.contains('btn-outline')) {
        rejectBtn.style.display = 'none';
    }
    
    showToast('Job Accepted! Customer notified.', 'success');
}

function rejectJob(btn, elId) {
    const card = document.getElementById(elId);
    if(card) {
        card.style.opacity = '0.5';
        card.style.pointerEvents = 'none';
        btn.innerHTML = 'Rejected';
    }
}
