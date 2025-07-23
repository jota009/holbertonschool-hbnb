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
  // If not on login.html, check for token
  if (!loginForm) {
    const token = getCookie('access_token');
    if (!token) {
      // no token -> bounce to login
      window.location.href = 'login.html';
      return;
    }
  }
  // If on login.html wire up the form
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
    return;
  }
  // Otherwise we must be on index.html or ...
  if (document.getElementById('places-list')) {
    initPlacesList();
  }
  // place.html and add-review later
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
  try {
    // 1. Fetch places from your API
    const res    = await fetch('http://localhost:5000/api/v1/places');
    if (!res.ok) throw new Error(`Server responded ${res.status}`);
    const places = await res.json();

    console.log('Fetched places:', places);
    console.log('Number of places:', places.length);

    // 2. Build the Max-Price dropdown
    const prices = [...new Set(places.map(p => p.price))].sort((a, b) => a - b);
    filterEl.innerHTML =
      '<option value="">All</option>' +
      prices.map(p => `<option value="${p}">$${p}</option>`).join('');

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
