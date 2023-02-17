<template>
  <div class="cartcontrol">
    <transition name="move">
      <div class="iconfont icon-minus-circle-fill" v-if="food.count" @click.stop="updateFoodCount(false)"></div>
    </transition>
    <div class="cart-count" v-if="food.count">{{food.count}}</div>
    <div class="iconfont icon-plus-circle-fill" @click.stop="updateFoodCount(true)"></div>
  </div>
</template>

<script>
export default {
  props: {
    food: Object
  },

  methods: {
    updateFoodCount (isAdd) {
      this.$store.dispatch('updateFoodCount', {isAdd, food: this.food})
    }
  }
}
</script>

<style lang="less">
  @import "../../common/less/mixins.less";
  .cartcontrol{
    font-size: 0;
    .cart-decrease{
      display: inline-block;
      padding: 6px;
      line-height: 24px;
      font-size: 24px;
      color: rgb(0, 160, 220);
    }

    .icon-minus-circle-fill{
      display: inline-block;
      padding:6px;
      line-height:24px;
      font-size:24px;
      color:@green;
      &.move-enter-active, &.move-leave-active{
        transition:all .3s;
      }
      &.move-enter, &.move-leave-to{
        opacity:0;
        transform:translateX(15px) rotate(180deg);
      }
    }
    .cart-count{
      display: inline-block;
      vertical-align: top;
      width: 12px;
      padding-top: 6px;
      line-height: 24px;
      text-align: center;
      font-size: 10px;
      color: rgb(147, 153, 159);
    }
    .icon-plus-circle-fill{
      display: inline-block;
      padding: 6px;
      line-height: 24px;
      font-size: 24px;
      color:@green;
    }
  }
</style>
