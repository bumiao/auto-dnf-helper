<template>
  <div>
    <div class="text-lg font-bold">Auto Unpack</div>
    <ElAlert
      title="通过配置启动脚本。在运行过程中按下ESC键可以强制终止。"
      type="info"
      show-icon
      :closable="false"
      class="!mb-4"
    />
    <div>通过空格捕获坐标</div>
    <div v-if="!isNil(x) && !isNil(y)" class="color-gray text-xs mt-2">
      已捕获坐标: x : <ElTag>{{ x }}</ElTag> y : <ElTag>{{ y }}</ElTag>
    </div>

    <ElButton class="mt-4 mb-4" type="primary" :icon="Plus" @click="onAdd" @mousedown.prevent>
      Add
    </ElButton>
    <ElButton class="mt-4 mb-4" type="success" @click="onRun" :icon="VideoPlay" @mousedown.prevent>
      Run
    </ElButton>
    <ElTooltip placement="top" content="导出至剪贴板">
      <ElButton class="mt-4 mb-4" :icon="Share" @click="onExport" @mousedown.prevent>
        导出
      </ElButton>
    </ElTooltip>
    <ElTooltip placement="top" content="从剪贴板导入">
      <ElButton class="mt-4 mb-4" :icon="Upload" @click="onImport" @mousedown.prevent>
        导入
      </ElButton>
    </ElTooltip>
    <ElButton type="danger" @click="onClear" @mousedown.prevent>重置</ElButton>

    <VueDraggable v-model="data" :animation="150" target="tbody">
      <ElTable :data="data" :max-height="500" border row-key="id">
        <ElTableColumn prop="type" label="方法" :formatter="typeFomatter"></ElTableColumn>
        <ElTableColumn prop="prop" label="属性">
          <template #default="{ row }: { row: AutoUnpackMethod }">
            {{ omit(row, ['type', 'description', 'id']) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="description" label="描述"></ElTableColumn>
        <ElTableColumn prop="action" label="操作" width="120">
          <template #default="{ row, $index }">
            <ElButton
              :icon="Edit"
              size="small"
              @click="onEdit(row, $index)"
              @mousedown.prevent
            ></ElButton>
            <ElButton
              :icon="Delete"
              type="danger"
              size="small"
              @click="onDelete($index)"
              @mousedown.prevent
            ></ElButton>
          </template>
        </ElTableColumn>
      </ElTable>
    </VueDraggable>

    <ElForm class="mt-4" label-width="10%" label-position="top">
      <ElFormItem label="微调变速" class="h-32">
        <ElAlert title="整体的自动化操作会被加速或减速" type="info" show-icon :closable="false" />
        <div class="!w-[50%] ml-8">
          <ElSlider
            v-model="speed"
            :min="0.2"
            :max="3"
            :step="0.1"
            :marks="{ 0.2: '最慢', 1: '标准', 3: '最快' }"
          />
        </div>
      </ElFormItem>
      <ElFormItem label="循环次数 (整数,其中-1表示无限次)">
        <ElInputNumber v-model="loop_count" :min="-1" :max="999" />
      </ElFormItem>
    </ElForm>

    <div>暂存的脚本</div>
    <ElButton class="mt-4 mb-4" :icon="Upload" @click="onImportProduction" @mousedown.prevent>
      导入
    </ElButton>
    <ElButton
      :disabled="selectedProduction.length === 0"
      class="mt-4 mb-4"
      :icon="Promotion"
      @click="onExecute"
      @mousedown.prevent
    >
      顺序执行
    </ElButton>

    <VueDraggable v-model="production" :animation="150" target="tbody">
      <ElTable
        :data="production"
        :max-height="500"
        border
        @selection-change="onProductionSelectionChange"
      >
        <ElTableColumn type="selection"> </ElTableColumn>
        <ElTableColumn prop="name" label="名称">
          <template #default="{ row }">
            <ElInput v-model="row.name" class="!w-80" placeholder="给脚本取个名吧"></ElInput>
          </template>
        </ElTableColumn>
        <ElTableColumn prop="loop" label="循环">
          <template #default="{ row }">
            <ElInputNumber v-model="row.loop" class="!w-30" placeholder="循环次数" />
          </template>
        </ElTableColumn>
        <ElTableColumn prop="action" label="操作" width="120">
          <template #default="{ row, $index }">
            <ElButton
              :icon="VideoPlay"
              size="small"
              type="primary"
              @click="onPlay(row)"
              @mousedown.prevent
            />
            <ElButton
              :icon="Delete"
              type="danger"
              size="small"
              @click="onProductionDelete($index)"
              @mousedown.prevent
            />
          </template>
        </ElTableColumn>
      </ElTable>
    </VueDraggable>

    <MethodDialog ref="methodDialogRef"></MethodDialog>
  </div>
</template>

<script setup lang="ts">
import { Plus, Promotion, Share, Upload, VideoPlay } from '@element-plus/icons-vue'
import {
  ElButton,
  ElMessage,
  ElMessageBox,
  ElTooltip,
  ElTable,
  ElTableColumn,
  ElTag,
  ElForm,
  ElFormItem,
  ElSlider,
  ElAlert,
  ElInputNumber,
  ElInput
} from 'element-plus'
import { onUnmounted, ref, useTemplateRef } from 'vue'
import { useEventListener, useLocalStorage, type Fn } from '@vueuse/core'
import { getMousePosition, postRun } from '@/api'
import { cloneDeep, isNil, omit } from 'lodash-es'
import MethodDialog from './components/method-dialog.vue'
import type { AutoUnpackMethod, AutoUnpackProduction } from '@/types'
import { Delete, Edit } from '@element-plus/icons-vue'
import { VueDraggable } from 'vue-draggable-plus'

const methodDialogRef = useTemplateRef('methodDialogRef')

const data = useLocalStorage<AutoUnpackMethod[]>('AutoUnpackData', [])
const speed = useLocalStorage<number>('AutoUnpackSpeed', 1)
const loop_count = useLocalStorage<number>('AutoUnpackLoopCount', 1)

const production = useLocalStorage<AutoUnpackProduction[]>('AutoUnpackProduction', [])
const selectedProduction = ref<AutoUnpackProduction[]>([])

const x = ref<number>()
const y = ref<number>()

let stopPointerCapture: Fn | null = null

stopPointerCapture = useEventListener('keypress', async (event) => {
  if (methodDialogRef.value?.visible) {
    return
  }
  if (event.code === 'Space') {
    event.preventDefault()
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
  } else if (row.type === 'delay') {
    return '延迟'
  } else if (row.type === 'keyPress') {
    return '键盘按下'
  } else if (row.type === 'continuousMoveClick') {
    return '连续水平点击'
  }
  return ''
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

const onProductionDelete = async (index: number) => {
  await ElMessageBox.confirm('确定要删除吗', {
    type: 'warning'
  })
  production.value.splice(index, 1)
}

const onRun = async () => {
  await postRun({
    speed: speed.value,
    loop_count: loop_count.value,
    data: data.value
  })
}

const onPlay = async (row: AutoUnpackProduction) => {
  await postRun({
    speed: speed.value,
    loop_count: row.loop ?? loop_count.value,
    data: row.script || []
  })
}

const onExport = async () => {
  await navigator.clipboard.writeText(JSON.stringify(data.value).replace(/\s+/g, ''))
  ElMessage.success({
    message: '已成功导出到剪贴板'
  })
}

const onImport = async () => {
  try {
    // 从剪贴板读取数据
    const clipboardText = await navigator.clipboard.readText()
    // 尝试解析为 JSON
    const importedData = JSON.parse(clipboardText)
    // 将解析后的数据赋值给目标变量
    data.value = importedData
    ElMessage.success({
      message: '已成功从剪贴板导入数据'
    })
  } catch (error) {
    // 处理解析错误或其他错误
    ElMessage.error({
      message: '导入失败：剪贴板内容无效或不是合法的 JSON 数据'
    })
  }
}

const onImportProduction = async () => {
  try {
    // 从剪贴板读取数据
    const clipboardText = await navigator.clipboard.readText()
    // 尝试解析为 JSON
    const importedData = JSON.parse(clipboardText)
    // 将解析后的数据赋值给目标变量
    production.value.push({ name: '', script: importedData })
    ElMessage.success({
      message: '已成功从剪贴板导入数据'
    })
  } catch (error) {
    // 处理解析错误或其他错误
    ElMessage.error({
      message: '导入失败：剪贴板内容无效或不是合法的 JSON 数据'
    })
  }
}

const onClear = async () => {
  await ElMessageBox.confirm('确定要重置吗', {
    type: 'warning'
  })
  data.value = []
  speed.value = 1
}

const onExecute = async () => {
  for (const item of production.value) {
    await onPlay(item)
  }
}

const onProductionSelectionChange = (data: AutoUnpackProduction[]) => {
  selectedProduction.value = cloneDeep(data)
}

onUnmounted(() => {
  stopPointerCapture()
})
</script>

<style lang="less" scoped></style>
