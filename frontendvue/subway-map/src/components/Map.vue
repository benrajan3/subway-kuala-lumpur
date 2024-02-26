<template>
    <div class="map-wrap">
      <a href="https://www.maptiler.com" class="watermark"><img
          src="https://api.maptiler.com/resources/logo.svg" alt="MapTiler logo"/></a>
      <div class="map" ref="mapContainer"></div>
    </div>
  </template>
  
  <script>
  import { Map } from 'maplibre-gl';
  import { shallowRef, onMounted, onUnmounted, markRaw } from 'vue';
  import * as maptilersdk from '@maptiler/sdk';
  
  // Research: https://www.youtube.com/watch?v=8DDQ0Pnsd0I
  // API: IOoJQ69k8dO8c7KXGEQd
  export default {
    name: "mainMap",
    setup () {
      const mapContainer = shallowRef(null);
      const map = shallowRef(null);
  
      onMounted(() => {
        const apiKey = 'IOoJQ69k8dO8c7KXGEQd';
  
        const initialState = { lng: 101.6841, lat: 3.1319, zoom: 14 };
  
        map.value = markRaw(new Map({
          container: mapContainer.value,
          style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${apiKey}`,
          center: [initialState.lng, initialState.lat],
          zoom: initialState.zoom
        }));

        const marker = new maptilersdk.Marker().setLngLat([initialState.lng,initialState.lat]).addTo(map)
  
      }),
      onUnmounted(() => {
        map.value?.remove();
      })
  
      return {
        map, mapContainer
      };
    }
  };
  </script>
  
  
  <style scoped>
  @import '~maplibre-gl/dist/maplibre-gl.css';
  
  .map-wrap {
    position: relative;
    width: 100%;
    height: calc(100vh - 77px); /* calculate height of the screen minus the heading */
  }
  
  .map {
    position: absolute;
    width: 100%;
    height: 100%;
  }
  
  .watermark {
    position: absolute;
    left: 10px;
    bottom: 10px;
    z-index: 999;
  }
  </style>