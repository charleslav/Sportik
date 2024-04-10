<script setup>
const props = defineProps(["keys","infos"])


</script>

<template>
  <router-link to="/item" class="product-card">
    <img :src="props.infos.product_image" :alt="props.infos.product_name">
    <div class="product-details">
      <h2>{{ props.infos.product_name }}</h2>
      <p>{{ props.infos.description }}</p>
      <p>Price: ${{ props.infos.price }}</p>
      <button @click="$emit('addproducts', props.infos)">Add to Cart</button>
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
