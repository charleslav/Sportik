<template>
  <router-link :to="'/information/' + props.bmid" class="model-card">
    <img :src="props.infos.image" :alt="props.infos.brand_name">
    <div class="product-details">
      <h2>{{ props.infos.brand_model_name }}</h2>
    </div>
  </router-link>
</template>

<script setup>
const props = defineProps(["bmid", "infos"]);
</script>

<style scoped>
.model-card {
  display: inline-block;
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  width: 300px;
  text-decoration: none;
  color: black;
  transition: transform 0.3s ease;
  align-content: center;
}

.model-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
}

.model-card img {
  width: 100%;
  border-radius: 8px 8px 0 0;
}

.product-details {
  padding: 10px;
}

.product-details h2 {
  margin-top: 0;
  font-size: 18px;
}

.product-details p {
  margin-bottom: 0;
  font-size: 14px;
}
</style>
