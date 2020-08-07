<template>
  <div id="app">
    <transition :name="transitionName">
      <router-view class="router-view"/>
    </transition>
  </div>
</template>

<script>
export default {
  data () {
    return {
      transitionName: ''
    }
  },
  watch: {
    $route(to, from) {
      if(to.meta.index > from.meta.index) {
        this.transitionName = 'slide-left'
      } else {
        this.transitionName = 'slide-right'
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.router-view {
  position: absolute;
  width: 100%;
  transition: all .8s cubic-bezier(.55, 0, .1, 1);
}

.slide-left-enter, .slide-right-leave-active {
  opacity: 0;
  transform: translateX(50px);
}

.slide-left-leave-active, .slide-right-enter {
  opacity: 0;
  transform: translateX(-50px);
}
</style>
