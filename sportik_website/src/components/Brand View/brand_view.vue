<template>

  <div class="home">
    <h1>Welcome to Our Shoes Shopping Website</h1>
    <p>Check out our latest collection!</p>
    <!-- Search bar -->
    <div class="input-container">
      <input type="text" v-model="searchQuery" placeholder="Search products..." class="search-input">
    </div>
    <!-- Products display -->
    <div class="products">
      <!-- Example product cards -->
      <card v-for="brand in filteredBrands"
            :key="brand.bid"
            :infos="brand"
            :bid="brand.bid"></card>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import card from "./brand_card.vue"

let isConnected = sessionStorage.getItem("isConnected")
let brands = ref([]);
let searchQuery = ref('');

onMounted(async () => {
  console.log("isConnected:", isConnected);


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
  }).catch((error) => {
    console.log(error)
  })
}

const filteredBrands = computed(() => {
  return brands.value.filter(brand => {
    return brand.brand_name.toLowerCase().includes(searchQuery.value.toLowerCase());
  });
});
</script>

<style scoped>
/* Styling for the search bar */
.input-container {
  margin-bottom: 20px; /* Add some space between the search bar and the products */
}

.search-input {
  width: 300px;
  height: 40px;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ccc; /* Add a border */
  border-radius: 5px; /* Add rounded corners */
}

.search-input:focus {
  outline: none; /* Remove default focus outline */
  border-color: #007bff; /* Change border color when focused */
}

/* Styling for the products container */
.home {
  text-align: center;
}

.products {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
