import Vue from 'vue'
import Router from 'vue-router'
import Start from '@/components/Start'
import DataSetOverview from '@/components/DataSetOverview'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Start',
      component: Start
    },
    {
      path: '/data_set/:dataSet',
      name: 'DataSetOverview',
      component: DataSetOverview
    }
  ]
})
