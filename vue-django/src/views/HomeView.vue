<template>
  <div class="container py-5">
    <div class="row mb-4">
      <div class="col-12">
        <label for="currency-select">Seleccionar divisa:</label>
        <select id="currency-select" v-model="selectedCurrency">
          <option value="CLP">CLP</option>
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>

        </select>
      </div>
    </div>
    <div class="row">
      <div v-for="producto in productos" :key="producto.id_producto" class="col-12 col-sm-6 col-md-4 col-lg-3 mb-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ producto.nomb_producto }}</h5>
            <p class="card-text mt-auto text-end">{{ formatPrice(producto.precio_producto) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',

  data() {
    return {
      productos: [],
      indicadores: {},
      loading: true,
      selectedCurrency: 'CLP',
    }
  },

  mounted() {
    this.fetchProducts();
    this.fetchIndicadores();
  },

  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/productos/');
        this.productos = response.data;
      } catch (error) {
        console.error('Error al obtener los productos:', error);
      }
    },

    async fetchIndicadores() {
      try {
        const response = await axios.get('https://mindicador.cl/api');
        this.indicadores = response.data;
      } catch (error) {
        console.error('Error al obtener los indicadores:', error);
      } finally {
        this.loading = false;
      }
    },


    formatPrice(price) {
      if (typeof price !== 'number') {
        price = parseFloat(price);
      }
      if (isNaN(price)) {
        return 'N/A';
      }

      const currency = this.selectedCurrency;
      if (currency === 'USD') {
        return (price / this.indicadores.dolar.valor).toFixed(2) + ' USD';
      } else if (currency === 'EUR') {
        return (price / this.indicadores.euro.valor).toFixed(2) + ' EUR';
      } else {
        return price.toFixed(2) + ' CLP';
      }
    }
  }
};
</script>