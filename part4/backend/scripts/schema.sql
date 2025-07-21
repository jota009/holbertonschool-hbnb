-- --------------------------------------------------
-- HBnB Database Schema
-- --------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users
CREATE TABLE users (
  id          CHAR(36)    PRIMARY KEY,
  first_name  VARCHAR(255) NOT NULL,
  last_name   VARCHAR(255) NOT NULL,
  email       VARCHAR(255) NOT NULL UNIQUE,
  password    VARCHAR(255) NOT NULL,
  is_admin    BOOLEAN      NOT NULL DEFAULT FALSE
);

-- Places
CREATE TABLE places (
  id          CHAR(36)      PRIMARY KEY,
  title       VARCHAR(255)  NOT NULL,
  description TEXT,
  price       DECIMAL(10,2) NOT NULL,
  latitude    FLOAT         NOT NULL,
  longitude   FLOAT         NOT NULL,
  owner_id    CHAR(36)      NOT NULL,
  CONSTRAINT fk_place_owner
    FOREIGN KEY(owner_id) REFERENCES users(id)
);

-- Reviews
CREATE TABLE reviews (
  id        CHAR(36) PRIMARY KEY,
  text      TEXT     NOT NULL,
  rating    INT      NOT NULL CHECK (rating BETWEEN 1 AND 5),
  user_id   CHAR(36) NOT NULL,
  place_id  CHAR(36) NOT NULL,
  CONSTRAINT fk_review_user
    FOREIGN KEY(user_id)  REFERENCES users(id),
  CONSTRAINT fk_review_place
    FOREIGN KEY(place_id) REFERENCES places(id),
  CONSTRAINT uq_user_place_review
    UNIQUE(user_id, place_id)
);

-- Amenities
CREATE TABLE amenities (
  id   CHAR(36)     PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

-- Place ↔ Amenity (many-to-many)
CREATE TABLE place_amenity (
  place_id   CHAR(36) NOT NULL,
  amenity_id CHAR(36) NOT NULL,
  PRIMARY KEY(place_id, amenity_id),
  CONSTRAINT fk_pa_place
    FOREIGN KEY(place_id)   REFERENCES places(id),
  CONSTRAINT fk_pa_amenity
    FOREIGN KEY(amenity_id) REFERENCES amenities(id)
);
