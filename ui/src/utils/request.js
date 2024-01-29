import axios from 'axios'


const AxiosInstance = axios.create({
    baseURL: ``,
    timeout: 5000
})

AxiosInstance.interceptors.request.use(
    (request) => {
        return request
    },
    (error) => {
        console.error(error)
        return Promise.reject(error)
    }
)

AxiosInstance.interceptors.response.use(
    (response) => {
        return response.data
    },
    (error) => {
        console.error(error)
        return Promise.reject(error)
    }
)

export default AxiosInstance
