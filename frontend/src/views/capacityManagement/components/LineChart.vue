<template>
  <div :class="className" :style="{ height: height, width: width }">
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '../mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '500px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
      console.log(this.chartData)
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
    },
    resetZoom() {
      myChart.setOption({
        dataZoom: {
          start: 0,
          end: 100
        }
      });
    },
    setOptions({ expectedData, actualData,expectedDataXAxis } = {}) {
      this.chart.setOption({
        xAxis: {
          data: expectedDataXAxis,
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 50,
          bottom: 50,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          }
        },
        legend: {
          data: ['expected', 'actual']
        },
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            start: 0,
            end: 100,
            filterMode: 'empty'
          },
          {
            type: 'inside',
            xAxisIndex: 0,
            start: 0,
            end: 100,
            filterMode: 'empty'
          },
          {
            type: 'slider',
            yAxisIndex: 0,
            start: 0,
            end: 100,
            filterMode: 'empty'
          },
          {
            type: 'inside',
            yAxisIndex: 0,
            start: 0,
            end: 100,
            filterMode: 'empty'
          }]
        ,
        series: [{
          name: 'expected',
          itemStyle: {
            normal: {
              color: '#FF9000',
              lineStyle: {
                color: '#FF9000',
                width: 1
              },
            }
          },
          // smooth: true,
          type: 'line',
          data: expectedData,
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        },
        {
          name: 'actual',
          smooth: false,
          type: 'line',
          symbol: 'circle',
          symbolSize: 2,
          itemStyle: {
            normal: {
              color:'#006CD4',
            }
          },
          emphasis: {
            symbol: 'triangle',
            symbolSize: 6
          },
          symbol: 'triangle',

          data: actualData,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        ]
      })
    }
  }
}
</script>
