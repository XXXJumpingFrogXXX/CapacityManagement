<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" :class="{ active: activeButton === 'futureDay' }" @click="handleSetLineChartData('futureDay')">
        <!-- <div class="card-panel-icon-wrapper icon-day">
          <svg-icon icon-class="star" class-name="card-panel-icon" />
        </div> -->
        <div class="card-panel-description">
          <div class="card-panel-text">
            未来一天
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" :class="{ active: activeButton === 'futureWeek' }" @click="handleSetLineChartData('futureWeek')">
        <!-- <div class="card-panel-icon-wrapper icon-week">
          <svg-icon icon-class="star" class-name="card-panel-icon" />
        </div> -->
        <div class="card-panel-description">
          <div class="card-panel-text">
            未来一周
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" :class="{ active: activeButton === 'futureHalfMonth' }" @click="handleSetLineChartData('futureHalfMonth')">
        <!-- <div class="card-panel-icon-wrapper icon-month">
          <svg-icon icon-class="star" class-name="card-panel-icon" />
        </div> -->
        <div class="card-panel-description">
          <div class="card-panel-text">
            未来半月
          </div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel" :class="{ active: activeButton === 'futureMonth' }" @click="handleSetLineChartData('futureMonth')">
        <!-- <div class="card-panel-icon-wrapper icon-year">
          <svg-icon icon-class="star" class-name="card-panel-icon" />
        </div> -->
        <div class="card-panel-description">
          <div class="card-panel-text">
            未来一月
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>

export default {
  components: {
  },
  data() {
    return {
      activeButton: 'futureDay'
      // other data
    }
  },
  methods: {
    handleSetLineChartData(type) {
      this.activeButton = type
      this.$emit('handleSetLineChartData', type)
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 5px;
  }

  .card-panel {

    height: 60px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(130, 9, 9, 0.05);
    font-weight: bold;

    .card-panel-text {
      line-height: 60px;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      // color: rgba(0, 0, 0, 0.45);
      font-size: 25px;
    }
    &:hover {
      background: rgba(0, 0, 0, .3);

      .card-panel-description {
        float: right;
        font-weight: bold;
        margin: auto;

        // margin-left: 10px;

        .card-panel-text {
          line-height: 60px;
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          color: rgb(255, 255, 255);
          font-size: 25px;
        }
      }
    }

    // &:active {
    //   background: aqua;

    //   .card-panel-text {
    //     color: rgb(185, 35, 35);
    //   }
    // }

  }
}
.card-panel.active {
  background-color: #3f4e5e;
  color: #fff;
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }

    .card-panel {
      height: auto; // 修改这一行
      display: flex; // 添加这一行
      justify-content: center; // 添加这一行
      align-items: center; // 添加这一行
    }
  }
}</style>
