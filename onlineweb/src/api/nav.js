import http from "../utils/http.js"
import {reactive} from "vue";


const nav = reactive({
    header_nav_list: [],
    footer_nav_list: [],
    get_header_nav(){
        // 获取头部导航
        return http.get("/home/nav/header/")
    },
    get_footer_nav(){
        // 获取脚部导航
        return http.get("/home/nav/footer/")
    },
})
export default nav;
