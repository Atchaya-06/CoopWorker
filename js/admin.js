// Admin & AI Insights Logic

document.addEventListener('DOMContentLoaded', () => {
    
    // Animate CSS Charts
    setTimeout(() => {
        // Bookings Overview (Bar Chart)
        const bars = document.querySelectorAll('.css-bar');
        const heights = ['30%', '50%', '40%', '70%', '60%', '90%', '80%'];
        bars.forEach((bar, index) => {
            if(heights[index]) bar.style.height = heights[index];
        });

        // Service Demand (Horizontal Bar)
        const hBars = document.querySelectorAll('.css-h-bar');
        const hWidths = ['95%', '65%', '45%', '30%'];
        hBars.forEach((bar, index) => {
            if(hWidths[index]) bar.style.width = hWidths[index];
        });
        
        // Revenue (Line simulation via height)
        const revBars = document.querySelectorAll('#revChart .css-bar');
        const revHeights = ['40%', '45%', '42%', '55%', '65%', '85%', '90%'];
        revBars.forEach((bar, index) => {
            if(revHeights[index]) bar.style.height = revHeights[index];
        });
        
    }, 200);

    // Verification Modal
    const verifyModal = document.getElementById('verifyModal');
    if (verifyModal) {
        const closeBtn = verifyModal.querySelector('.modal-close');
        
        window.openVerifyModal = function(id) {
            // Find worker data or mock
            document.getElementById('verifyWorkerId').textContent = id;
            verifyModal.classList.add('active');
        };

        closeBtn.addEventListener('click', () => {
            verifyModal.classList.remove('active');
        });

        verifyModal.addEventListener('click', (e) => {
            if (e.target === verifyModal) {
                verifyModal.classList.remove('active');
            }
        });
    }
});

function approveWorker() {
    document.getElementById('verifyModal').classList.remove('active');
    showToast('Worker W001 has been verified successfully.', 'success');
    
    const row = document.querySelector('tr[data-id="W001"]');
    if (row) {
        const statusCell = row.querySelector('.status-cell');
        statusCell.innerHTML = '<span class="badge badge-success">Verified</span>';
        
        const actionCell = row.querySelector('.action-cell');
        actionCell.innerHTML = '<button class="btn btn-outline" style="padding: 0.25rem 0.75rem; font-size: 0.75rem;">Manage</button>';
    }
}
