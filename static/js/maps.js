// ============================================
// Drivera — Maps & UI Interactivity
// ============================================

// ── Navbar scroll effect ─────────────────────
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    }
});

// ── Mobile nav toggle ────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggle && navLinks) {
        toggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Auto-dismiss flash messages after 4s
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(40px)';
            setTimeout(() => flash.remove(), 300);
        }, 4000);
    });

    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
});


// ── Leaflet Maps Initialization ───────────────
document.addEventListener('DOMContentLoaded', () => {
    initMap();
});

function initMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Default center: India
    const defaultCenter = [20.5937, 78.9629];

    const map = L.map('map').setView(defaultCenter, 5);

    // Using CartoDB Dark Matter for the dark theme feel 
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Add supplier markers from data attributes
    const supplierItems = document.querySelectorAll('.supplier-list-item');
    const markers = [];

    supplierItems.forEach(item => {
        const lat = parseFloat(item.dataset.lat);
        const lng = parseFloat(item.dataset.lng);
        const name = item.dataset.name;
        const vehicles = item.dataset.vehicles || '0';
        const price = item.dataset.price || 'N/A';
        const verified = item.dataset.verified === '1';

        if (isNaN(lat) || isNaN(lng)) return;

        const customIcon = L.divIcon({
            className: 'custom-map-icon',
            html: `<div style="background-color: #FF6B35; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 6px rgba(0,0,0,0.5);"></div>`,
            iconSize: [22, 22],
            iconAnchor: [11, 11]
        });

        const marker = L.marker([lat, lng], {icon: customIcon}).addTo(map);

        const verifiedBadge = verified
            ? '<span style="color:#22C55E;font-weight:600;">✓ Verified</span>'
            : '';

        const popupContent = `
            <div style="font-family:'DM Sans',sans-serif;color:#0F172A;padding:4px;min-width:200px;">
                <h3 style="font-family:'Sora',sans-serif;margin:0 0 6px;font-size:1rem;">${name}</h3>
                ${verifiedBadge}
                <p style="margin:6px 0;font-size:0.85rem;color:#334155;">
                    🚗 ${vehicles} vehicles
                </p>
                <p style="margin:0;font-size:0.9rem;font-weight:600;color:#FF6B35;">
                    From ₹${price}/day
                </p>
            </div>
        `;

        marker.bindPopup(popupContent, {
            closeButton: false,
            offset: [0, -10]
        });
        markers.push(marker);

        // Highlight supplier card on marker hover
        marker.on('mouseover', () => {
            item.style.borderColor = '#FF6B35';
        });
        marker.on('mouseout', () => {
            if (!item.classList.contains('selected')) {
                item.style.borderColor = 'rgba(255,255,255,0.06)';
            }
        });

        // Click supplier card to pan to marker
        item.addEventListener('click', () => {
            map.flyTo([lat, lng], 12);
            marker.openPopup();

            supplierItems.forEach(i => i.classList.remove('selected'));
            item.classList.add('selected');
            
            // Sync form hidden inputs for Booking
            const idInput = document.getElementById('selectedSupplierId');
            if(idInput) {
                idInput.value = item.dataset.id || '';
                document.getElementById('selectedVehicleType').value = document.getElementById('vehicleType').value;
                document.getElementById('selectedStartDate').value = document.getElementById('startDate').value;
                document.getElementById('selectedEndDate').value = document.getElementById('endDate').value;
                document.getElementById('selectedFleetSize').value = document.getElementById('fleetSize').value;
                document.getElementById('bookSelectedFleet').disabled = false;
            }
        });
    });

    // Fit bounds to all markers
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds(), {padding: [30, 30]});
    }

    // ── Filtering Logic ─────────────────────────
    const searchLocation = document.getElementById('searchLocation');
    const vehicleTypeSelect = document.getElementById('vehicleType');
    const fleetSizeSelect = document.getElementById('fleetSize');

    function filterSuppliers() {
        const locFilter = searchLocation.value.toLowerCase();
        const typeFilter = vehicleTypeSelect.value;
        const sizeFilter = parseInt(fleetSizeSelect.value) || 0;

        let visibleCount = 0;

        supplierItems.forEach((item, index) => {
            const loc = (item.dataset.location || '').toLowerCase();
            const types = (item.dataset.types || '').split(',');
            const vehicles = parseInt(item.dataset.vehicles) || 0;
            const marker = markers[index];

            const matchesLoc = loc.includes(locFilter);
            const matchesType = !typeFilter || types.includes(typeFilter);
            const matchesSize = vehicles >= sizeFilter;

            if (matchesLoc && matchesType && matchesSize) {
                item.style.display = 'block';
                if (marker) marker.addTo(map);
                visibleCount++;
            } else {
                item.style.display = 'none';
                if (marker) map.removeLayer(marker);
            }
        });

        // Update count text
        const countText = document.querySelector('.booking-sidebar h4');
        if (countText) {
            countText.textContent = `${visibleCount} Suppliers Found`;
        }
    }

    if (searchLocation) searchLocation.addEventListener('input', filterSuppliers);
    if (vehicleTypeSelect) vehicleTypeSelect.addEventListener('change', filterSuppliers);
    if (fleetSizeSelect) fleetSizeSelect.addEventListener('change', filterSuppliers);
}
