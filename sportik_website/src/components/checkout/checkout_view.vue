<template>
  <div class="checkout">
    <!-- Left Column: Checkout Form -->
    <div class="left-column">
      <div class="checkout-form">
        <h1>Checkout</h1>

        <!-- Billing Information -->
        <h2 v-if="!useAccountInfo">Billing Information</h2>
        <div class="form-group" v-if="!useAccountInfo">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="billingInfo.name">
        </div>
        <div class="form-group" v-if="!useAccountInfo">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="billingInfo.email">
        </div>

        <!-- Shipping Information
        <h2 v-if="!useAccountInfo">Shipping Information</h2>
        <div class="form-group" v-if="!useAccountInfo">
          <label for="address">Address:</label>
          <input type="text" id="address" v-model="shippingInfo.address">
        </div>-->

        <!-- Account Information Checkbox -->
        <div class="form-group">
          <input type="checkbox" id="accountInfo" v-model="useAccountInfo">
          <label for="accountInfo">With my account information</label>
        </div>

        <!-- Payment Information -->
        <h2>Payment Information</h2>
        <select v-model="paymentInfo.payment_method" id="payments">
          <option value="Bank Card">Bank Card</option>
          <option value="Credit Card">Credit Card</option>
          <option value="In Cash">In Cash</option>
        </select>

        <!-- Error Message -->
        <p v-if="formError" class="error-message">{{ formError }}</p>

      </div>
    </div>

    <!-- Right Column: Cart Details -->
    <div class="right-column">
      <h2 class="cart-title">Cart</h2>
      <div v-if="cartIsEmpty">Your cart is empty</div>
      <div v-else>
        <!-- Cart Items -->
        <div v-for="(product, index) in cartItems" :key="index" class="cart-item">
          <img :src="product.image" alt="Product Image" class="cart-item-image">
          <div class="cart-item-details">
            <div>{{ product.name }}</div>
            <div>Quantity: {{ product.quantity }}</div>
            <div>Subtotal: ${{ productSubtotal(product) }}</div>
          </div>
        </div>

        <!-- Subtotal Taxes and Discount -->
        <div class="taxes-discount">
          <div>SubTotal: ${{ checkoutValue.order_total }}</div>
          <div>Taxes: ${{ checkoutValue.tax_price }}</div>
          <div>Discount: ${{ checkoutValue.total_discount }}</div>
        </div>

        <!-- Total -->
        <div class="total">Total: ${{ checkoutValue.total_price }}</div>

        <!-- Place Order Button -->
        <div class="submit-button">
          <button @click="validateAndPlaceOrder" class="btn-primary">Place Order</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import Cookies from 'js-cookie'
import router from '@/router'
const hostname = inject("$hostname");

// Reactive variables
const billingInfo = reactive({
  name: '',
  email: ''
});

const paymentInfo = reactive({
  payment_method: ''
});

const useAccountInfo = ref(false);

// Cart items
let cartItems = ref([]);
let checkoutValue = ref({})

// Error message
const formError = ref('');

const cartIsEmpty = computed(() => cartItems.value.length === 0);

// Fetch cart data on component mount
onMounted(async () => {
  await fetchCheckout();
  await fetchCarts();
});

// Fetch checkout data
async function fetchCheckout() {
  if (Cookies.get("user_token")) {
    const response = await fetch(`${hostname}/user/${Cookies.get("user_token")}/checkout`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    if (data.status === 401) {
      alert(data.message);
    } else if (data.status === 200) {
      checkoutValue.value = data.checkout_data;
      console.log(data.checkout_data)
    }
  } else {
    alert("You are not connected");
  }
}

// Fetch cart data
async function fetchCarts() {
  if (Cookies.get("user_token")) {
    const response = await fetch(`${hostname}/cart/${Cookies.get("user_token")}`, {
      method: "GET",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    if (data.status === 401) {
      alert(data.message);
    } else if (data.status === 200) {
      cartItems.value = data.cart;
    }
  } else {
    alert("You are not connected");
  }
}

async function fetchPlaceorder() {
  if (Cookies.get("user_token")) {
    const response = await fetch(`${hostname}/user/${Cookies.get("user_token")}/place_order`, {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({

        payment_method: paymentInfo.payment_method
      })

    });

    const data = await response.json();
    if (data.status === 401) {
      alert(data.message);
    } else if (data.status === 200) {
      alert("Order placed")
      router.push("/")
    }
  } else {
    alert("You are not connected");
  }
}

// Calculate product subtotal
function productSubtotal(product) {
  return product.price * product.quantity;
}

// Place order function
async function placeOrder() {
  await fetchPlaceorder()
  console.log('Placing order...');
}

// Validation and place order
function validateAndPlaceOrder() {
  if (!useAccountInfo.value) {
    if (!billingInfo.name.trim() || !billingInfo.email.trim() ||
      !paymentInfo.payment_method.trim()) {
      formError.value = 'Please fill in all required fields.';
      return;
    }
  } else {
    if (!paymentInfo.payment_method.trim()) {
      formError.value = 'Please fill in all required fields.';
      return;
    }
  }

  formError.value = ""
  placeOrder();
}
</script>

<style scoped>

.checkout {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.left-column {
  flex: 1;
}

.right-column {
  flex: 1;
}

.checkout-form {
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.submit-button {
  text-align: center;
  margin-top: 4rem;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.cart-item {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.cart-item-image {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.cart-item-details {
  text-align: left;
}

.cart-title {
  text-align: center;
}

.total {
  font-weight: bold;
  text-align: center;
}

.taxes-discount {
  margin-bottom: 20px;
  text-align: center;
}

.error-message {
  color: red;
}
</style>
