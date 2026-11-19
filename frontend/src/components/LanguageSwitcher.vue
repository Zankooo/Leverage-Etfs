<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n({ useScope: 'global' })
const languages = [
  { code: 'sl', label: 'SLO', name: 'Slovenščina' },
  { code: 'en', label: 'ENG', name: 'English' },
] as const
</script>

<template>
  <div role="group" :aria-label="t('app.language')" class="flex shrink-0 items-center gap-1 rounded-xl border border-gray-200 bg-gray-50 p-1">
    <button
      v-for="language in languages"
      :key="language.code"
      type="button"
      :lang="language.code"
      :aria-label="language.name"
      :aria-pressed="locale === language.code"
      :title="language.name"
      class="min-h-9 min-w-10 cursor-pointer rounded-lg px-2.5 text-xs font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#10B981]"
      :class="locale === language.code ? 'bg-[#10B981] text-white shadow-sm' : 'text-gray-500 hover:bg-white hover:text-gray-900'"
      @click="locale = language.code"
    >
      {{ language.label }}
    </button>
  </div>
</template>
