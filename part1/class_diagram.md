```mermaid
classDiagram
    class User {
        +UUID4 id
        +datatime created_at
        +datatime updated_at
        +String name
        +String email
        +String password_hash
        +createPlace()
        +submitReview()
        +getPlaces()
    }

    class Place {
        +UUID4 id
        +datetime created_at
        +datetime updated_at
        +String title
        +String description
        +float price
        +String location
        +UUID4 owner_id
        +addReview()
        +addAmenity()
        +getReviews()
        +getAmenities()
    }

    class Review {
        +UUID4 id
        +datetime created_at
        +datetime updated_at
        +String text
        +int rating
        +UUID4 user_id
        +UUID4 place_id
        +editReview()
    }

    class Amenity {
        +UUID4 id
        +datetime created_at
        +datetime updated_at
        +String name
        +String description
        +assignToPlace
    }

    %% Relationships
    User "1" -- "0..*" Place : owns >
    Place "1" -- "0..*" Review : has >
    Place "1" -- "0..*" Amenity : includes >
    Amenity "1" -- "0..*" Place : available_in >

    Review "1" -- "1" User : written_by >
    Review "1" -- "1" Place : about >
