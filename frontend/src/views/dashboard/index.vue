<template>
  <div class="dashboard-editor-container">
    <div class="title">
      <span class="title-head">容量预测</span>
      <div class="title-select">
        <el-dropdown class="avatar-container" trigger="click">
          <div class="avatar-wrapper">
            <span class="user-avatar">集群 {{ fileIndex }}</span>
            <i class="el-icon-caret-bottom"></i>
          </div>
          <el-dropdown-menu slot="dropdown" class="user-dropdown">
            <el-dropdown-item v-for="(filename, index) in this.files" :key="index" @click.native="switchFile(index+1)">{{
              filename }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <el-row class="chart-container">
      <line-chart :chart-data="lineChartData" />
    </el-row>
    <panel-group @handleSetLineChartData="handleSetLineChartData" />
    <hr>
    <div class="alarm">
      <div class="alarm-title">集群{{this.fileIndex}}告警数据表</div>
      <br>
      <alarm-table :alarm-data="anomalyData" class="alarm-table"></alarm-table>
    </div>
    
    
  </div>
</template>

<script>
import axios from "axios";
import PanelGroup from './components/PanelGroup'
import LineChart from './components/LineChart'
import AlarmTable from './components/AlarmTable'

const lineChartData = {
  allData:{
    expectedData: [],
    actualData: [],
    expectedLowerData: [],
    expectedUpperData: [],
    actualStatus:[],
    expectedDataXAxis: []
  },
  anomalyData:[

  ],
  futureHour: {
    expectedData: [100, 250, 242, 456, 232, 864],
    actualData: [120, 82, 91, 154, 162, 140, 145],
    expectedDataXAxis: [20221025, 20221026, 20221027, 20221028, 20221029, 20221030, 20221031],
    actualStatus: [0, 1, 2, 0, 0, 1, 0]
  },
  futureDay: {
    expectedData: [200, 192, 120, 144, 160, 130, 140, 400],
    actualData: [180, 160, 151, 106, 145, 150, 130, 500],
    expectedDataXAxis: [20221024, 20221025, 20221026, 20221027, 20221028, 20221029, 20221030, 20221031],
    actualStatus: [0, 1, 2, 0, 0, 1, 2, 1]
  },
  futureWeek: {
    expectedData: [80, 100, 121, 104, 105, 90, 100, 400, 500],
    actualData: [120, 90, 100, 138, 142, 130, 130, 500, 600],
    expectedDataXAxis: [20221023, 20221024, 20221025, 20221026, 20221027, 20221028, 20221029, 20221030, 20221031],
    actualStatus: [0, 1, 2, 0, 0, 1, 1, 1, 2]
  },
  futureMonth: {
    expectedData: [130, 140, 141, 142, 145, 150, 160],
    actualData: [120, 82, 91, 154, 162, 140, 130],
    expectedDataXAxis: [20221025, 20221026, 20221027, 20221028, 20221029, 20221030, 20221031],
    actualStatus: [0, 1, 2, 0, 0, 1, 1]
  }
}

export default {
  name: 'DashboardAdmin',
  components: {
    PanelGroup,
    LineChart,
    AlarmTable
  },
  data() {
    return {
      fileIndex: 1,
      files: ['集群1', '集群2', '集群3', '集群4', '集群5', '集群6', '集群7', '集群8', '集群9', '集群10','集群11', '集群12', '集群13', '集群14', '集群15'],
      lineChartData: lineChartData.allData,
      anomalyData:[]
    }
  },
  mounted(){
    this.$nextTick(() => {
      this.initData()
    })
  },
  methods: {
    initData(){
      this.switchFile(1)
      this.handleSetLineChartData('futureDay')
      this.lineChartData = lineChartData.allData
      console.log(this.lineChartData)
    },
    handleSetLineChartData(type) {
      axios.post(`http://localhost:5000/period`, { time: type }).then(res => {
        console.log('正在获取目标数据...'),
        lineChartData.allData.expectedData=res.data.all_data.predict,
        lineChartData.allData.actualData=res.data.all_data.raw_data,
        lineChartData.allData.expectedLowerData=res.data.all_data.predict_lower,
        lineChartData.allData.expectedUpperData=res.data.all_data.predict_upper,
        lineChartData.allData.actualStatus=res.data.all_data.status,
        lineChartData.allData.expectedDataXAxis=res.data.all_data.date,
        console.log('all_data获取成功...')
      }).catch(error => {
        if (error.response.status === 400)
          console.log('出错了')
      });
    },
    switchFile(index) {
      this.fileIndex = index;
      console.log('点击了集群 ' + this.fileIndex + ' 的文件');
      axios.post(`http://localhost:5000/data`, { num: index }).then(res => {
        console.log('正在获取目标数据...'),
        lineChartData.allData.expectedData=res.data.all_data.predict,
        lineChartData.allData.actualData=res.data.all_data.raw_data,
        lineChartData.allData.expectedLowerData=res.data.all_data.predict_lower,
        lineChartData.allData.expectedUpperData=res.data.all_data.predict_upper,
        lineChartData.allData.ActualStatus=res.data.all_data.status,
        lineChartData.allData.expectedDataXAxis=res.data.all_data.date,
        console.log('all_data获取成功...'),
        this.anomalyData=res.data.outliner,
        console.log('anomaly获取成功...')
      }).catch(error => {
        if (error.response.status === 400)
          console.log('出错了')
      });
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
  overflow-y: scroll;
  /* 显示垂直滚动条 */
}
</style>