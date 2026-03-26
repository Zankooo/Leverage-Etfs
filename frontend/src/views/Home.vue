<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import { ChevronRight, FileText, Loader2 } from 'lucide-vue-next'

const initialInvestment = ref('')
const monthlyContribution = ref('')
const selectedIndex = ref('S&P 500')
const selectedInterval = ref(15)

const backendResponse = ref<string | null>(null)
const results = ref<any[]>([])
const isLoading = ref(false)

const isFormValid = computed(function () {
  return initialInvestment.value !== '' &&
         monthlyContribution.value !== '' &&
         selectedInterval.value != null &&
         Number(selectedInterval.value) >= 1 &&
         Number(selectedInterval.value) <= 50
})

async function izracunaj() {
  isLoading.value = true

  try {
    const podatki_za_poslat = {
      zacetna_investicija: Number(initialInvestment.value),
      mesecni_vlozek: Number(monthlyContribution.value),
      indeks: selectedIndex.value,
      interval: Number(selectedInterval.value)
    }

    const response = await axios.post('http://localhost:8000/primerjava_vrstic', podatki_za_poslat)
    const data = response.data

    console.log("Odgovor strežnika:", data)

    const getEtfColor = (file: string) => {
      if (file === 'osnoven.csv') return '#A78BFA'
      if (file === 'vzvod-2x.csv') return '#56B4F3'
      if (file === 'vzvod-3x.csv') return '#F4B000'
      return '#111827'
    }

    const getEtfLabel = (file: string) => {
      if (file === 'osnoven.csv') return 'Osnoven'
      if (file === 'vzvod-2x.csv') return '2x vzvod'
      if (file === 'vzvod-3x.csv') return '3x vzvod'
      return file
    }

    const formatNumber = (num: number) => {
      return new Intl.NumberFormat('sl-SI', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(num)
    }

    const formatPercent = (num: number) => {
      return `+${formatNumber(num)}%`
    }
    
    const naslovHtml = `
      <div style="padding: 12px 0; border-bottom: 2px solid #d1d5db; margin-bottom: 8px; font-weight: 700; line-height: 1.8;">
        Datum | NAJBOLJŠI (narejen plus/minus, vse skupaj) &nbsp; &gt;&gt; &nbsp; +% &nbsp; &gt;&gt; &nbsp; DRUGI (narejen plus/minus, vse skupaj) &nbsp; &gt;&gt; &nbsp; +% &nbsp; &gt;&gt; &nbsp; TRETJI (narejen plus/minus, vse skupaj)
      </div>
    `

    const summaryHtml = `
      <div style="margin-bottom: 20px; padding: 16px; background: #f9fafb; border-radius: 12px; line-height: 1.8;">
        <div><strong>Skupno primerjav:</strong> ${data.summary.total_compared}</div>
        <div>
          <strong style="color: ${getEtfColor('osnoven.csv')}">Osnoven:</strong>
          ${data.summary.wins["osnoven.csv"].count} (${data.summary.wins["osnoven.csv"].procent}%)
        </div>
        <div>
          <strong style="color: ${getEtfColor('vzvod-2x.csv')}">2x vzvod:</strong>
          ${data.summary.wins["vzvod-2x.csv"].count} (${data.summary.wins["vzvod-2x.csv"].procent}%)
        </div>
        <div>
          <strong style="color: ${getEtfColor('vzvod-3x.csv')}">3x vzvod:</strong>
          ${data.summary.wins["vzvod-3x.csv"].count} (${data.summary.wins["vzvod-3x.csv"].procent}%)
        </div>
      </div>
    `

    const vrsticeHtml = data.rows.map((row: any) => {
      const bestColor = getEtfColor(row.best.file)
      const secondColor = getEtfColor(row.second.file)
      const thirdColor = getEtfColor(row.third.file)

      return `
        <div style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; line-height: 1.9;">
          <strong>${row.datum}</strong>
          &nbsp; | &nbsp;

          <span style="color: ${bestColor}; font-weight: 700;">
            ${getEtfLabel(row.best.file)}
          </span>
          :
          <span style="color: ${bestColor}; font-weight: 600;">
            ${formatNumber(row.best.gain)}, ${formatNumber(row.best.total)}
          </span>

          &nbsp; &gt;&gt; &nbsp;
          <span style="color: #10B981; font-weight: 600;">
            ${formatPercent(row.diff_best_second_pct)}
          </span>
          &nbsp; &gt;&gt; &nbsp;

          <span style="color: ${secondColor}; font-weight: 700;">
            ${getEtfLabel(row.second.file)}
          </span>
          :
          <span style="color: ${secondColor}; font-weight: 600;">
            ${formatNumber(row.second.gain)}, ${formatNumber(row.second.total)}
          </span>

          &nbsp; &gt;&gt; &nbsp;
          <span style="color: #10B981; font-weight: 600;">
            ${formatPercent(row.diff_second_third_pct)}
          </span>
          &nbsp; &gt;&gt; &nbsp;

          <span style="color: ${thirdColor}; font-weight: 700;">
            ${getEtfLabel(row.third.file)}
          </span>
          :
          <span style="color: ${thirdColor}; font-weight: 600;">
            ${formatNumber(row.third.gain)}, ${formatNumber(row.third.total)}
          </span>
        </div>
      `
    }).join('')

    backendResponse.value = `
      <div style="padding: 20px; font-family: sans-serif;">
        <h2 style="color: #10B981; font-weight: bold; margin-bottom: 16px;">Povezava uspela!</h2>
        <p style="margin-bottom: 20px;">Prejeli smo odgovor iz endpointa /primerjava_vrstic.</p>
        ${summaryHtml}
        ${naslovHtml}
        <div style="display: flex; flex-direction: column; gap: 4px;">
          ${vrsticeHtml}
        </div>
      </div>
    `

    const res = await axios.post("http://localhost:8000/html-files", podatki_za_poslat)
    results.value = res.data.results || []

    console.log("Tole je iz backenda prišlo:", results.value)
    console.log(JSON.stringify(results.value, null, 2))

  } catch (error) {
    console.error("Poskus povezave spodletel:", error)
    alert("Prisotna je težava z backendom ali pa ne teče na portu 8000!")
  } finally {
    isLoading.value = false
  }
}

  const openHtml = (url: string) => {
    window.open(url, '_blank')
  }
</script>

<template>
  <div class="max-w-2xl mx-auto">
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
            
            <div class="relative">
              <select 
                v-model="selectedIndex"
                class="w-full px-4 py-3 pr-10 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] appearance-none cursor-pointer"
              >
                <option>S&P 500</option>
                <option>Nasdaq 100</option>
                <option>Nasdaq Composite</option>
              </select>

              <div class="pointer-events-none absolute inset-y-0 right-3 flex items-center text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Interval (leta)</label>
            <input 
              v-model="selectedInterval"
              type="number"
              min="1"
              max="50"
              placeholder="npr. 10"
              class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all placeholder:text-gray-300"
            />
          </div>
        </div>

        <!-- Calculate Button -->
        <button 
          @click="izracunaj"
          :disabled="isLoading || !isFormValid"
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
  </div>
    <!-- Results Section se prikaze le ko damo na true oz k dobim iz backenda response-->
    

      <div v-if="backendResponse" class="mt-10 flex justify-center px-6">
        <div class="w-full max-w-[1600px] bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <div v-html="backendResponse"></div>
        </div>
      </div>
    
    <div v-if="results.length > 0" class="mt-16 space-y-6">
      <h2 class="text-2xl font-bold text-[#1A1A1A] px-4">Rezultati simulacije</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="res in results" 
          :key="res.id"
          @click="openHtml(res.url)""
          class="bg-white p-6 rounded-2xl border border-gray-100 hover:border-[#10B981] hover:shadow-md transition-all cursor-pointer flex items-center justify-between group"
        >
          <div class="flex items-center gap-4">
            <div class="bg-emerald-50 p-3 rounded-xl text-[#10B981]">
              <FileText class="w-6 h-6" />
            </div>
            <span class="font-medium text-gray-700">{{"Simulacija Scenarij " + res.title }}</span>
          </div>
          <ChevronRight class="text-gray-300 group-hover:text-[#10B981] transition-colors" />
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
