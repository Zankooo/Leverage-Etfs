<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <header class="mb-12 text-center">
      <h1 class="text-4xl font-bold text-[#1A1A1A] mb-4">{{ t('contact.title') }}</h1>
      <p class="text-gray-500">{{ t('contact.intro') }}</p>
    </header>

    <form @submit.prevent class="space-y-6 bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="contact-name" class="block text-sm font-medium text-gray-700 mb-2">{{ t('contact.name') }}</label>
          <input id="contact-name" type="text" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10B981] outline-none" :placeholder="t('contact.namePlaceholder')">
        </div>
        <div>
          <label for="contact-email" class="block text-sm font-medium text-gray-700 mb-2">{{ t('contact.email') }}</label>
          <input id="contact-email" type="email" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10B981] outline-none" :placeholder="t('contact.emailPlaceholder')">
        </div>
      </div>
      <div>
        <label for="contact-message" class="block text-sm font-medium text-gray-700 mb-2">{{ t('contact.message') }}</label>
        <textarea id="contact-message" rows="4" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10B981] outline-none" :placeholder="t('contact.messagePlaceholder')"></textarea>
      </div>
      <button class="w-full py-4 bg-gray-900 text-white font-bold rounded-xl hover:bg-black transition-colors">
        {{ t('contact.send') }}
      </button>
    </form>

    <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
      <div>
        <div class="text-gray-400 mb-2 text-sm uppercase font-bold tracking-widest">{{ t('contact.email') }}</div>
        <div class="font-medium">info@vzvodno.si</div>
      </div>
      <div>
        <div class="text-gray-400 mb-2 text-sm uppercase font-bold tracking-widest">{{ t('contact.phone') }}</div>
        <div class="font-medium">+386 41 000 000</div>
      </div>
      <div>
        <div class="text-gray-400 mb-2 text-sm uppercase font-bold tracking-widest">{{ t('contact.location') }}</div>
        <div class="font-medium">{{ t('contact.address') }}</div>
      </div>
    </div>
  </div>
</template>
