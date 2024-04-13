<script setup>
const props = defineProps(["bid","infos"])


</script>

<template>
  <router-link :to="'/brand_model/' + props.bid" class="product-card">
    <img :src="props.infos.brand_image" :alt="props.infos.brand_name">
    <div class="product-details">
      <h2>{{ props.infos.brand_name }}</h2>
    </div>
  </router-link>
</template>

<style scoped>
.product-card {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
  transition: background-color 0.3s ease; /* Add transition effect */
  cursor: pointer; /* Change cursor to hand */
  text-decoration: none;
  color: black;
}

.product-card:hover {
  background-color: lightgray; /* Change color on hover */
}

.product-card img {
  width: 100%;
  border-radius: 5px;
}

.product-details {
  margin-top: 10px;
}
</style>
