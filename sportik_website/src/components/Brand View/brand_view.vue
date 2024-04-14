<script setup>
import { onMounted, ref } from 'vue'
import card from "./brand_card.vue"

let isConnected = sessionStorage.getItem("isConnected")//inject("$isConnected")
let brands = ref([]);

onMounted(async () => {
  console.log("isConnected:", isConnected); // Logging isConnected after it might have been updated
  await fetchBrands();
})

async function fetchBrands(){
  fetch("http://127.0.0.1:5000/brands", {
    method:"get",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

  }).then( (response) => {
    return response.json()
  }).then((data) => {
    if (data.status === 200) {
      brands.value = data.brands;
      console.log(brands.value)
    }
  })
}
</script>

<template>
  <div class="home">
    <h1>Welcome to Our Clothes Shopping Website</h1>
    <p>Check out our latest collection!</p>
    <div class="products">
      <!-- Example product cards -->
      <card v-for="brand in brands"
            :key="brand.bid"
            :infos="brand"
            :bid="brand.bid"></card>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
}

.products {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
