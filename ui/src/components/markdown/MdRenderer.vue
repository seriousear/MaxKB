<template>
  <template v-for="(item, index) in md_view_list" :key="index">
    <div
      v-if="item.type === 'question'"
      @click="quickProblemHandle ? quickProblemHandle(item.content) : (content: string) => {}"
      class="problem-button ellipsis-2 mb-8"
      :class="quickProblemHandle ? 'cursor' : 'disabled'"
    >
      <el-icon><EditPen /></el-icon>
      {{ item.content }}
    </div>
    <HtmlRander v-else-if="item.type === 'html_rander'" :source="item.content"></HtmlRander>
    <EchartsRander
      v-else-if="item.type === 'echarts_rander'"
      :option="item.content"
    ></EchartsRander>
    <MdPreview
      v-else
      noIconfont
      ref="editorRef"
      editorId="preview-only"
      :modelValue="item.content"
      :key="index"
      class="maxkb-md"
    />
  </template>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue'
import { config } from 'md-editor-v3'
import HtmlRander from './HtmlRander.vue'
import EchartsRander from './EchartsRander.vue'
config({
  markdownItConfig(md) {
    md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
      tokens[idx].attrSet('target', '_blank')
      return md.renderer.renderToken(tokens, idx, options)
    }
    document.appendChild
  }
})
const props = withDefaults(
  defineProps<{
    source?: string
    inner_suffix?: boolean
    quickProblemHandle?: (q: string) => void
  }>(),
  {
    source: ''
  }
)
const editorRef = ref()
const md_view_list = computed(() => {
  const temp_source = props.source
  const temp_md_img_list = temp_source.match(/(!\[.*?\]\(img\/.*?\){.*?})|(!\[.*?\]\(img\/.*?\))/g)
  const md_img_list = temp_md_img_list ? temp_md_img_list.filter((i) => i) : []
  const split_img_value = temp_source
    .split(/(!\[.*?\]\(img\/.*?\){.*?})|(!\[.*?\]\(img\/.*?\))/g)
    .filter((item) => item !== undefined)
    .filter((item) => !md_img_list?.includes(item))
  const result = Array.from(
    { length: md_img_list.length + split_img_value.length },
    (v, i) => i
  ).map((index) => {
    if (index % 2 == 0) {
      return split_img_value[Math.floor(index / 2)]
    } else {
      return md_img_list[Math.floor(index / 2)]
    }
  })
  return split_echarts_rander(split_html_rander(split_quick_question(split_md_img(result))))
})
const split_md_img = (result: Array<string>) => {
  return result
    .map((item) => split_md_img_(item))
    .reduce((x: any, y: any) => {
      return [...x, ...y]
    }, [])
}

const split_md_img_ = (source: string) => {
  const temp_md_img_list = source.match(/(!\[.*?\]\(.*?\){.*?})|(!\[.*?\]\(.*?\))/g)
  const md_img_list = temp_md_img_list ? temp_md_img_list.filter((i) => i) : []
  const split_img_value = source
    .split(/(!\[.*?\]\(.*?\){.*?})|(!\[.*?\]\(.*?\))/g)
    .filter((item) => item !== undefined)
    .filter((item) => !md_img_list?.includes(item))
  const result = Array.from(
    { length: md_img_list.length + split_img_value.length },
    (v, i) => i
  ).map((index) => {
    if (index % 2 == 0) {
      return split_img_value[Math.floor(index / 2)]
    } else {
      return md_img_list[Math.floor(index / 2)]
    }
  })
  return result
}
const split_quick_question = (result: Array<string>) => {
  return result
    .map((item) => split_quick_question_(item))
    .reduce((x: any, y: any) => {
      return [...x, ...y]
    }, [])
}
const split_quick_question_ = (source: string) => {
  const temp_md_quick_question_list = source.match(/<quick_question>[\d\D]*?<\/quick_question>/g)
  const md_quick_question_list = temp_md_quick_question_list
    ? temp_md_quick_question_list.filter((i) => i)
    : []
  const split_quick_question_value = source
    .split(/<quick_question>[\d\D]*?<\/quick_question>/g)
    .filter((item) => item !== undefined)
    .filter((item) => !md_quick_question_list?.includes(item))
  const result = Array.from(
    { length: md_quick_question_list.length + split_quick_question_value.length },
    (v, i) => i
  ).map((index) => {
    if (index % 2 == 0) {
      return { type: 'md', content: split_quick_question_value[Math.floor(index / 2)] }
    } else {
      return {
        type: 'question',
        content: md_quick_question_list[Math.floor(index / 2)]
          .replace('<quick_question>', '')
          .replace('</quick_question>', '')
      }
    }
  })
  return result
}
const split_html_rander = (result: Array<any>) => {
  return result
    .map((item) => split_html_rander_(item.content, item.type))
    .reduce((x: any, y: any) => {
      return [...x, ...y]
    }, [])
}

const split_html_rander_ = (source: string, type: string) => {
  const temp_md_quick_question_list = source.match(/<html_rander>[\d\D]*?<\/html_rander>/g)
  const md_quick_question_list = temp_md_quick_question_list
    ? temp_md_quick_question_list.filter((i) => i)
    : []
  const split_quick_question_value = source
    .split(/<html_rander>[\d\D]*?<\/html_rander>/g)
    .filter((item) => item !== undefined)
    .filter((item) => !md_quick_question_list?.includes(item))
  const result = Array.from(
    { length: md_quick_question_list.length + split_quick_question_value.length },
    (v, i) => i
  ).map((index) => {
    if (index % 2 == 0) {
      return { type: type, content: split_quick_question_value[Math.floor(index / 2)] }
    } else {
      return {
        type: 'html_rander',
        content: md_quick_question_list[Math.floor(index / 2)]
          .replace('<html_rander>', '')
          .replace('</html_rander>', '')
      }
    }
  })
  return result
}

const split_echarts_rander = (result: Array<any>) => {
  return result
    .map((item) => split_echarts_rander_(item.content, item.type))
    .reduce((x: any, y: any) => {
      return [...x, ...y]
    }, [])
}

const split_echarts_rander_ = (source: string, type: string) => {
  const temp_md_quick_question_list = source.match(/<echarts_rander>[\d\D]*?<\/echarts_rander>/g)
  const md_quick_question_list = temp_md_quick_question_list
    ? temp_md_quick_question_list.filter((i) => i)
    : []
  const split_quick_question_value = source
    .split(/<echarts_rander>[\d\D]*?<\/echarts_rander>/g)
    .filter((item) => item !== undefined)
    .filter((item) => !md_quick_question_list?.includes(item))
  const result = Array.from(
    { length: md_quick_question_list.length + split_quick_question_value.length },
    (v, i) => i
  ).map((index) => {
    if (index % 2 == 0) {
      return { type: type, content: split_quick_question_value[Math.floor(index / 2)] }
    } else {
      return {
        type: 'echarts_rander',
        content: md_quick_question_list[Math.floor(index / 2)]
          .replace('<echarts_rander>', '')
          .replace('</echarts_rander>', '')
      }
    }
  })
  return result
}
</script>
<style lang="scss" scoped>
.problem-button {
  width: 100%;
  border: none;
  border-radius: 8px;
  background: var(--app-layout-bg-color);
  height: 46px;
  padding: 0 12px;
  line-height: 46px;
  box-sizing: border-box;
  color: var(--el-text-color-regular);
  -webkit-line-clamp: 1;
  word-break: break-all;
  &:hover {
    background: var(--el-color-primary-light-9);
  }
  &.disabled {
    &:hover {
      background: var(--app-layout-bg-color);
    }
  }
  :deep(.el-icon) {
    color: var(--el-color-primary);
  }
}
</style>
