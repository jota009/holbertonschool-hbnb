/**
 * Reads a cookie by name; returns its value or null if missing.
 */
function getCookie(name) {
  const match = document.cookie.match(
    new RegExp('(?:^|; )' + name.replace(/([$?*|{}()[\]\\/+^])/g,'\\$1') + '=([^;]*)')
  );
  return match ? decodeURIComponent(match[1]) : null;
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  const placesList = document.getElementById('places-list');
  const token = getCookie('access_token');
 // ── Show / hide login vs logout ────
 if (loginLink)  loginLink.style.display  = token ? 'none' : 'inline-block';
 if (logoutLink) logoutLink.style.display = token ? 'inline-block' : 'none';

 // ── Wire up the logout click ───
 if (logoutLink) {
   logoutLink.addEventListener('click', ev => {
     ev.preventDefault();
     // Clear the cookie
     document.cookie = 'access_token=; path=/; max-age=0';
     // Redirect to login page
     window.location.href = 'login.html';
   });
 }

 // ── If on login.html, handle that form and stop ────────
 if (loginForm) {
   loginForm.addEventListener('submit', handleLogin);
   return;
 }

 // ── Protect other pages: if no token, go to login ──────
 if (!token) {
   window.location.href = 'login.html';
   return;
 }

 // ── If this is index.html, initialize the places list ─
 if (placesList) {
   initPlacesList();
 }

 // ── (You can add place.html and add_review.html initializers here)
});

/**
 * 1-LOGIN HANDLER
 */
async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  try {
    const res = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json' },
      body: JSON.stringify({email, password})
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || res.statusText);

    const { access_token } = data;
    // Store JWT in a cookie
    document.cookie = `access_token=${access_token}; path=/`;
    // Redirect to the main page
    window.location.href = 'index.html';

  } catch (err) {
    console.error('Login error:', err);
    alert('Login failed: ' + err.message);
  }
}

/**
 * Renders an array of place objects into the #places-list container.
 */
function renderPlaces(list) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';      // clear old cards
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
  const filterEl  = document.getElementById('price-filter');
  const token = getCookie('access_token');

  try {
    // 1. Fetch places from your API
    const res    = await fetch('http://localhost:5000/api/v1/places/',{
      headers: token
        ? { 'Authorization': `Bearer ${token}`}
        : {}
    });
    if (!res.ok) throw new Error(`Server responded ${res.status}`);
    const places = await res.json();

    // added to test back to index
    if(!token) {
      window.location.href='login.html'
      return;
    }
    console.log('Fetched places:', places);
    console.log('Number of places:', places.length);

    //  TEMPORARILY USE FIXED PRICE OPTIONS, THIS DYNAMIC OPTION CAN BE CHOSEN LATER
    //const prices = [...new Set(places.map(p => p.price))].sort((a, b) => a - b);
    //filterEl.innerHTML =
    //  '<option value="">All</option>' +
    //  prices.map(p=> `<option value="${p}">$${p}</option>`).join('');

    filterEl.innerHTML = `
      <option value="">ALL</option>
      <option value="10">$10</option>
      <option value="50">$50</option>
      <option value="100">$100</option>
    `;

    // 3. Initial render of all places
    renderPlaces(places);

    // 4. On dropdown change → filter & re-render
    filterEl.addEventListener('change', () => {
      const max = Number(filterEl.value);
      const subset = filterEl.value
        ? places.filter(p => p.price <= max)
        : places;
      renderPlaces(subset);
    });

  } catch (err) {
    console.error('Error fetching places:', err);
    document.getElementById('places-list')
      .innerHTML = '<p>Unable to load places at the moment.</p>';
  }
}
