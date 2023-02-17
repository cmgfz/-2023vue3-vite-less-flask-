<template>    
    <div id="app">
        <router-view></router-view>
        <FooterGuide v-show="$route.meta.showFooter"/>
    </div>
</template>

<script>
    import {mapActions} from 'vuex'
    import FooterGuide from './components/FooterGuide/FooterGuide.vue';
    export default{
        components:{
            FooterGuide
        },
        mounted(){
            this.getAddress()
            this.getUserInfo()
        },
        methods:{
            ...mapActions(['getAddress','getUserInfo'])
        }
    }
</script>

<style lang="less">
*{
    touch-action: manipulation;
}
#app{
  width:100%;
  height:100%;
  background:#f5f5f5;
  position:relative;
}
</style>