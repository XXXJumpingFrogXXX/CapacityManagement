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
    setOptions({ expectedData, expectedUpperData, expectedLowerData, actualData, expectedDataXAxis, actualStatus } = {}) {
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
          data: ['expected', 'actual', 'expectedUpperData', 'expectedLowerData']
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
              color: '#00D300',
              lineStyle: {
                color: '#00D300',
                width: 1
              },
              areaStyle: {
                color: '#FFFFFF'
              }
            }
          },
          smooth: true,
          type: 'line',
          data: expectedData,
          animationDuration: 2800,
          animationEasing: 'cubicInOut'
        },
        {
          name: 'actual',
          smooth: false,
          type: 'scatter',
          symbol: 'circle',
          symbolSize: 2,
          itemStyle: {
            normal: {
              color: function (params) {
                if (actualData != null) {
                  if (actualStatus[params.dataIndex] === 'too high') {
                    // console.log('red');
                    return 'red';
                  } else if (actualStatus[params.dataIndex] === 'too low') {
                    return 'red';
                  } else {
                    return '#B8DEFF';
                  }

                } else {
                  return '#B8DEFF';
                }

              },
            }
          },
          emphasis: {
            // 设置标记为三角形
            symbol: 'triangle',
            // 设置三角形标记的大小
            symbolSize: 6
          },
          symbol:'triangle',

          data: actualData,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }, {
          name: 'expectedUpperData',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#FFB8E6',
              lineStyle: {
                color: '#FFB8E6',
                width: 2
              },
              areaStyle: {
                color: '#F8FFE7',
                opacity: 0.6 // 设置填充透明度
              }
            }
          },
          data: expectedUpperData,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        },
        {
          name: 'expectedLowerData',
          smooth: true,
          type: 'line',
          itemStyle: {
            normal: {
              color: '#FFD4B7',
              lineStyle: {
                color: '#FFD4B7',
                width: 2
              },
              areaStyle: {
                color: '#FFFFFF',
                opacity: 1 // 设置填充透明度
              }
            }
          },
          data: expectedLowerData,
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }]
      })
    }
  }
}
</script>
