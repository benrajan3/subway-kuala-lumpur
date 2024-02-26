<template>
    <div class="header">
        <div class="logo">
            <img src="../../subway-logo-2.jpg" alt="Subway Logo" class="subwayLogo">
        </div>
        <div class="heading">
            <h1>Subway Kuala Lumpur Locations</h1>
        </div>
    </div>
</template>

<script>
    export default {
    name: 'mainNavbar'
    }
</script>

<style scoped>
    .header {
    display: flex;
    align-items: center; 
    background-color: #028940;
    color: #FFC20D;
    }

    .logo {
    margin-right: 10px; 
    }

    .subwayLogo {
    width: 200px;
    height: auto; /* Automatically adjust height to maintain aspect ratio */
    }


    .heading > h1 {
    padding: 20px;
    margin: 0;
    }
</style>
