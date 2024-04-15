<script setup>
import { inject, onMounted, ref } from 'vue';
import Cookies from 'js-cookie';


const props = defineProps(["brandModelId"]);
const hostname = inject("$hostname");
const infosBrandModel = ref({});


const reviews = ref([]);
const newReview = ref({ user: '', rating: 5, comment: '' });
let isAdded = ref(false)

const quantity = ref(1); // 1 as default quantity

async function submitReview(){
  // Access $function directly from globalProperties


  if (Cookies.get("user_token")){
  await fetch(`${hostname}/review`, {
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },

    body: JSON.stringify({
      customer_token: Cookies.get("user_token"),
      brand_model_id: props.brandModelId,
      comment: newReview.value.comment,
      rating: newReview.value.rating
    })
  }).then( (response) => {
    return response
  }).then( (data) => {
    console.log(data.status)
  })
  }else{
    alert("Veuillez vous connecter")
  }

  await fetchReview()
}

onMounted( async () => {
  //await Promise.all([
  //  fetchInformation(), fetchReview()
  //]);
  await fetchInformation()
  await fetchReview()
});

const addToCart = async () => {


  await fetch(`${hostname}/cart`, {
    method: "POST",
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      token: Cookies.get("user_token"),
      bmid: Number(props.brandModelId),
      quantity : quantity.value
    })
  }).then( (response) => {
    return response.json()
  }).then((response_data) => {
    if (response_data.status === 401) {
      alert(response_data.message)
    }else if(response_data.status === 200){
      isAdded.value = true;
    }
  })




}

async function fetchInformation() {
  return fetch(`${hostname}/information/${props.brandModelId}`,{
    method: "GET",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then( (response) => {
    return response.json()
  }).then( (data) => {
    if (data.status === 200){
      infosBrandModel.value = data.modelData;
      console.log(data.modelData)
    }
  });
}

async function fetchReview() {
  return fetch(`${hostname}/review/${props.brandModelId}`, {
    method:"GET",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then( (response) => {
    return response.json()
  }).then( (data) => {
    if (data.status === 200) {
      reviews.value = data.reviews
      console.log(data)
    }
  });
}
</script>



<template>
  <div class="item-details">

    <h2>{{ infosBrandModel.brand_model_name }}</h2>
    <div class="brand-info">

      <div class="brand-image">
        <img :src="infosBrandModel.image" alt="Brand Image">
      </div>

      <div class="brand-details">
        <p><strong>Brand:</strong> {{ infosBrandModel.brand_name }}</p>
        <p><strong>Description:</strong> {{ infosBrandModel.description }}</p>
        <p><strong>Price:</strong> ${{ infosBrandModel.price }}</p>
        <p><strong>Rating:</strong> {{ infosBrandModel.brand_rating }}</p>

        <p v-if="infosBrandModel.isInStock" class="status"><strong>Status:</strong> <span class="in-stock">In Stock</span></p>
        <p v-else class="status"><strong>Status:</strong> <span class="out-of-stock">Out of Stock</span></p>

        <div>
          <label for="quantity">Quantity:</label>
          <input v-model="quantity" id="quantity" type="number" min="1" :max="infosBrandModel.quantity">
        </div>
        <label v-if="isAdded">Your product was added, great job !</label>
        <div>
          <button class="add-to-cart-button" @click="addToCart">Add to Cart</button>
        </div>
        
      </div>
    </div>
    <!-- Review section -->
    <div class="reviews">
      <h3>Product Reviews</h3>
      <div v-if="reviews.length === 0">
        <p>No reviews yet. Be the first to leave a review!</p>
      </div>
      <div v-else>
        <div v-for="(review, index) in reviews" :key="index" class="review">
          <p><strong>User:</strong> {{ review.user }}</p>
          <p><strong>Rating:</strong> {{ review.brand_rating_review }}/5</p>
          <p>{{ review.comment }}</p>
        </div>
      </div>
      <!-- Review form -->
      <div class="review-form">
        <h4>Leave a Review</h4>
        <input v-model="newReview.rating" type="number" min="1" max="5" placeholder="Rating (1-5)">
        <textarea v-model="newReview.comment" placeholder="Your Review"></textarea>
        <button @click="submitReview">Submit Review</button>
      </div>
    </div>
  </div>
</template>



<style scoped>
.item-details {
  max-width: 800px;
  margin: 8vh auto;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
}

h2 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.brand-info {
  display: flex;
  align-items: flex-start;
}

.brand-image img {
  width: 200px;
  height: auto;
  margin-right: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.brand-details p {
  margin-bottom: 10px;
  font-size: 16px;
  color: #555;
}

.brand-details strong {
  font-weight: bold;
  color: #333;
}

.brand-details p:last-child {
  margin-bottom: 0;
}

.status {
  font-size: 18px;
  margin-top: 10px;
}

.status strong {
  color: #555;
}

.status .in-stock {
  color: #28a745;
}

.status .out-of-stock {
  color: #dc3545;
}

.add-to-cart-button {
  margin-top: 2rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-to-cart-button:hover {
  background-color: #0056b3;
}

.add-to-cart-button:focus {
  outline: none;
}


.reviews {
  margin-top: 40px;
}

.reviews h3 {
  font-size: 24px;
  margin-bottom: 20px;
}

.review {
  margin-bottom: 20px;
}

.review p {
  margin-bottom: 5px;
}

.review-form {
  margin-top: 30px;
}

.review-form h4 {
  font-size: 20px;
  margin-bottom: 15px;
}

.review-form input,
.review-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.review-form button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.review-form button:hover {
  background-color: #0056b3;
}

.review-form button:focus {
  outline: none;
}

</style>
