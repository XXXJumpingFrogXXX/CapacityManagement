<template>
  <div class="dashboard-editor-container">
    <div class="title">
      <span class="title-head">容量预测</span>
      <div class="title-select">
        <!-- 文件索引选择下拉框 -->
        <el-dropdown class="avatar-container" trigger="click">
          <div class="avatar-wrapper">
            <span class="user-avatar"> {{ this.files[fileIndex] }}</span>
            <i class="el-icon-caret-bottom" />
          </div>
          <el-dropdown-menu slot="dropdown" class="user-dropdown">
            <el-dropdown-item v-for="(filename, index) in this.files" :key="index" @click.native="switchFile(index)">
              {{ filename }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <el-row class="chart-container">
      <!-- 使用 LineChart 组件显示图表 -->
      <line-chart :chart-data="lineChartData" />
    </el-row>
    <panel-group @handleSetLineChartData="handleSetLineChartData" />
  </div>
</template>


<script>
import axios from 'axios'
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'

const lineChartData = {
  allData: {
    expectedData: [],
    actualData: [],
    expectedDataXAxis: []
  },
  anomalyData: [

  ]
}

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    LineChart
  },
  data() {
    return {
      fileIndex: 0,
      files: ['test-aiops-hbase-203', 'test-bpfp-bs-engine2-ft', 'test-rr_offline_qf_cluster'],
      lineChartData: lineChartData.allData,
      anomalyData: []
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initData()
    })
  },
  methods: {
    initData() {
      this.switchFile(0)
      this.handleSetLineChartData('futureDay')
      this.lineChartData = lineChartData.allData
      console.log(this.lineChartData)
    },
    handleSetLineChartData(type) {
      //向后端发送需要的预测时间步长-3.1
      axios.post(`http://localhost:5000/sheet_period`, { sheet_time: type }).then(res => {
        console.log('正在获取目标数据...'),
        lineChartData.allData.expectedData = res.data.all_data.predict,
        lineChartData.allData.actualData = res.data.all_data.actual,
        lineChartData.allData.expectedDataXAxis = res.data.all_data.date,
        console.log('all_data获取成功...')
      }).catch(error => {
        if (error.response.status === 400) { console.log('出错了') }
      })
    },
    switchFile(index) {
      this.fileIndex = index
      console.log('点击了集群 ' + this.fileIndex + ' 的文件')
      axios.post(`http://localhost:5000/predict`, { sheet_num: index }).then(res => {
        //向后端发送需要的文件索引-3.1
        console.log('正在获取目标数据...'),
        lineChartData.allData.expectedData = res.data.all_data.predict,
        lineChartData.allData.actualData = res.data.all_data.actual,
        lineChartData.allData.expectedDataXAxis = res.data.all_data.date,
        console.log('all_data获取成功...'),
        console.log('anomaly获取成功...')
      }).catch(error => {
        if (error.response.status === 400) { console.log('出错了') }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;
}

.chart-container {
  background-color: #fff;
  padding: 16px;
  margin-bottom: 10px;
}

.title {
  height: 70px;
  // overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, .08);
  padding: 20px;

  .title-head {
    font-size: 24px;
    height: 100%;
    // margin-top: 25px;
    width: 20%;
    // background-color: aqua;
    // border-style: dashed;
    // border-width: 5px;
    // border-color: rgb(86, 16, 77);
  }

  .title-select {
    float: right;
    height: 100%;
    // line-height: 50px;
    &:focus {
      outline: none;
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        // margin-top: 5px;
        position: relative;

        .user-avatar {
          font-size: 24px;
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 10px;
          font-size: 12px;
        }

      }

    }

  }
}
.alarm-title{
  text-align: center;
  font-size: x-large;
  height: 70px;
  // overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, .08);
  padding: 20px;

}
.el-dropdown-menu {
  max-height: 200px;
  /* 设置最大高度 */
  max-width: 200px;
}
</style>
