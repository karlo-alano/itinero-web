import { defineStore } from 'pinia';
import axios from 'axios'
import router, { routerInstance } from '@/router';

export const useFormStore = defineStore('form', {

  state: () => ({
    currentFormState: {
      startingLocation: null,
      endingLocation: null,
      timeAllotted: null,
      interests: [],
      stops: null,
      distances: [],
      durations: [],
      polyline: null,
      totalDistance: null,
      totalDuration: null
    }

  }),
  getters: {
    startingLocationUppercase() {
      return this.startingLocation.toUpperCase()
    }
  },
  actions: {
    async updateFormData(data) {
      this.currentFormState.startingLocation = data.startingLocation;
      this.currentFormState.endingLocation = data.endingLocation;
      this.currentFormState.timeAllotted = data.timeAllotted;
      this.currentFormState.interests = data.interests;

      this.loading = true;
      this.error = null;

      
      const response = await axios.post('/api', this.currentFormState);
      this.SuccessMessage = response.data.message;
      console.log('Search Results: ', response.data.search_results);
      console.log('Other Places:', response.data.other_results);
      console.log('Distance Matrix:', response.data.distance_matrix)
      console.log("Distance: ", response.data.distances)
      console.log("Durations: ", response.data.durations)
      console.log("Path: ", response.data.path)
      console.log("Total Distance: ", response.data.total_distance)
      console.log("Total Time: ", response.data.total_time)
      console.log("Final_schedule", response.data.final_schedule)
      console.log("Time for activities", response.data.time_for_activities)
      console.log("Segment Duration: ", response.data.segments.durations)
      console.log("Segment Distance", response.data.segments.distances)
      console.log("Polyline: ", response.data.polyline)
      this.currentFormState.stops = response.data.final_schedule
      this.currentFormState.distances = response.data.segments.distances
      this.currentFormState.durations = response.data.segments.durations
      this.currentFormState.polyline = response.data.polyline
      this.currentFormState.totalDistance = response.data.total_distance
      this.currentFormState.totalDuration = response.data.total_time
      
      routerInstance.push('/Dashboard');
        
      // } catch (error) {
      //   this.errorthis.error = error.response.data.error || 'Network error.';
      //   console.error('Error details:', error);
      // } finally {
      //   this.loading = false;
      // }
    },
    resetState () {
      this.$reset();
    }
  } 
});
