<template>
  <el-form-item>
    <template #label>
      <div class="flex-between">
        选项值
        <el-button link type="primary" @click.stop="addOption()">
          <el-icon class="mr-4">
            <Plus />
          </el-icon>
          添加
        </el-button>
      </div>
    </template>

    <div
      class="w-full flex-between mb-8"
      v-for="(option, $index) in formValue.option_list"
      :key="$index"
    >
      <el-input v-model="formValue.option_list[$index].value" placeholder="请输入选项值" />
      <el-button link class="ml-8" @click.stop="delOption($index)">
        <el-icon>
          <Delete />
        </el-icon>
      </el-button>
    </div>
  </el-form-item>
  <el-form-item
    label="默认值"
    :required="formValue.required"
    prop="default_value"
    :rules="formValue.required ? [{ required: true, message: '默认值 为必填属性' }] : []"
  >
    <el-select v-model="formValue.default_value" :teleported="false" popper-class="default-select">
      <el-option
        v-for="(option, index) in formValue.option_list"
        :key="index"
        :label="option.value"
        :value="option.value"
      />
    </el-select>
  </el-form-item>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue'

const props = defineProps<{
  modelValue: any
}>()
const emit = defineEmits(['update:modelValue'])
const formValue = computed({
  set: (item) => {
    emit('update:modelValue', item)
  },
  get: () => {
    return props.modelValue
  }
})

const addOption = () => {
  formValue.value.option_list.push({ value: '' })
}

const delOption = (index: number) => {
  const option = formValue.value.option_list[index]
  if (option.value && formValue.value.default_value == option.value) {
    formValue.value.default_value = ''
  }
  formValue.value.option_list.splice(index, 1)
}

const getData = () => {
  return {
    input_type: 'SingleSelect',
    attrs: {},
    default_value: formValue.value.default_value,
    text_field: 'value',
    value_field: 'value',
    option_list: formValue.value.option_list
  }
}
const rander = (form_data: any) => {
  formValue.value.option_list = form_data.option_list || []
  formValue.value.default_value = form_data.default_value
}

defineExpose({ getData, rander })
onMounted(() => {
  formValue.value.option_list = []
  formValue.value.default_value = ''
})
</script>
<style lang="scss" scoped>
:deep(.el-form-item__label) {
  display: block;
}

:deep(.el-select-dropdown) {
  max-width: 400px;
}
</style>
