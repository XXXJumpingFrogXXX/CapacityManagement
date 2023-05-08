import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/frontend/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/frontend/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/frontend/user/logout',
    method: 'post'
  })
}
