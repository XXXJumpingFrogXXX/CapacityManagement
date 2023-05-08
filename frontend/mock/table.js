const Mock = require('mockjs')

const data = Mock.mock({
  'items|50': [{
    id: '@id',
    display_time: '@datetime',
    title: '@sentence(10, 20)',
    'status|1': ['published', 'draft', 'deleted'],
  }]
})

module.exports = [
  {
    url: '/frontend/table/list',
    type: 'get',
    response: config => {
      const items = data.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  }
]
