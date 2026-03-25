<template>
  <div class="max-w-4xl mx-auto">
    <header class="mb-16 text-center">
      <h1 class="text-5xl font-bold text-[#1A1A1A] mb-6 tracking-tight">Prednosti platforme</h1>
      <p class="text-xl text-gray-500 leading-relaxed max-w-2xl mx-auto">
        Zakaj izbrati Vzvodno za vaše investicijske simulacije?
      </p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-24">
      <div v-for="feature in features" :key="feature.title" class="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
        <div class="w-12 h-12 bg-emerald-50 text-[#10B981] rounded-2xl flex items-center justify-center mb-6">
          <component :is="feature.icon" class="w-6 h-6" />
        </div>
        <h3 class="text-xl font-bold mb-4">{{ feature.title }}</h3>
        <p class="text-gray-500 leading-relaxed">{{ feature.description }}</p>
      </div>
    </div>

    <div class="bg-gray-900 text-white rounded-[40px] p-12 md:p-20 relative overflow-hidden">
      <div class="relative z-10 max-w-xl">
        <h2 class="text-4xl font-bold mb-6">Pripravljeni na simulacijo?</h2>
        <p class="text-gray-400 text-lg mb-10">
          Preizkusite naše orodje in odkrijte moč dolgoročnega investiranja z uporabo različnih parametrov.
        </p>
        <RouterLink to="/" class="inline-block px-8 py-4 bg-[#10B981] hover:bg-[#059669] text-white font-bold rounded-2xl transition-all">
          Začni zdaj
        </RouterLink>
      </div>
      <div class="absolute right-0 bottom-0 w-1/2 h-full bg-gradient-to-tl from-emerald-500/20 to-transparent pointer-events-none"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Zap, Shield, BarChart3 } from 'lucide-vue-next'

const features = [
  {
    title: 'Hitrost',
    description: 'Naši algoritmi v trenutku obdelajo tisoče podatkovnih točk za natančno simulacijo.',
    icon: Zap
  },
  {
    title: 'Varnost',
    description: 'Vaši podatki so varni. Simulacije se izvajajo anonimno in brez shranjevanja osebnih podatkov.',
    icon: Shield
  },
  {
    title: 'Analitika',
    description: 'Prejmite podrobna poročila v HTML obliki, ki jih lahko shranite za kasnejšo uporabo.',
    icon: BarChart3
  }
]
</script>
