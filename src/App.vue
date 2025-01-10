<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
import { RouterView } from 'vue-router'
</script>

<template>
  <ElConfigProvider>
    <RouterView />
  </ElConfigProvider>
</template>
