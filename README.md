# ITINERO

## Technical Documentation

### Version

1.0

### Project Type

Web-Based Smart Travel Itinerary Planning System

---

# 1. Introduction

## 1.1 Project Overview

Itinero is a web-based itinerary planning platform designed to help users create optimized travel schedules based on their interests, available time, and preferred destinations.

The system integrates Google Maps services, route optimization algorithms, and attraction data to automatically generate efficient travel itineraries. Users can explore destinations, customize schedules, manage accounts, and view optimized routes through an interactive map interface.

---

# 2. Objectives

The primary objectives of the system are:

* Generate optimized travel itineraries automatically
* Minimize travel time between destinations
* Improve tourist planning efficiency
* Provide route visualization through Google Maps
* Support itinerary customization and management
* Offer personalized recommendations based on user preferences

---

# 3. System Architecture

The system follows a three-tier architecture.

## Presentation Layer

Frontend application built using:

* Vue 3
* Vite
* PrimeVue
* Tailwind CSS
* Vue Router
* Pinia

Responsibilities:

* User Interface
* User Authentication
* Route Visualization
* Itinerary Management
* Data Presentation

---

## Application Layer

Backend application built using:

* Flask
* Python

Responsibilities:

* Business Logic
* Route Computation
* Itinerary Optimization
* API Communication
* Data Processing

---

## Data Layer

Storage technologies:

* Supabase
* JSON Data Store

Responsibilities:

* User Data Storage
* Itinerary Storage
* Cached Establishment Information
* Store Operating Hours

---

# 4. Technology Stack

## Frontend

* Vue 3
* Vite
* PrimeVue
* Tailwind CSS
* Pinia
* Axios
* Vue Router
* VeeValidate
* Yup

## Backend

* Python
* Flask
* Flask-CORS
* PuLP Optimization Library

## External APIs

### Google Places API

Used for:

* Nearby Place Search
* Attraction Discovery
* Establishment Information

### Google Routes API

Used for:

* Route Computation
* Travel Time Calculation
* Distance Matrix Generation

### Google Maps JavaScript API

Used for:

* Interactive Maps
* Route Visualization
* Marker Placement

## Database

* Supabase
* JSON Cache Database

---

# 5. Functional Modules

## 5.1 User Management Module

Features:

* User Registration
* User Login
* Account Management
* Password Updates
* User Settings

Related Views:

* Registration.vue
* Account.vue
* Settings.vue
* UpdatePassword.vue

---

## 5.2 Itinerary Generation Module

Core functionality of the system.

Input:

* Starting Location
* Available Time
* User Interests
* Ranking Preferences

Processing:

* Attraction Filtering
* Travel Time Calculation
* Route Optimization
* Schedule Generation

Output:

* Optimized Travel Plan
* Route Information
* Destination Sequence

---

## 5.3 Route Optimization Module

Implemented in the backend using mathematical optimization techniques.

Responsibilities:

* Minimize travel distance
* Maximize destination coverage
* Respect user time constraints
* Optimize visitation sequence

Optimization Engine:

* PuLP

---

## 5.4 Mapping Module

Responsible for:

* Displaying destinations
* Route rendering
* Interactive navigation
* Marker management

Main Component:

* Map.vue

---

## 5.5 Explore Module

Allows users to:

* Browse attractions
* Discover destinations
* View location information

Related View:

* Explore.vue

---

## 5.6 Dashboard Module

Provides:

* Saved itineraries
* Recent activities
* User travel information

Related View:

* Dashboard.vue

---

# 6. Backend Design

## Flask Application

Main backend file:

```text
backend/app.py
```

Responsibilities:

* Receive itinerary requests
* Process user preferences
* Query Google APIs
* Execute optimization algorithms
* Return itinerary results

---

## API Integration

The backend communicates with:

### Google Places API

Purpose:

* Retrieve nearby attractions
* Obtain place details

### Google Route Matrix API

Purpose:

* Compute travel durations
* Calculate distances

### Google Directions API

Purpose:

* Generate route paths
* Create navigation routes

---

# 7. Database Design

## Cached Establishment Database

File:

```text
database/storeHours.json
```

Contains:

* Attraction Information
* Store Hours
* Categories
* Ranking Data

Benefits:

* Reduced API requests
* Faster response times
* Improved reliability

---

# 8. Frontend Design

## Routing Structure

Views identified within the system:

* Home
* About
* Explore
* Create Itinerary
* Dashboard
* Account
* Settings
* Blog
* Itinerary Edit
* Registration
* Loading Screen

---

## Reusable Components

Major UI components include:

* Navbar
* Mobile Navbar
* Sidebar
* Map
* Autocomplete Fields
* Account Tabs

Benefits:

* Code Reusability
* Easier Maintenance
* Consistent User Experience

---

# 9. Security Considerations

Implemented Measures:

* Environment Variables for API Keys
* Cross-Origin Resource Sharing (CORS) Configuration
* User Authentication through Supabase
* Secure API Communication

Recommended Improvements:

* Rate Limiting
* JWT Refresh Token Rotation
* Request Validation Middleware
* API Usage Monitoring

---

# 10. System Workflow

1. User accesses the platform.
2. User enters preferences and trip details.
3. Frontend sends request to Flask backend.
4. Backend retrieves attraction information.
5. Travel distances and durations are computed.
6. Optimization algorithm generates itinerary.
7. Results are returned to the frontend.
8. Optimized route is displayed on Google Maps.
9. User saves or edits itinerary.

---

# 11. Future Enhancements

* AI-powered destination recommendations
* Real-time traffic integration
* Multi-day itinerary planning
* Group travel optimization
* Budget-aware itinerary generation
* Weather-aware route planning
* Mobile application deployment
* Recommendation engine using machine learning

---

# 12. Conclusion

Itinero is a smart itinerary planning system that combines route optimization, mapping technologies, and travel recommendation features into a single platform. By integrating Google Maps services, optimization algorithms, and modern web technologies, the system provides users with efficient and personalized travel planning experiences.
