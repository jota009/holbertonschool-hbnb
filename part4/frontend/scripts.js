document.addEventListener('DOMContentLoaded', initPlacesList);

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
