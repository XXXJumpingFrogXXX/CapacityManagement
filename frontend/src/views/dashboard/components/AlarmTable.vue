<template>
  <el-table
    v-loading="listLoading"
    :data="list"
    element-loading-text="Loading"
    border
    fit
    highlight-current-row
    max-height="800"
    height="800"
    append-to-body
    width="100%"
  >
    <el-table-column align="center" label="ID" width="200">
      <template slot-scope="scope">
        {{ scope.row.id }}
      </template>
    </el-table-column>

    <el-table-column align="center" prop="created_at" label="Display_time" width="auto">
      <template slot-scope="scope">
        <i class="el-icon-time" />
        <span>{{ scope.row.ds }}</span>
      </template>
    </el-table-column>

    <el-table-column align="center" label="Value" width="auto">
      <template slot-scope="scope">
        {{ scope.row.raw_data }}
      </template>
    </el-table-column>

    <el-table-column class-name="status-col" label="Status" width="auto" align="center">
      <template slot-scope="scope">
        <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
      </template>
    </el-table-column>

  </el-table>
</template>

<script>
import axios from 'axios'
import { getList } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      //告警状态
      const statusMap = {
        'normal': 'success',
        'too low': 'gray',
        'too high': 'danger'
      }
      return statusMap[status]
    }
  },
  props: {
    alarmData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      list: null,
      listLoading: true
    }
  },
  watch: {
    alarmData: {
      deep: true,
      handler(val) {
        this.listLoading = true,
        this.list = this.alarmData
        this.listLoading = false
      }
    }

  },
  created() {
    this.listLoading = true,
    this.list = this.alarmData,
    console.log(this.alarmData)
    this.listLoading = false
  },
  methods: {
    // fetchData() {
    //   this.listLoading = true
    //   // axios.post(`http://localhost:5000/data`, index).then(res => {
    //   //   res.data
    //   //   this.listLoading = false
    //   // });
    //   getList().then(response => {
    //     this.list = response.data.items
    //     this.listLoading = false
    //   })
    // }
  }
}
</script>
<style>
/* .el-table{
  border-radius: 20px;
  border-color: #40c9c6;
  border-width: 2px;
  border-style: dotted;
} */
</style>
