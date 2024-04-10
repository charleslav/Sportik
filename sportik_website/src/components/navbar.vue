<template>
  <div class="navbar">
    <router-link to="/" class="nav-link">Home</router-link>
    <router-link to="/femme" class="nav-link">Femme</router-link>
    <router-link to="/services" class="nav-link">Homme</router-link>
    <router-link to="/contact" class="nav-link">Enfant</router-link>
    <router-link to="/auth" class="sign-in-icon" ><i class="fas fa-sign-in-alt"></i></router-link>
  </div>
</template>

<script>
export default {
  name: 'navbar_website',
}
</script>

<style scoped>
.navbar {
  background-color: #252422;
  overflow: hidden;
}

.nav-link {
  float: left;
  display: block;
  color: #FFFCF2;
  text-align: center;
  padding: 14px 20px;
  text-decoration: none;
}

.nav-link:hover {
  background-color: #CCC5B9;
  color: #403D39;
}

.nav-link.router-link-exact-active {
  background-color: #EB5E28;
}

.sign-in-icon {
  float: right;
  padding: 14px 20px;
  color: #FFFCF2;
}

.sign-in-icon i {
  font-size: 18px;
}
</style>
