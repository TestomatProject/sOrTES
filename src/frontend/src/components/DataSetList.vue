<template>
  <div>
    <v-list>
      <v-list-tile v-if="loading">
        <v-list-tile-content>
          <div class="text-xs-center" style="width:100%;">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile v-for="item in items" :key="item" :to="{ name: 'DataSetOverview', params: { dataSet: item }}">
        <v-list-tile-content>
          <v-list-tile-title>
            {{ item }}
          </v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
    <v-container>
      <h3>Add new</h3>
      <v-form v-model="valid" ref="form" lazy-validation>
          <v-text-field
            label="Name"
            v-model="name"
            :rules="nameRules"
            required
          ></v-text-field>
          <v-btn
            @click="createNewDataSet"
            :disabled="!valid"
          >Add</v-btn>
      </v-form>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import router from '../router'

export default {
  name: 'DataSetList',

  data: () => ({
    items: [],
    name: '',
    nameRules: [
      v => !!v || 'Name is required'
    ],
    loading: false,
    valid: false
  }),

  methods: {
    getDataSets () {
      this.loading = true
      axios.get(this.path)
        .then(res => {
          this.items = res.data
          this.loading = false
        })
    },
    createNewDataSet () {
      if (this.$refs.form.validate()) {
        // Native form submission is not yet supported
        axios
          .post(this.path, {
            name: this.name
          })
          .then(res => {
            this.items.push(res.data)
            this.name = ''
          })
      }
    },

    navigateToDataSet (dataSet) {
      router.push({ name: 'DataSet', params: { dataSet: dataSet } })
    }
  },

  created () {
    this.path = process.env.BACKEND + '/data_sets'
    this.getDataSets()
  }
}
</script>
