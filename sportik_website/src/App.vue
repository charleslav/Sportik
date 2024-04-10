<template>
  <navbar_website/>
  <router-view></router-view>
</template>

<script>
import navbar_website from './components/navbar.vue'

export default {
  name: 'App',
  components: {
    navbar_website
  }
}



</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
