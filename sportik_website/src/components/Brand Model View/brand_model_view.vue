<script setup>
import { onMounted, ref } from 'vue'
import card from './brand_model_card.vue'

const props = defineProps(['brandId'])

let brand_model_list = ref([])


onMounted(async () => {
  await fetchBrandModel()
})


async function fetchBrandModel() {
  fetch('http://127.0.0.1:5000/brands/' + props.brandId, {
    method: 'get',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }

  }).then((response) => {
    return response.json()
  }).then((data) => {
    if (data.status === 200) {
      brand_model_list.value = data.brandModel
    }
  })
}
</script>

<template>
  <div class="model">
    <card v-for="brand_model in brand_model_list"
          :key="brand_model.bmid"
          :bmid="brand_model.bmid"
          :infos="brand_model"></card>
  </div>

</template>

<style scoped>
.model {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
</style>