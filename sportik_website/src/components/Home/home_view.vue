<script setup>
import { onMounted, ref } from 'vue'
import card from "./category_card.vue"

let products = ref([]);

onMounted(async () => {
  await fetchProducts();
})

async function fetchProducts(){
  fetch("http://127.0.0.1:5000/products", {
    method:"get",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

  }).then( (response) => {
    return response.json()
  }).then( (data) => {
    if (data.status === 200){
      products.value = data.products;
      console.log(products.value)
    }
  })
}

function addToCart(product) {
   //Add logic to add product to cart
  console.log("Product added to cart:", product);
}
</script>


<template>
  <div class="home">
    <h1>Welcome to Our Clothes Shopping Website</h1>
    <p>Check out our latest collection!</p>
    <div class="products">
      <!-- Example product cards -->
      <card v-for="product in products"
            :key="product.pid"
            :infos="product"
            @addproducts="addToCart"></card>
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