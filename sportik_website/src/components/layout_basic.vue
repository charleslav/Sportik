<script setup>






</script>

<template>
  <div class="navbar">
    <router-link to="/" class="nav-link">Home</router-link>
    <router-link to="/services" class="nav-link">services</router-link>
    <router-link to="/contact" class="nav-link">contact</router-link>
    <router-link to="/register" class="register-icon"><i class="fas fa-user-plus"></i></router-link>
    <router-link to="/login" class="sign-in-icon"><i class="fas fa-sign-in-alt"></i></router-link>

    <router-link to="/cart" class="cart-icon"><i class="fas fa-shopping-cart"></i></router-link>
  </div>
  <router-view></router-view>
</template>

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

.sign-in-icon,
.user-icon,
.register-icon,
.cart-icon {
  float: right;
  padding: 14px 10px; /* Adjusted padding */
  color: #FFFCF2;
}

i {
  font-size: 18px;
}
</style>
