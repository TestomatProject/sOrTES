<template>
  <embed id="svg-obj" style="width:100%;" ref="obj" type="image/svg+xml" :src="data" />
</template>

<script>
import svg_pan_zoom from 'svg-pan-zoom'

export default {
  name: 'SVGZoomer',
  props: {
    data: null,
    id: 'svg-obj'
  },
  mounted () {
    document.getElementById('svg-obj').addEventListener('load', () => {
      // Will get called after embed element was loaded
      svg_pan_zoom(document.getElementById('svg-obj'), { minZoom: 0.001, fit: false })
    })
  }
}
</script>
