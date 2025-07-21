document.addEventListener('DOMContentLoaded', initPlacesList);

async function initPlacesList() {
  const container = document.getElementById('places-list');
  try {
    // 1. Fetch places from your API
    const res = await fetch('http://localhost:5000/api/v1/places');
    if (!res.ok) {
      throw new Error(`Server responded ${res.status}`);
    }
    const places = await res.json();

    console.log('Fetched places:', places);
    console.log('Number of places:', Array.isArray(places) ? places.length : 'not an array');

    // 2. For each place, create and append a card
    places.forEach(place => {
      console.log('Place keys:', Object.keys(place), 'full object:', place);
      const card = document.createElement('article');
      card.className = 'place-card';
      card.innerHTML = `
        <img src="${place.image_url || 'https://via.placeholder.com/300x150'}" alt="${place.title}">
        <div class="card-body">
          <h3>${place.title}</h3>
          <p class="price">$${place.price}/night</p>
          <button class="details-button"
                  onclick="window.location.href='place.html?id=${place.id}'">
            View Details
          </button>
        </div>`;
      container.append(card);
    });
  } catch (err) {
    console.error('Error fetching places:', err);
    container.innerHTML = '<p>Unable to load places at the moment.</p>';
  }
}
