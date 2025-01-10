<template>
  <ElDialog :title="`${state.mode === 'add' ? 'Add' : 'Edit'}`" v-model="visible" @close="onCancel">
    <ElForm label-width="150px" class="mr-12">
      <ElFormItem label="方法">
        <ElSelect v-model="state.data.type" @change="onTypeChange">
          <ElOption label="鼠标移动" value="moveTo"></ElOption>
          <ElOption label="鼠标单击" value="click"></ElOption>
          <ElOption label="延迟" value="delay"></ElOption>
        </ElSelect>
      </ElFormItem>
      <template v-if="state.data.type === 'moveTo'">
        <ElFormItem label="X">
          <ElInputNumber v-model="state.data.x"></ElInputNumber>
        </ElFormItem>
        <ElFormItem label="Y">
          <ElInputNumber v-model="state.data.y"></ElInputNumber>
        </ElFormItem>
      </template>
      <template v-else-if="state.data.type === 'click'">
        <ElFormItem label="键值">
          <ElSelect v-model="state.data.key">
            <ElOption label="左键" value="left"></ElOption>
            <ElOption label="右键" value="right"></ElOption>
          </ElSelect>
        </ElFormItem>
      </template>
      <template v-else-if="state.data.type === 'delay'">
        <ElFormItem label="延迟时间(ms)">
          <ElInputNumber v-model="state.data.time"></ElInputNumber>
        </ElFormItem>
      </template>
      <ElFormItem label="描述">
        <ElInput v-model="state.data.description" type="textarea"></ElInput>
      </ElFormItem>
    </ElForm>
    <template #footer>
      <ElButton @click="onCancel"> Cancel </ElButton>
      <ElButton type="primary" @click="onSubmit"> Submit </ElButton>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
import { nextTick, reactive, ref } from 'vue'

import {
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElInputNumber,
  ElOption,
  ElSelect
} from 'element-plus'
import { cloneDeep } from 'lodash-es'
import type { AutoUnpackMethod } from '@/types'

let resolve: (value?: AutoUnpackMethod) => void | undefined

const formRef = ref()
const state = reactive<{
  data: AutoUnpackMethod
  mode: 'add' | 'edit'
}>({
  data: {} as AutoUnpackMethod,
  mode: 'add' // add or edit
})
const visible = ref()

const open = () => {
  visible.value = true
}

const close = () => {
  visible.value = false
}

const show = async (initData?: AutoUnpackMethod) => {
  state.data = cloneDeep(initData ?? {}) as AutoUnpackMethod
  state.mode = initData ? 'edit' : 'add'
  nextTick(() => {
    formRef.value?.clearValidate()
  })
  open()
  return new Promise<AutoUnpackMethod | undefined>((res) => {
    resolve = res
  })
}

const onTypeChange = () => {
  state.data = { type: state.data.type, description: state.data.description }
}

const onSubmit = async () => {
  await formRef.value?.validate?.()
  close()
  resolve(state.data)
}

const onCancel = () => {
  resolve()
  close()
}

defineExpose({ show, close })
</script>

<style lang="scss" scoped></style>
