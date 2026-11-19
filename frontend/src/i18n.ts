import { watch } from 'vue'
import { createI18n } from 'vue-i18n'
import sl from './locales/sl'
import en from './locales/en'

const languageStorageKey = 'vzvodno-language'

function savedLanguage(): 'sl' | 'en' {
  try {
    return localStorage.getItem(languageStorageKey) === 'en' ? 'en' : 'sl'
  } catch {
    // Preklop deluje tudi, če brskalnik ne dovoli shranjevanja izbire.
    return 'sl'
  }
}

const numberFormats = {
  decimal: { minimumFractionDigits: 2, maximumFractionDigits: 2, useGrouping: true },
  integer: { maximumFractionDigits: 0, useGrouping: true },
  percent: { style: 'percent', minimumFractionDigits: 0, maximumFractionDigits: 2 },
} as const

const datetimeFormats = {
  short: { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' },
} as const

export const i18n = createI18n({
  legacy: false,
  locale: savedLanguage(),
  fallbackLocale: 'sl',
  messages: { sl, en },
  numberFormats: { sl: numberFormats, en: numberFormats },
  datetimeFormats: { sl: datetimeFormats, en: datetimeFormats },
  pluralRules: {
    sl: (choice) => {
      const remainder = Math.abs(choice) % 100
      if (remainder === 1) return 0
      if (remainder === 2) return 1
      if (remainder === 3 || remainder === 4) return 2
      return 3
    },
  },
})

watch(i18n.global.locale, (language) => {
  document.documentElement.lang = language
  document.title = i18n.global.t('app.title')
  try {
    localStorage.setItem(languageStorageKey, language)
  } catch {
    // Onemogočen localStorage ne sme preprečiti uporabe aplikacije.
  }
}, { immediate: true })
