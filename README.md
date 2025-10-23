# Itinero

This is Itinero, a time-Constrained Automatic Itinerary Generator for Effective Travel Planning in Intramuros, Manila
This project is developed and research by three computer science students from Cavite State University Indang Campus.

In an effort to streamline and automate itinerary planning, Itinero proposes an automated generator which plans, searches,
and schedules Places Of Interests (POIs) that dynamically changes based on the time requirements specified by the user.
It uses the Google Maps Places API to search and filter through a list of POIs and then forwards the list to by scheduled 
by a Nearest Neighbor Algorithm. The result is then presented into a GUI that a user can interact with

## Features
* Automatic Itinerary Generator using Flask and Vue
* Explore page with ability to share and discover user made itineraries
* Dynamically changing time boxes depending on POI type and time allottment

## Installation
Before getting started, you must first install the following dependencies:
* [Node.js](https://nodejs.org/en)
* [Python](https://www.python.org/)

1. Navigate to the folder you want to clone to and clone the repository.
`https://github.com/karlo-alano/itinero.git` or `git@github.com:karlo-alano/itinero.git`

2. Navigate to ./frontend/ and download the necesarry dependencies.
`npm install`
After installation, the code should now be editable.

3. To run and test, make the dev server live
`npm run dev`

