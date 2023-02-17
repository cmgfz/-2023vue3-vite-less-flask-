import {defineConfig} from "vite";
import viteBaseConfig from "./vite.base.config";
import viteDevConfig from "./vite.dev.config";
import viteProConfig from "./vite.pro.config";
const envResolver={
    "build":()=>{
        console.log("生产环境");
        return ({...viteBaseConfig,...viteProConfig})
    },
    "serve":()=>{
        console.log("开发环境");
        return Object.assign({},viteBaseConfig,viteDevConfig)
    }
}
export default defineConfig(({command})=>{
    console.log("command",command);
    return envResolver[command]();
})