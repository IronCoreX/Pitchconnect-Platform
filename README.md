# PitchConnect: Elite Turf Booking & Matchmaking Platform

PitchConnect is a comprehensive, mobile-responsive web application designed to solve a real-world logistical problem for athletes: discovering athletic turfs, scheduling time slots, and dynamically organizing matches to ensure enough players are present.

## 📺 Live Video Demonstration

[![Watch the PitchConnect Demo](https://img.youtube.com/vi/k24fM6jyjhs/0.jpg)](https://youtu.be/k24fM6jyjhs)

*Click the image thumbnail above to watch the unlisted video walkthrough demonstrating the asynchronous booking engine, matchmaking lobby, and custom user dashboard.*

---

## 🚀 System Architecture & Core Features

PitchConnect integrates a dynamic, asynchronous frontend with a robust, relational database backend to serve as a **time-based resource allocation engine** and a **transactional social layer**. 

* **Time-Based Resource Allocation:** The core logic revolves around preventing overlapping bookings for finite resources (turfs) on specific dates and times.
* **Transactional Matchmaking Lobby:** Utilizes a Many-to-Many relationship architecture to solve the logistical challenge of assembling a sports team for a previously confirmed booking. Interaction is purposeful and strictly tied to athletic events.
* **Asynchronous Logic (Frontend):** To provide a premium user experience, the application avoids full-page reloads when checking turf availability. Vanilla JavaScript and the Fetch API are used to send asynchronous requests to a Django JSON endpoint. The frontend dynamically renders the DOM to disable already-booked time slots, managing state based on server responses.
* **Database Architecture (Backend):** The backend utilizes complex relational models. A `Booking` relies on a `ForeignKey` to a specific `Turf` and `User`. The application handles atomic transactions: when a user opts to make a booking public via a custom UI toggle, Django simultaneously creates a `Booking` instance and a linked `Match` instance via a `OneToOneField`. The matchmaking engine then utilizes a `ManyToManyField` to manage player rosters, implementing strict validation to prevent over-filling player slots or duplicate entries.
* **State Management & Authentication:** The project bypasses Django's default Admin interface, utilizing a fully custom, branded authentication flow using `AuthenticationForm` and `UserCreationForm`. It features deep linking (capturing the `request.path` as a `?next=` parameter) to seamlessly redirect users back to their intended booking page after logging in. Defensive template design (`{% if user.is_authenticated %}`) ensures that sensitive logic and UI elements are strictly encapsulated from guest users.
* **Data Synchronization:** The backend logic incorporates robust time normalization (converting Python `datetime` objects to standard strings) to ensure perfect synchronization between database storage formats and the frontend JavaScript rendering logic.

---

## 📂 File Contents

### Project Root
* `README.md`: Comprehensive documentation and architecture overview.
* `requirements.txt`: Lists all Python dependencies required to run the application (Django, Pillow).
* `manage.py`: Django's command-line utility for administrative tasks.

### `football_project/` (Project Configuration)
* `settings.py`: Contains standard Django settings, including configurations for static files, media files (`MEDIA_URL` and `MEDIA_ROOT`), and default routing.
* `urls.py`: The master URL configuration, routing base paths to the `pitch_app`.

### `pitch_app/` (Application Logic)
* **`models.py`**: Defines the data schema.
    * `Turf`: Stores venue details, location, pricing, and uploaded images.
    * `Booking`: Links a `User` to a `Turf` for a specific `date` and `start_time`.
    * `Match`: A social wrapper linked to a `Booking` (One-to-One) tracking `required_players` and a roster of joined `players` (Many-to-Many).
* **`views.py`**: Contains the core Python functions handling requests:
    * `index`: Renders the homepage with available turfs.
    * `turf_detail`: Displays specific turf data and the booking interface.
    * `check_availability`: A JSON response view that calculates free time slots against the database.
    * `save_booking`: Processes POST requests to atomically save Bookings and optional Matches.
    * `match_list`: Queries and renders open matches for the social lobby.
    * `join_match`: Handles M2M addition of users to a match roster.
    * `profile`: Utilizes reverse relationships to aggregate a user's schedule.
    * Custom Auth Views: `login_view`, `register_view`, and `logout_view`.
* **`urls.py`**: Maps application routes to their respective views.
* **`admin.py`**: Registers models for the Django superuser interface.

### `pitch_app/templates/pitch_app/` (Frontend)
* `index.html`: The landing page showcasing all available venues.
* `turf_detail.html`: The core interactive page containing the JavaScript booking engine, date picker, and deep-linked authentication gates.
* `matches.html`: The active lobby displaying open games and live roster counts.
* `profile.html`: A custom user dashboard ("Player Card") tracking upcoming sessions and reliability.
* `login.html` & `register.html`: Custom-styled authentication forms.

*Note: All templates utilize Tailwind CSS (via CDN) to maintain a cohesive, mobile-responsive "Dark Mode" aesthetic.*

### `media/`
* Directory designated for storing user-uploaded `Turf` images handled by the Pillow library.

---

## 💻 How to Run the Application

1. Ensure Python 3.x is installed on your local machine.
2. Clone this repository and navigate to the project root directory in your terminal.
3. It is recommended to create a virtual environment:
   * Windows: `python -m venv venv` followed by `.\venv\Scripts\activate`
   * Mac/Linux: `python3 -m venv venv` followed by `source venv/bin/activate`
4. Install the required dependencies: 
   `pip install -r requirements.txt`
5. Apply the database migrations:
   `python manage.py makemigrations`
   `python manage.py migrate`
6. (Optional) Create a superuser to access the admin panel and add Turf data:
   `python manage.py createsuperuser`
7. Start the development server:
   `python manage.py runserver`
8. Open your web browser and navigate to `http://127.0.0.1:8000/`.

---

## 🎨 Additional Information
This application was designed with mobile-responsiveness in mind. To test the responsiveness, use your browser's Developer Tools to toggle device emulation. 

The aesthetic is specifically tailored to a premium "Night Match" feel using Tailwind CSS utility classes, utilizing glassmorphism and high-contrast accents to deliver an immersive user experience.
