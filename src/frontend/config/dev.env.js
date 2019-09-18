'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  BACKEND: '"http://127.0.0.1:5000/api"',
  GRAPHS: '"http://127.0.0.1:5000/graphs/"'
})
