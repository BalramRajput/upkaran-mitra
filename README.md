# UpkaranMitra
#### Video Demo:  https://youtu.be/jAn0FTnIskQ
#### Description:
UpkaranMitra is a community-driven platform designed to address a common problem faced by farmers—the high costs of acquiring farming equipment. Often, farmers require specific tools or machines for short durations, making the outright purchase of such equipment impractical and expensive. UpkaranMitra bridges this gap by providing a platform where farmers can borrow and lend farming equipment among themselves, fostering resource-sharing and reducing costs. By connecting equipment owners and borrowers, the project promotes sustainability and collaboration within farming communities.

This platform is developed using HTML, CSS, JavaScript, Python, Flask, Jinja, and SQLite, ensuring a robust and user-friendly experience for its users.

#### Main Use Cases:
UpkaranMitra offers several key functionalities that make equipment sharing seamless:

1. Search Equipment by Category: Farmers can easily search for the equipment they need by category, such as tractors, plows, sprayers, or harvesters.

2. Booking Equipment: Users can book equipment listed by others for specified durations. This feature ensures the availability of equipment when needed.

3. Manage Bookings: Borrowers can view and manage their active and past bookings. Lenders can track who has borrowed their equipment and for how long.

4. Add User Equipment: Farmers with surplus equipment can list their tools or machines on the platform, making them available for others to borrow.

5. User Management: Farmers can register, log in, and can provide essential details about themselves and their equipment.

#### Important Files:

app.py

This is the entry point of the application. It initializes the Flask app, sets up routes, and manages configurations. It ensures the seamless integration of various components like templates and static files.

database.py

This module handles database interactions. It includes utility functions for connecting to the SQLite database, executing queries, and managing transactions. It ensures the application can store and retrieve data efficiently.

routes/…

This directory contains route handlers that manage application logic for different features:

    __init__.py: Initializes the routes module for Flask.

    bookings.py: Handles endpoints related to booking equipment, including viewing, creating, and managing bookings.

    equipments.py: Manages functionality for adding, updating, and retrieving equipment details.

    users.py: Handles user registration, login, and profile management.

sql/…

This directory manages the database schema and initial data:

    base_schema.sql: Defines the database schema, including tables for users, equipment, and bookings.

    upkaranmitra.db: The SQLite database file storing all project data.

    master_seeds/: Contains seed data to populate the database with initial values like country and villages data.

templates/…

Contains HTML templates rendered by Flask:

    base.html: The master layout for other templates, providing a consistent structure.

    index.html: The homepage of the platform, showcasing featured equipment and navigation.

    add_equipments.html: The form for users to add their equipment.

    login.html and register.html: Provide interfaces for user authentication.

    my_bookings.html and my_equipments.html: Allow users to view and manage their bookings and listed equipment.

static/…

Holds static assets like CSS and JavaScript files:

    css/: Includes stylesheets like base.css for common styles and my_equipments.css for specific pages.

    js/: Contains JavaScript files for client-side interactivity, such as search.js for dynamic equipment search and booking.js for handling booking workflows.

UpkaranMitra aims to empower farmers by building a collaborative and sustainable farming community.
