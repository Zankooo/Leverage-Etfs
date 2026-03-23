<script setup lang="ts">
import { ref } from 'vue'
import { ChevronRight, FileText, Loader2 } from 'lucide-vue-next'

const initialInvestment = ref('')
const monthlyContribution = ref('')
const selectedIndex = ref('S&P 500')
const selectedInterval = ref('15 let')

const isLoading = ref(false)
const results = ref<{ id: number; title: string; content: string }[]>([])


const calculate = async () => {
  isLoading.value = true
  // Simulate backend delay
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  // Mock backend response with "tens of HTMLs"
  const mockHtmls = Array.from({ length: 12 }, (_, i) => ({
    id: i + 1,
    title: `Simulacija Scenarij #${i + 1} - ${selectedIndex.value}`,
    content: `
      <div class="p-8 font-sans">
        <h2 class="text-2xl font-bold mb-4 text-[#1A1A1A]">Poročilo o simulaciji #${i + 1}</h2>
        <p class="mb-4 text-gray-600">To je podrobna analiza za vašo investicijo z indeksom <strong>${selectedIndex.value}</strong> čez obdobje <strong>${selectedInterval.value}</strong>.</p>
        <div class="grid grid-cols-2 gap-4 mb-6">
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-100">
            <span class="text-xs text-gray-400 uppercase font-bold">Začetni vložek</span>
            <p class="text-xl font-semibold">${initialInvestment.value} €</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-100">
            <span class="text-xs text-gray-400 uppercase font-bold">Mesečni vložek</span>
            <p class="text-xl font-semibold">${monthlyContribution.value} €</p>
          </div>
        </div>
        <div class="prose prose-sm max-w-none text-gray-700">
          <p>Pričakovana donosnost v tem scenariju temelji na zgodovinskih podatkih med leti ${2000 + i} in ${2015 + i}.</p>
          <ul class="list-disc pl-5 space-y-2">
            <li>Povprečna letna rast: ${(7 + Math.random() * 5).toFixed(2)}%</li>
            <li>Največji upad (Drawdown): -${(10 + Math.random() * 20).toFixed(2)}%</li>
            <li>Končna vrednost portfelja: <strong>${(parseInt(initialInvestment.value || '0') * 2.5 + Math.random() * 100000).toFixed(0)} €</strong></li>
          </ul>
        </div>
        <div class="mt-8 pt-6 border-t border-gray-100 text-xs text-gray-400 italic">
          Opozorilo: Pretekli donosi niso zagotovilo za prihodnje rezultate.
        </div>
      </div>
    `
  }))
  
  results.value = mockHtmls
  isLoading.value = false
}

const openHtml = (content: string) => {
  // TODO: ko bo backend integriran, bo content prišel od API-ja
  const blob = new Blob([content], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank')
}
</script>

<template>
  <div class="max-w-xl mx-auto">
    <!-- Calculation Form Card -->
    <div class="bg-white rounded-[32px] shadow-[0_20px_50px_rgba(0,0,0,0.05)] p-7 md:p-10 border border-gray-50">
      <div class="text-center mb-7">
        <h1 class="text-3xl font-bold text-[#1A1A1A] mb-2 tracking-tight">Vzvodno investiranje</h1>
        <p class="text-gray-400 text-base">Vnesi parametre in pripravi simulacijo rasti portfelja.</p>
      </div>

      <div class="space-y-5">
        <!-- Initial Investment -->
        <div>
          <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Začetna investicija (€)</label>
          <input 
            v-model="initialInvestment"
            type="number" 
            placeholder="npr. 1.000 €"
            class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all placeholder:text-gray-300"
          />
        </div>

        <!-- Monthly Contribution -->
        <div>
          <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Mesečni vložek (€)</label>
          <input 
            v-model="monthlyContribution"
            type="number" 
            placeholder="npr. 100 €"
            class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all placeholder:text-gray-300"
          />
        </div>

        <!-- Selectors -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Indeks</label>
            <select 
              v-model="selectedIndex"
              class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] appearance-none cursor-pointer"
            >
              <option>S&P 500</option>
              <option>Nasdaq 100</option>
              <option>MSCI World</option>
              <option>Euro Stoxx 50</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Interval</label>
            <select 
              v-model="selectedInterval"
              class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] appearance-none cursor-pointer"
            >
              <option>5 let</option>
              <option>10 let</option>
              <option>15 let</option>
              <option>20 let</option>
              <option>30 let</option>
            </select>
          </div>
        </div>

        <!-- Calculate Button -->
        <button 
          @click="calculate"
          :disabled="isLoading"
          class="w-full py-3.5 bg-[#10B981] hover:bg-[#059669] text-white text-base font-semibold rounded-xl transition-all shadow-lg shadow-[#10B981]/20 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <Loader2 v-if="isLoading" class="w-5 h-5 animate-spin" />
          <span>{{ isLoading ? 'Računam...' : 'Izračunaj' }}</span>
        </button>

        <p class="text-center text-gray-400 text-sm px-8 leading-relaxed">
          Opomba: Stran je zasnovana kot "login-page" kartica — sredinsko, čista in osredotočena na vnos.
        </p>
      </div>
    </div>

    <!-- Results Section -->
    <div v-if="results.length > 0" class="mt-16 space-y-6">
      <h2 class="text-2xl font-bold text-[#1A1A1A] px-4">Rezultati simulacije</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="res in results" 
          :key="res.id"
          @click="openHtml(res.content)"
          class="bg-white p-6 rounded-2xl border border-gray-100 hover:border-[#10B981] hover:shadow-md transition-all cursor-pointer flex items-center justify-between group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-emerald-50 p-3 rounded-xl text-[#10B981]">
              <FileText class="w-6 h-6" />
            </div>
            <span class="font-medium text-gray-700">{{ res.title }}</span>
          </div>
          <ChevronRight class="text-gray-300 group-hover:text-[#10B981] transition-colors" />
        </div>
      </div>
    </div>


  </div>
</template>

<style scoped>
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
</style>
