# HBnB – Part 4: Frontend (HTML/CSS/JS)

A lightweight, framework-free frontend that consumes the HBnB REST API.

## 🎯 Goals
- Provide a simple, accessible UI to **browse places**, **view details**, and **interact with reviews**.
- Implement **authentication** with a smooth login/register flow using **JWT** (stored as a cookie).
- Keep the stack minimal (HTML/CSS/JS) to highlight **API integration** and **state handling**.

## 🗂️ What’s Included
- **Pages**
  - **Home / Places list**: shows available places; supports basic filtering ideas (price, city, amenity).
  - **Place detail**: title, description, price, location, amenities, existing reviews; add a review when logged in.
  - **Auth pages**: login and registration; logout control in the header.
  - Optional static pages: About, Contact.
- **State & Feedback**
  - **Loading** indicators while fetching.
  - **Empty** states when nothing matches.
  - **Error** messages surfaced from the API.
- **Auth UX**
  - After login, a JWT is stored as a cookie and used for protected actions.
  - Header toggles **Login/Logout** visibility based on auth state.
- **Accessibility & Responsiveness**
  - Semantic HTML, labeled forms, keyboard-friendly navigation.
  - Responsive layout using simple flex/grid patterns.

## 🔌 How It Works (High Level)
1. The frontend reads a **base API URL** from a small config file.
2. All requests are sent to the backend; if you’re logged in, the JWT cookie is attached automatically.
3. Pages render data returned by the API and update the UI according to loading/empty/error states.

## ▶️ Running the Frontend
- Serve the `frontend/` folder as **static files** (any simple static server works).
- Ensure the **backend API is running** and the **base API URL** in the frontend config points to it.
- Open the site in your browser and sign up / log in to try protected actions (e.g., add a review).

## 🧪 Testing & Validation
- **Manual checks** in the browser (Network tab, error states, auth toggling).
- Recommended future additions:
  - **E2E testing** with Playwright/Cypress.
  - **Accessibility checks** (e.g., Lighthouse, axe).
  - **Smoke tests** for key flows: login → view places → open detail → add review.

## 🛣️ Future Enhancements
- Client-side routing for SPA-like navigation.
- Pagination and advanced filters.
- User profiles and bookings.
- Image upload & galleries.
- Componentization or migration to a framework if needed.

## 🤝 Requirements
- Any static server to host the frontend.
- Running backend API (Parts 2–3).
- Correct API base URL configured in the frontend.

## 🧑‍💻 Author
**Josniel Ramos**
