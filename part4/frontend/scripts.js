/**
 * Reads a cookie by name; returns its value or null if missing.
 */
function getCookie(name) {
  const match = document.cookie.match(
    new RegExp('(?:^|; )' + name.replace(/([$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)')
  );
  return match ? decodeURIComponent(match[1]) : null;
}

document.addEventListener('DOMContentLoaded', () => {
  // Page detection handles
  const loginForm    = document.getElementById('login-form');
  const loginLink    = document.getElementById('login-link');
  const logoutLink   = document.getElementById('logout-link');
  const placesList   = document.getElementById('places-list');
  const placeDetail  = document.getElementById('place-details');
  const token        = getCookie('access_token');

  // ── Show / hide Login vs Logout ─────────────────────────
  if (loginLink)  loginLink.style.display  = token ? 'none' : 'inline-block';
  if (logoutLink) logoutLink.style.display = token ? 'inline-block' : 'none';

  // ── Wire up Logout click ─────────────────────────────────
  if (logoutLink) {
    logoutLink.addEventListener('click', ev => {
      ev.preventDefault();
      document.cookie = 'access_token=; path=/; max-age=0';
      window.location.href = 'login.html';
    });
  }

  // ── If on login.html, handle login form and stop ──────────
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
    return;
  }

  // ── Protect other pages: if no token, redirect to login ───
  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  // ── Index page (List of Places) initialization ───────────
  if (placesList) {
    initPlacesList();
  }

  // ── Place Details page initialization ────────────────────
  if (placeDetail) {
    initPlaceDetails();
  }

  // ── Add Review page initialization ────────────────────────
  const placeNameEl = document.getElementById('place-name');
  if (placeNameEl) {
    // 1) Redirect if not authenticated
    const addToken = getCookie('access_token');
    if (!addToken) {
      window.location.href = 'index.html';
      return;
    }

    // 2) Fill in place name
    const placeId = new URLSearchParams(window.location.search).get('id');
    fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: { 'Authorization': `Bearer ${addToken}` }
    })
      .then(res => res.ok ? res.json() : Promise.reject(res.status))
      .then(p => placeNameEl.innerText = p.title)
      .catch(() => placeNameEl.innerText = 'Unkown place');


    // 3) Handle review submission
    const reviewForm = document.getElementById('review-form');
    const feedbackEl = document.getElementById('review-feedback');
    reviewForm.addEventListener('submit', async ev => {
      ev.preventDefault();
      feedbackEl.textContent = '';
      feedbackEl.className   = 'feedback';

      const text   = document.getElementById('review-text').value.trim();
      const rating = +document.getElementById('review-rating').value;

      try {
        const res = await fetch(
          `http://localhost:5000/api/v1/reviews/`, {
            method:  'POST',
            headers: {
              'Content-Type':  'application/json',
              'Authorization': `Bearer ${addToken}`
            },
            body: JSON.stringify({ place_id: placeId, text, rating })
          }
        );
        const payload = await res.json().catch(() => ({}));

        if (res.ok) {
          feedbackEl.textContent = '🎉 Review submitted successfully!';
          feedbackEl.classList.add('success');
          reviewForm.reset();
          // fetch frech reviews and redraw the list
          loadAndRenderReviews(placeId);
        } else {
          feedbackEl.textContent = payload.message || `Error ${res.status}`;
          feedbackEl.classList.add('error');
        }
      } catch {
        feedbackEl.textContent = 'Network error – please try again later.';
        feedbackEl.classList.add('error');
      }
    });
  } // ← end if(addReviewForm)

}); // ← end DOMContentLoaded



// ==========================================
// 1. LOGIN HANDLER
// ==========================================
async function handleLogin(event) {
  event.preventDefault();
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  try {
    const res = await fetch('http://localhost:5000/api/v1/auth/login', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || res.statusText);

    document.cookie = `access_token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } catch (err) {
    alert('Login failed: ' + err.message);
  }
}

// ==========================================
// 2. PLACES LIST (Index)
// ==========================================
function renderPlaces(list) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';
  list.forEach(place => {
    const card = document.createElement('article');
    card.className = 'place-card';
    card.innerHTML = `
      <img src="${place.image_url || 'https://via.placeholder.com/300x150'}"
           alt="${place.title}">
      <div class="card-body">
        <h3>${place.title}</h3>
        <p class="price">$${place.price}/night</p>
        <button class="details-button"
                onclick="location.href='place.html?id=${place.id}'">
          View Details
        </button>
      </div>`;
    container.append(card);
  });
}

async function initPlacesList() {
  const filterEl = document.getElementById('price-filter');
  const token    = getCookie('access_token');

  try {
    const res    = await fetch('http://localhost:5000/api/v1/places/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const places = await res.json();

    filterEl.innerHTML = `
      <option value="">All</option>
      <option value="10">$10</option>
      <option value="50">$50</option>
      <option value="100">$100</option>
    `;
    renderPlaces(places);

    filterEl.addEventListener('change', () => {
      const max    = Number(filterEl.value);
      const subset = filterEl.value
        ? places.filter(p => p.price <= max)
        : places;
      renderPlaces(subset);
    });

  } catch {
    document.getElementById('places-list')
      .innerHTML = '<p>Unable to load places at the moment.</p>';
  }
}

// ==========================================
// 3. PLACE DETAILS PAGE
// ==========================================
async function initPlaceDetails() {
  const token       = getCookie('access_token');
  const placeId     = new URLSearchParams(window.location.search).get('id');
  const detailsEl   = document.getElementById('place-details');
  const reviewsEl   = document.getElementById('reviews');
  const addReviewEl = document.getElementById('add-review');
  const form        = document.getElementById('review-form');

  try {
    // Fetch place
    const res   = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const place = await res.json();

    // Render main info
    const amenities = place.amenities.map(a => a.name).join(', ');
    detailsEl.innerHTML = `
      <div class="place-info-card">
        <h1>${place.title}</h1>
        <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
        <p><strong>Price:</strong> $${place.price}/night</p>
        <p><strong>Description:</strong> ${place.description}</p>
        <p><strong>Amenities:</strong> ${amenities}</p>
      </div>`;

    await loadAndRenderReviews(placeId);

    // Render reviews

    // Toggle add‑review form
    addReviewEl.style.display = token ? 'block' : 'none';

    // Wire up review submission
    form.addEventListener('submit', async ev => {
      ev.preventDefault();
      const feedbackEl = document.getElementById('review-feedback');
      const text = document.getElementById('review-text').value.trim();
      const rating = +document.getElementById('review-rating').value;

      feedbackEl.textContent = '';
      feedbackEl.className   = '';

      try {
        const rres = await fetch(`http://localhost:5000/api/v1/reviews/`, {
          method:  'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type':  'application/json'
          },
          body: JSON.stringify({ place_id: placeId, text, rating })
        });

        if (!rres.ok) {
          const err = await rres.json().catch(() => ({}));
          feedbackEl.textContent = err.message || `Error ${rres.status}`;
          feedbackEl.classList.add('error');
          return;
        }
        feedbackEl.textContent = 'Your review has been posted!';
        feedbackEl.classList.add('success');
        form.reset();
        await loadAndRenderReviews(placeId);

      } catch {
        feedbackEl.textContent = 'Network error – please try again later.';
        feedbackEl.classList.add('error');
      }
    });

  } catch (e) {
    detailsEl.innerHTML = `<p>Unable to load place details: ${e.message}</p>`;
  }
}  // ← closes initPlaceDetails()

// ==========================================
// Helper: reload just the reviews section
// ==========================================
async function loadAndRenderReviews(placeId) {
  const token     = getCookie('access_token');
  const reviewsEl = document.getElementById('reviews');

  // re‑GET the single place (so you get updated .reviews[])
  const res   = await fetch(
    `http://localhost:5000/api/v1/places/${placeId}/reviews`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  if (!res.ok) {
    reviewsEl.innerHTML = `<h2>Reviews</h2><p>Failed to load reviews: ${res.status}</p>`;
    return;
  }
  const reviews = await res.json();

  // rebuild just the reviews block
  const valid = reviews.filter(r => r.user);
  reviewsEl.innerHTML = '<h2>Reviews</h2>' +
    (valid.length
      ? valid.map(r => `
          <article class="review-card">
            <p><strong>${r.user.first_name} ${r.user.last_name}</strong></p>
            <p>${r.text}</p>
            <p>Rating: ${'★'.repeat(r.rating)}${'☆'.repeat(5-r.rating)}</p>
          </article>`
        ).join('')
      : '<p>No reviews yet.</p>'
    );
}
