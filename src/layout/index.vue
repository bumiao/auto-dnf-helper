<template>
  <ElContainer class="h-full w-full">
    <ElAside width="200px">
      <ElMenu :default-active="currentMenu" router class="h-full">
        <ElMenuItem index="/introduction">
          <ElIcon><House /></ElIcon>
          Get Start
        </ElMenuItem>
        <ElMenuItem index="/auto-unpack">
          <ElIcon><Box /></ElIcon>
          Auto Unpack
        </ElMenuItem>
      </ElMenu>
    </ElAside>
    <ElMain style="width: 100%">
      <RouterView />
    </ElMain>
  </ElContainer>
</template>

<script setup lang="ts">
import { ElContainer, ElAside, ElMain, ElMenu, ElMenuItem, ElIcon } from 'element-plus'
import { Box, House } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

defineOptions({
  name: 'LayoutView'
})

const route = useRoute()
const currentMenu = ref(route.path)
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  overflow: hidden;

  .menu {
    height: 100%;
  }
}
</style>
