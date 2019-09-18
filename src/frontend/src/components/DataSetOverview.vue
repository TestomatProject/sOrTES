<template>
  <v-container
    fluid
    style="min-height: 0;"
    grid-list-lg
  >
    <v-layout row wrap>
      <v-flex xs12>
        <v-alert type="error" :value="true" v-if="notFound">
          Data set not found!
        </v-alert>
        <v-alert type="error" :value="true" v-if="error && !notFound">
          Something went wrong when fetching the data set!
        </v-alert>
        <v-card color="blue-grey darken-2" class="white--text" v-if="!error">
         <v-card-title primary-title>
           <div class="headline">{{ $route.params.dataSet }}</div>
         </v-card-title>
         <v-card-text v-if="loading">
           <div class="text-xs-center" style="width:100%;">
             <v-progress-circular indeterminate color="primary"></v-progress-circular>
           </div>
         </v-card-text>
        </v-card>
     </v-flex>
     <v-flex xs12>
       <v-card color="light-blue darken-1" class="white--text" v-if="!error && !loading">
          <v-card-title primary-title>
            <div class="headline">Source File</div>
          </v-card-title>
          <v-card-text>
            Handle the source file of this data set
          </v-card-text>
          <v-card-actions>
            <input
              ref="source"
              type="file"
              name="source"
              id="source"
              v-if="!dataSet.hasFile">

            <v-btn
              color="success"
              @click="upload"
              v-if="!dataSet.hasFile">Upload</v-btn>

              <v-btn
                color="warning"
                @click="removeFiles"
                v-if="dataSet.hasFile">Delete</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
      <v-flex xs12>
        <v-card v-if="!loading && dataSet.hasFile">
          <v-card-title>
            <div class="headline">Dependency Structure</div>
          </v-card-title>
          <v-card-text>
            <SVGZoomer v-if="showGraph" :data="graphsPath + $route.params.dataSet + '.svg?dummy=' + getRandom()"></SVGZoomer>
          </v-card-text>
          <v-card-actions>
            <v-btn color="success" @click="showGraph = !showGraph">Toggle graph</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
      <v-flex xs12 v-if="!loading && dataSet.hasFile">
        <schedule-shower :dataSet="dataSet.name"></schedule-shower>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
import SVGZoomer from './SVGZoomer'
import ScheduleShower from './ScheduleShower'

export default {
  components: {
    SVGZoomer,
    ScheduleShower
  },
  data () {
    return {
      notFound: false,
      error: false,
      loading: false,
      dataSet: null,
      source: null,
      showGraph: false
    }
  },
  methods: {
    getDataSetURL () {
      return this.path + this.$route.params.dataSet
    },
    getRandom () {
      return Math.random()
    },
    upload (e) {
      e.preventDefault()
      let files = this.$refs.source.files
      let data = new FormData()

      data.append('source', files[0])

      axios.post(this.getDataSetURL(), data)
        .then(res => {
          this.dataSet = res.data
        })
        .catch(err => {
          console.log(err.response)
        })
    },

    removeFiles () {
      axios.delete(this.getDataSetURL())
        .then(res => {
          this.dataSet = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },

    getDataSet () {
      this.loading = true

      axios.get(this.getDataSetURL())
        .then(res => {
          this.dataSet = res.data
          this.error = false
          this.notFound = false
          this.loading = false
        })
        .catch(err => {
          this.error = true
          this.loading = false
          this.notFound = err.response.status === 404
        })
    }
  },
  watch: {
    '$route.params.dataSet': function (dataSet) {
      this.getDataSet()
    }
  },
  created () {
    this.path = process.env.BACKEND + '/data_sets/'
    this.graphsPath = process.env.GRAPHS
    this.getDataSet()
  }
}
</script>
