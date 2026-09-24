// Customer Portal Logic

document.addEventListener('DOMContentLoaded', () => {
    renderServices();
    renderNearbyWorkers();

    const searchInput = document.getElementById('serviceSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            if (term.length > 2) {
                // Simulate AI search trigger
                showAIResults(term);
            } else if (term.length === 0) {
                hideAIResults();
                renderNearbyWorkers();
            }
        });
    }
});

function renderServices() {
    const grid = document.getElementById('customerServicesGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    DATA.services.forEach(service => {
        const div = document.createElement('div');
        div.className = 'category-card';
        div.innerHTML = `
            <div class="category-icon" style="color: ${service.color}; background: ${service.color}20;">
                <i class="fas ${service.icon}"></i>
            </div>
            <h4>${service.name}</h4>
        `;
        div.addEventListener('click', () => {
            document.getElementById('serviceSearch').value = service.name;
            showAIResults(service.name.toLowerCase());
        });
        grid.appendChild(div);
    });
}

function renderNearbyWorkers() {
    const list = document.getElementById('nearbyWorkersList');
    if (!list) return;
    
    list.innerHTML = '';
    
    // Display first 2 workers for nearby
    const workers = DATA.workers.slice(0, 2);
    
    workers.forEach(worker => {
        list.appendChild(createWorkerCard(worker, false));
    });
}

function showAIResults(term) {
    const defaultSection = document.getElementById('defaultSection');
    const aiSection = document.getElementById('aiMatchSection');
    const aiResultsList = document.getElementById('aiResultsList');
    
    if (!defaultSection || !aiSection) return;
    
    defaultSection.style.display = 'none';
    aiSection.style.display = 'block';
    
    // Filter workers based on term or just show AI matched ones
    const matchedWorkers = DATA.workers.filter(w => w.skill.toLowerCase().includes(term));
    
    // If no match, show default AI top 3
    const workersToShow = matchedWorkers.length > 0 ? matchedWorkers : DATA.workers.slice(0, 3);
    
    aiResultsList.innerHTML = '';
    
    const scores = [98, 94, 91];
    
    workersToShow.forEach((worker, index) => {
        const score = scores[index] || 85;
        aiResultsList.appendChild(createWorkerCard(worker, true, score));
    });
}

function hideAIResults() {
    const defaultSection = document.getElementById('defaultSection');
    const aiSection = document.getElementById('aiMatchSection');
    
    if (defaultSection && aiSection) {
        defaultSection.style.display = 'block';
        aiSection.style.display = 'none';
    }
}

function createWorkerCard(worker, isAiMatch = false, score = 0) {
    const div = document.createElement('div');
    div.className = 'worker-card animate-fade-in-up';
    
    const aiBadgeHtml = isAiMatch ? `
        <div style="background: var(--ai-bg); color: var(--ai); padding: 0.5rem 1rem; border-radius: var(--radius); text-align: center; margin-right: 1.5rem; border: 1px solid #bfdbfe;">
            <div style="font-size: 1.5rem; font-weight: 700;">${score}%</div>
            <div style="font-size: 0.75rem; font-weight: 600;">Match</div>
        </div>
    ` : '';

    const aiReasonsHtml = isAiMatch ? `
        <div class="match-reasons">
            <span class="match-reason"><i class="fas fa-check"></i> Skill match</span>
            <span class="match-reason"><i class="fas fa-map-marker-alt"></i> Nearby</span>
            <span class="match-reason"><i class="fas fa-star"></i> High rating</span>
        </div>
    ` : '';

    div.innerHTML = `
        <div class="worker-info">
            ${aiBadgeHtml}
            <img src="https://ui-avatars.com/api/?name=${worker.name.replace(' ', '+')}&background=047857&color=fff" alt="${worker.name}" class="worker-avatar">
            <div class="worker-details">
                <h3>${worker.name} ${worker.verified ? '<i class="fas fa-check-circle verified-badge" title="Verified"></i>' : ''}</h3>
                <div style="font-weight: 500; color: var(--text); margin-bottom: 0.5rem;">${worker.skill}</div>
                <div class="worker-meta">
                    <span><i class="fas fa-star text-warning"></i> ${worker.rating}</span>
                    <span><i class="fas fa-briefcase"></i> ${worker.experience}</span>
                    <span><i class="fas fa-map-marker-alt"></i> ${worker.distance}</span>
                </div>
                ${aiReasonsHtml}
            </div>
        </div>
        <div class="worker-price">
            <div>
                <div class="price-val">${worker.price}</div>
                <div class="price-label">Estimated start</div>
            </div>
            <button class="btn btn-primary" onclick="bookWorker('${worker.id}')">Book Now</button>
            <button class="btn btn-outline" style="padding: 0.75rem; border-radius: var(--radius);" onclick="viewProfile('${worker.id}')"><i class="fas fa-user"></i></button>
        </div>
    `;
    return div;
}

function bookWorker(workerId) {
    localStorage.setItem('selectedWorker', workerId);
    window.location.href = 'booking.html';
}

function viewProfile(workerId) {
    localStorage.setItem('selectedWorker', workerId);
    window.location.href = 'profile.html';
}
