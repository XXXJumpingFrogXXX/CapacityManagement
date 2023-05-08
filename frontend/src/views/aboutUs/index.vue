<template>
    <div class="about-us">
      <div class="about-us-section">
        <img src="../../assets/nankai_images/logo.png" style="display: flex; justify-content: center; align-items: center;"/>
        <h1 class="page-title">关于我们</h1>
        <div class="about-us-section">
          <h2 class="section-title">我们的团队成员</h2>
          <ul class="value-list">
            <li>2012155 孙亚萱</li>
            <li>2012289 王麒翔</li>
            <li>2013030 董赛天</li>
          </ul>
        </div>
      </div>
      <div class="about-us-section">
        <h2 class="section-title">关于项目</h2>
        <p class="section-description">我们的项目是南开大学软件学院软件测试与维护课程的课程项目。我们的项目基于Prophet算法模型，通过对基础数据的预测与分析，使用vue框架和element-ui组件，完成了可以对容量管理和动态阈值告警功能进行可视化的Web界面。</p>
      </div>

    </div>
  </template>
  <style scoped>
  
    .about-us {
      padding: 40px;
      max-width: 960px;
      margin: 0 auto;
    }
    .about-us img {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 250px;
      height: auto;
      margin: 20px 0;
    }
    
    .page-title {
      font-size: 36px;
      margin-bottom: 40px;
      text-align: center;
    }
  
    .about-us-section {
      margin-bottom: 40px;
    }
  
    .section-title {
      font-size: 24px;
      margin-bottom: 20px;
    }
  
    .section-description {
      font-size: 18px;
      line-height: 1.5;
      margin-bottom: 20px;
    }
  
    .value-list {
      font-size: 18px;
      line-height: 1.5;
      list-style: disc;
      margin-left: 40px;
    }
  
    .value-list li {
      margin-bottom: 10px;
    }
  </style>