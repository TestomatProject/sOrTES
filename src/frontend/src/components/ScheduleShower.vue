<template>
  <v-card>
    <v-card-title>
     <div class="headline">Schedule</div>
     <v-spacer></v-spacer>
     <v-text-field
       append-icon="search"
       label="Search"
       single-line
       hide-details
       v-model="search"
     ></v-text-field>
    </v-card-title>

    <v-data-table
      :headers="headers"
      :items="items"
      :loading="loading"
      item-key="name"
      :search="search"
    >
      <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>
      <template slot="items" slot-scope="props">
        <tr v-bind:class="{ 'error': !props.item.canBeExecuted }">
          <td @click="props.expanded = !props.expanded">{{ props.item.name }}</td>
          <td class="text-xs-right">{{ props.item.priority }}</td>
          <td class="justify-center layout px-0">
            <v-btn icon class="mx-0" :disabled="!props.item.canBeExecuted" @click="addToPassedTests(props.item)">
              <v-icon>play_circle_filled</v-icon>
            </v-btn>
          </td>
        </tr>
      </template>
      <template slot="expand" slot-scope="props">
        <v-card flat>
          <v-card-text>
            <strong>Time</strong>: {{ props.item.time }}<br/>
            <strong>Score</strong>: {{ props.item.score }}<br/>
          </v-card-text>
        </v-card>
      </template>
    </v-data-table>
    <v-card-actions>
      <v-btn color="primary" dark class="mb-2" :disabled="passedTests.length == 0" @click="resetPassedTests()">Reset Schedule</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    dataSet: null
  },
  data () {
    return {
      search: '',
      headers: [
        {
          text: 'Name',
          value: 'name',
          sortable: false
        },
        {
          text: 'Priority',
          value: 'priority',
          align: 'right'
        }
      ],
      items: [],
      passedTests: [],
      loading: false
    }
  },

  methods: {
    getDataSetURL () {
      return this.path + this.dataSet + '/schedule'
    },

    loadSchedule () {
      this.loading = true
      axios.post(this.getDataSetURL(), { passedTests: this.passedTests })
        .then(res => {
          this.items = res.data.schedule
          this.passedTests = res.data.passedTests
        })
        .catch(err => console.log(err))
        .finally(() => {
          this.loading = false
        })
    },

    resetPassedTests () {
      this.passedTests = []
      this.loadSchedule()
    },

    addToPassedTests (test) {
      this.passedTests.push(test.name)
      this.loadSchedule()
    }
  },

  created () {
    this.path = process.env.BACKEND + '/data_sets/'
    this.loading = true
    if (window.localStorage) {
      if (localStorage.getItem('passedTests_' + this.dataSet) !== null) {
        this.passedTests = JSON.parse(localStorage.getItem('passedTests_' + this.dataSet))
      } else {
        this.passedTests = []
      }
    } else {
      this.passedTests = []
    }

    this.$watch('passedTests', passedTests => {
      if (window.localStorage) {
        localStorage.setItem('passedTests_' + this.dataSet, JSON.stringify(this.passedTests))
      }
    })

    this.loadSchedule()
  }
}
</script>
