-- --------------------------------------------------
-- scripts/initial_data.sql
-- --------------------------------------------------

-- 0) Make sure uuid-ossp is available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1) Administrator user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  'Admin',
  'HBnB',
  'admin@hbnb.io',
  '$2b$12$0pjs5wSmwB2ka08AF9KbE.xgnlZ9R0iO6FjtiOKDuIQggwtstJRMK',
  true
);

-- 2) Owner user (non-admin)
--    Replace <OWNER_HASH> with a bcrypt hash of "ownerpass"
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
  uuid_generate_v4()::text,
  'Owner',
  'User',
  'owner@hbnb.io',
  '$2b$12$0pjs5wSmwB2ka08AF9KbE.xgnlZ9R0iO6FjtiOKDuIQggwtstJRMK',
  false
);

-- 3) Initial Amenities
INSERT INTO amenities (id, name) VALUES
  (uuid_generate_v4()::text, 'WiFi'),
  (uuid_generate_v4()::text, 'Swimming Pool'),
  (uuid_generate_v4()::text, 'Air Conditioning');

-- 4) One sample Place (owned by that Owner)
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
  uuid_generate_v4()::text,
  'Sample Cottage',
  'A very cozy sample cottage',
  120.00,
  42.3601,
  -71.0589,
  -- pull the owner’s UUID we just inserted
  (SELECT id FROM users WHERE email = 'owner@hbnb.io')
);

-- 5) One sample Review (Admin reviews it)
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
  uuid_generate_v4()::text,
  'Loved the stay! Highly recommended.',
  5,
  '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
  (SELECT id FROM places WHERE title = 'Sample Cottage')
);

-- 6) Link “WiFi” amenity to that place
INSERT INTO place_amenity (place_id, amenity_id)
VALUES (
  (SELECT id FROM places WHERE title = 'Sample Cottage'),
  (SELECT id FROM amenities WHERE name = 'WiFi')
);
