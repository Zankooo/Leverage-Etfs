<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <header class="mb-16 text-center">
      <h1 class="text-5xl font-bold text-[#1A1A1A] mb-6 tracking-tight">{{ t('about.title') }}</h1>
      <p class="text-xl text-gray-500 leading-relaxed max-w-2xl mx-auto">
        {{ t('about.intro') }}
      </p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-24">
      <div>
        <h2 class="text-3xl font-bold mb-6">{{ t('about.vision') }}</h2>
        <p class="text-gray-600 mb-4 leading-relaxed">
          {{ t('about.visionDescription') }}
        </p>
        <p class="text-gray-600 leading-relaxed">
          {{ t('about.leverageDescription') }}
        </p>
      </div>
      <div class="bg-emerald-50 rounded-[40px] p-12 flex items-center justify-center">
        <div class="text-center">
          <div class="text-6xl font-bold text-[#10B981] mb-2">100%</div>
          <div class="text-emerald-800 font-medium uppercase tracking-widest text-sm">{{ t('about.transparency') }}</div>
        </div>
      </div>
    </div>

    <section class="bg-white rounded-3xl p-12 border border-gray-100 shadow-sm">
      <h2 class="text-3xl font-bold mb-8 text-center">{{ t('about.team') }}</h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
        <div v-for="i in 3" :key="i" class="text-center">
          <div class="w-24 h-24 bg-gray-100 rounded-full mx-auto mb-4"></div>
          <h3 class="font-bold text-lg">{{ t('about.namePlaceholder') }}</h3>
          <p class="text-gray-400 text-sm">{{ t('about.rolePlaceholder') }}</p>
        </div>
      </div>
    </section>
  </div>
</template>
