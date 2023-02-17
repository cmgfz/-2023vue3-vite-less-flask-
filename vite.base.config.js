import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
const path = require('path')
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue()
  ],
  css:{
    preprocessorOptions:{
      less:{
        charset:false,
        globalVars:{
          green:'#02a774',
          yellow:'#F5A100',
          bc:'#e4e4e4'
        }
      }
    }
  },
  server:{
    proxy:{
      "/api":{
        target:"http://localhost:3000",
        changeOrigin:true,
        rewrite:(path)=>path.replace(/^\/api/,'')
      }
    }
  }
});
