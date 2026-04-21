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


// ── Google Maps Initialization ───────────────
// Note: Replace YOUR_API_KEY in the script tag with an actual Google Maps API key
function initMap() {
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Default center: India
    const defaultCenter = { lat: 20.5937, lng: 78.9629 };

    const map = new google.maps.Map(mapElement, {
        zoom: 5,
        center: defaultCenter,
        styles: [
            // Dark theme style for map
            { elementType: 'geometry', stylers: [{ color: '#1E293B' }] },
            { elementType: 'labels.text.stroke', stylers: [{ color: '#0F172A' }] },
            { elementType: 'labels.text.fill', stylers: [{ color: '#64748B' }] },
            {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{ color: '#334155' }]
            },
            {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{ color: '#0F172A' }]
            },
            {
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{ visibility: 'off' }]
            }
        ]
    });

    // Add supplier markers from data attributes
    const supplierItems = document.querySelectorAll('.supplier-list-item');
    const markers = [];
    const infoWindow = new google.maps.InfoWindow();

    supplierItems.forEach(item => {
        const lat = parseFloat(item.dataset.lat);
        const lng = parseFloat(item.dataset.lng);
        const name = item.dataset.name;
        const vehicles = item.dataset.vehicles || '0';
        const price = item.dataset.price || 'N/A';
        const rating = item.dataset.rating || '0';
        const verified = item.dataset.verified === '1';

        if (isNaN(lat) || isNaN(lng)) return;

        const marker = new google.maps.Marker({
            position: { lat, lng },
            map: map,
            title: name,
            icon: {
                path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
                scale: 7,
                fillColor: '#FF6B35',
                fillOpacity: 1,
                strokeColor: '#E55A2B',
                strokeWeight: 2
            }
        });

        const verifiedBadge = verified
            ? '<span style="color:#22C55E;font-weight:600;">✓ Verified</span>'
            : '';

        marker.addListener('click', () => {
            infoWindow.setContent(`
                <div style="font-family:'DM Sans',sans-serif;color:#0F172A;padding:4px;min-width:200px;">
                    <h3 style="font-family:'Sora',sans-serif;margin:0 0 6px;font-size:1rem;">${name}</h3>
                    ${verifiedBadge}
                    <p style="margin:6px 0;font-size:0.85rem;color:#334155;">
                        🚗 ${vehicles} vehicles &nbsp;|&nbsp; ⭐ ${rating}
                    </p>
                    <p style="margin:0;font-size:0.9rem;font-weight:600;color:#FF6B35;">
                        From ₹${price}/day
                    </p>
                </div>
            `);
            infoWindow.open(map, marker);
        });

        markers.push(marker);

        // Highlight supplier card on marker hover
        marker.addListener('mouseover', () => {
            item.style.borderColor = '#FF6B35';
        });
        marker.addListener('mouseout', () => {
            if (!item.classList.contains('selected')) {
                item.style.borderColor = 'rgba(255,255,255,0.06)';
            }
        });

        // Click supplier card to pan to marker
        item.addEventListener('click', () => {
            map.panTo({ lat, lng });
            map.setZoom(12);
            google.maps.event.trigger(marker, 'click');

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
        const bounds = new google.maps.LatLngBounds();
        markers.forEach(m => bounds.extend(m.getPosition()));
        map.fitBounds(bounds);
    }
}
