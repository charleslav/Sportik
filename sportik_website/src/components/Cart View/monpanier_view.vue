

<script setup>
import { inject, onMounted, ref } from 'vue'
import Cookies from 'js-cookie'
import router from '@/router'
const hostname = inject("$hostname");
let cartItems = ref([]);
let isDeuteranopia = Cookies.get("deuteranopia") === "true"

onMounted(async () => {

  await fetchCarts()

})


async function removeFromCart(item) {

  if (Cookies.get("user_token")) {
    await fetch(`${hostname}/user/${Cookies.get("user_token")}/cart/${item.brand_model_id}`, {
      method: "DELETE",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).then((response) => {
      return response.json()
    }).then((data) => {
      console.log(data)
    }).catch((error) => {
      console.log(error)
    })
    await fetchCarts()
  }else{
    alert("You are not connected")
  }

}

const updateQuantity = (index) => {
  // Ensure quantity is a positive integer
  if (cartItems.value[index].quantity < 1 || isNaN(cartItems.value[index].quantity)) {
    cartItems.value[index].quantity = 1;
  }
};

async function onClickQuantity(item){
  //console.log(item.image)
  await fetch(`${hostname}/cart/quantity`, {
    method: "PUT",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body:JSON.stringify({
      token: Cookies.get("user_token"),
      bmid: item.brand_model_id,
      quantity: item.quantity
    })
  }).then((response) => {
    return response.json()
  }).then((data) => {
    console.log(data)
  })
}

async function fetchCarts(){
  if (Cookies.get("user_token")){

    await fetch(`${hostname}/cart/${Cookies.get("user_token")}`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).then((response) => {
      return response.json()
    }).then((data) => {
      console.log(data.cart)
      if (data.status === 401){
        alert(data.message)
      }else if(data.status === 200){
        cartItems.value = data.cart;
      }
    }).catch((error) => {
      console.log(error)
    })
  }else{
    alert("You are not connected")
  }

}



const pay = () => {
  // Logic for payment (e.g., redirect to payment page)
  //alert('Redirecting to payment page...');
  router.push("checkout")
};
</script>

<template>
  <div class="my-cart">
    <h2>My Cart</h2>
    <div v-if="cartItems.length === 0">
      <p>Your cart is empty.</p>
    </div>
    <div v-else>
      <ul>
        <li v-for="(item, index) in cartItems" :key="index">
          <img :src="item.image" alt="Product Image" style="width: 50px; height: 50px; margin-right: 10px;" :class="{deuteranopia : isDeuteranopia}">
          <div>
            <span>{{ item.brand_model_name }}</span><br>
            <span>Price: ${{ item.price }}</span><br>
            <span>Quantity: <input type="number" v-model="item.quantity" min="1" :max="item.stock" @input="updateQuantity(index)" @click="onClickQuantity(item)" class="quantity-input"></span>
          </div>
          <button @click="removeFromCart(item)">Remove</button>
        </li>
      </ul>
      <button @click="pay" v-if="cartItems.length > 0">Pay</button>
    </div>
  </div>
</template>


<style>
.my-cart {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.quantity-input {
  width: 50px; /* Adjust the width as needed */
}

button {
  margin-left: auto;
  padding: 5px 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
