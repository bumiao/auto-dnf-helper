<template>
  <div>
    <div>通过空格捕获坐标</div>
    <div v-if="!isNil(x) && !isNil(y)" class="color-gray text-xs">
      已捕获坐标: x : <ElTag>{{ x }}</ElTag> y : <ElTag>{{ y }}</ElTag>
    </div>

    <ElButton class="mt-4 mb-4" type="primary" @click="onAdd">Add</ElButton>
    <ElButton class="mt-4 mb-4" type="success" @click="onRun">Run</ElButton>

    <VueDraggable v-model="data" :animation="150" target="tbody">
      <ElTable :data="data">
        <ElTableColumn
          prop="type"
          label="方法"
          width="200"
          :formatter="typeFomatter"
        ></ElTableColumn>
        <ElTableColumn prop="description" label="描述"></ElTableColumn>
        <ElTableColumn prop="action" label="操作" width="200">
          <template #default="{ row, $index }">
            <ElButton :icon="Edit" size="small" @click="onEdit(row, $index)"></ElButton>
            <ElButton
              :icon="Delete"
              type="danger"
              size="small"
              @click="onDelete($index)"
            ></ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </VueDraggable>

    <MethodDialog ref="methodDialogRef"></MethodDialog>
  </div>
</template>

<script setup lang="ts">
import { ElButton, ElIcon, ElMessageBox, ElTable, ElTableColumn, ElTag } from 'element-plus'
import { onUnmounted, ref, useTemplateRef } from 'vue'
import { useEventListener, useLocalStorage, type Fn } from '@vueuse/core'
import { getMousePosition, postRun } from '@/api'
import { isNil } from 'lodash-es'
import MethodDialog from './components/method-dialog.vue'
import type { AutoUnpackMethod } from '@/types'
import { Delete, Edit, MessageBox } from '@element-plus/icons-vue'
import { VueDraggable } from 'vue-draggable-plus'

const methodDialogRef = useTemplateRef('methodDialogRef')

const data = useLocalStorage<AutoUnpackMethod[]>('AutoUnpackData', [])

const x = ref<number>()
const y = ref<number>()

let stopPointerCapture: Fn | null = null

stopPointerCapture = useEventListener('keypress', async (event) => {
  if (event.code === 'Space') {
    const mousePosition = await getMousePosition()
    x.value = mousePosition?.x
    y.value = mousePosition?.y
  }
})

const typeFomatter = (row: AutoUnpackMethod) => {
  if (row.type === 'moveTo') {
    return '鼠标移动'
  } else if (row.type === 'click') {
    return '鼠标单击'
  } else {
    return '延迟'
  }
}

const onAdd = async () => {
  const result = await methodDialogRef.value?.show()
  if (result) {
    data.value.push(result)
  }
}

const onEdit = async (row: AutoUnpackMethod, index: number) => {
  const result = await methodDialogRef.value?.show(row)
  if (result) {
    data.value.splice(index, 1, result)
  }
}

const onDelete = async (index: number) => {
  await ElMessageBox.confirm('确定要删除吗', {
    type: 'warning'
  })
  data.value.splice(index, 1)
}

const onRun = async () => {
  await postRun(data.value)
}

onUnmounted(() => {
  stopPointerCapture()
})
</script>

<style lang="less" scoped></style>
