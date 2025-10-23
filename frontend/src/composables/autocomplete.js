import { ref } from 'vue';

const startingLocation = ref(null);
const endingLocation = ref(null)

const startingLocationPlaceName = ref(null);
const endingLocationPlaceName = ref(null);

const startPlaceData = ref(null);
const endPlaceData = ref(null);

const selectedPlaceInfo = ref(null);



const mapBounds = {
    north: 14.595836339316302,
    south: 14.584846361895183,
    east: 120.98284688438612,
    west: 120.96558178040564
};

export async function initAutocomplete() {
    // Ensure the input element is mounted before proceeding
    if (!startingLocation.value) {
        console.error("Search input ref is not available.");
        return;
    }

    // 1. Load the 'places' library
    await google.maps.importLibrary("places");

    const startingLocationInput = startingLocation.value.$el; 
    const endingLocationInput = endingLocation.value.$el;
    
    // 2. Create the Autocomplete object, passing the actual HTML input element
    const autocompleteStart = new google.maps.places.Autocomplete(
        startingLocationInput,
        {
            bounds: mapBounds,
            strictBounds: true,
            types: [], 
            fields: ["name", "geometry", "formatted_address", "types", "place_id"]
        }
    );

    autocompleteStart.addListener("place_changed", () => {
        const place = autocompleteStart.getPlace();

        // Check if the place contains valid data
        if (!place.geometry) {
            // User entered text but didn't select a prediction
            startingLocationPlaceName.value = `No details available for input: '${place.name}'`;
            return;
        }

        // Update the reactive state with the selected place data
        startPlaceData.value = {
            name: place.name,
            address: place.formatted_address,
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng(),
            types: place.types,
            place_id: place.place_id
        };
        
        startingLocationPlaceName.value = place.formatted_address; 
        
        console.log("Selected Start Place:", startPlaceData.value);
    });

    const autocompleteEnd = new google.maps.places.Autocomplete(
        endingLocationInput,
        {
            bounds: mapBounds,
            strictBounds: true,
            types: [], 
            fields: ["name", "geometry", "formatted_address", "types", "place_id"]
        }
    );

    autocompleteEnd.addListener("place_changed", () => {
        const place = autocompleteEnd.getPlace();

        // Check if the place contains valid data
        if (!place.geometry) {
            // User entered text but didn't select a prediction
            endingLocationPlaceName.value = `No details available for input: '${place.name}'`;
            return;
        }

        // Update the reactive state with the selected place data
        endPlaceData.value = {
            name: place.name,
            address: place.formatted_address,
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng(),
            types: place.types,
            place_id: place.place_id
        };
        
        // FIX 2: Assign the READABLE ADDRESS to the v-model ref (endingLocationPlaceName)
        endingLocationPlaceName.value = place.formatted_address;

        console.log("Selected End Place:", endPlaceData.value);
    });
}

export function useAutocomplete() {
    return {
            startingLocation,
            endingLocation,
            startingLocationPlaceName,
            endingLocationPlaceName,
            startPlaceData,
            endPlaceData,
            initAutocomplete
    }

}

