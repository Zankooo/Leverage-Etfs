<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import axios from 'axios'
import { Loader2 } from 'lucide-vue-next'

// ref () pomeni : Shrani vrednost in ob njeni spremembi samodejno posodobi dele uporabniškega vmesnika, ki jo uporabljajo.
const initialInvestment = ref('')
const monthlyContribution = ref('')
const selectedIndex = ref('S&P 500')
const selectedInterval = ref(15)


// spremenljivka ali je backend ze odgovoril, vrednost je lahko strinj ali null -> ob uspesnem gre na "true"
// pred zacetkom je null in rezultati so skriti, po uspesnem se da na true in rezulati se prikazejo
const backendResponse = ref<string | null>(null)
// Hrani seznam grafov, ki jih vrne backend, ko uporabnik klikne gumb za graf se url iz tega rezultata vzame
const grafi = ref<any[]>([])
// Hrani informacijo, ali backend trenutno računa.
const isLoading = ref(false)

// New refs for table rendering and modal
const tableRows = ref<any[]>([])
const tableSummary = ref<any | null>(null)
const showGraphModal = ref(false)
const selectedGraphUrl = ref('')
let revizijaVnosa = 0


// RAZLIKA MED WATCH IN COMPUTED
// computed uporabiš, ko želiš izračunano vrednost iz drugih ref vrednosti.
// Primer: totalInvested, isFormValid.
// watch uporabiš, ko želiš ob spremembi izvesti neko dejanje.
// Primer: pobrisati stare grafe, poslati zahtevo ali nekaj zapisati v konzolo.


// ta funkcija se vedno 'izvaja' - čaka da se spremeni kaj in ukrepa,
// razlika med computed in watch funkcijo je: 
//  torej če se naredi sprememba od eni od teh, se izvede koda
watch(
  [initialInvestment, monthlyContribution, selectedIndex, selectedInterval],
  () => {
    revizijaVnosa += 1
    // pocistimo od prej 
    backendResponse.value = null
    tableRows.value = []
    tableSummary.value = null
    grafi.value = []
    showGraphModal.value = false
    selectedGraphUrl.value = ''
  }
)

// ko das gumb izracunaj se ta funkcija zalaufa, pogleda ce je vse prav vpisano
// vsak computed spremlja tiste reaktivne vrednosti ki jih v sebi uporablja
// kakroli se spremeni, se funkcija ponovno izvede
const isFormValid = computed(function () {
  return initialInvestment.value !== '' &&
         monthlyContribution.value !== '' &&
         selectedInterval.value != null &&
         Number(selectedInterval.value) >= 1 &&
         Number(selectedInterval.value) <= 50
})

const totalInvested = computed(() => {
  const initial = Number(initialInvestment.value) || 0
  const monthly = Number(monthlyContribution.value) || 0
  const years = Number(selectedInterval.value) || 0
  return initial + (monthly * 12 * years)
})

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('sl-SI', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num)
}

const formatPercent = (num: number) => {
  return `+${formatNumber(num)}%`
}

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

async function izracunaj() {
  const revizijaObZacetku = revizijaVnosa
  // pocistimo od prej 
  backendResponse.value = null
  tableRows.value = []
  tableSummary.value = null
  grafi.value = []
  showGraphModal.value = false
  selectedGraphUrl.value = ''

  isLoading.value = true

  try {
    // podatki ki se posljejo
    const podatki_za_poslat = {
      zacetna_investicija: Number(initialInvestment.value),
      mesecni_vlozek: Number(monthlyContribution.value),
      indeks: selectedIndex.value,
      interval: Number(selectedInterval.value)
    }

    // KLICI NA BACKEND IN ODGOVORI
    // Najprej izvedemo prvi klic na backend, da se printi v konzoli ne mešajo
    const responseVrstice = await axios.post('http://localhost:8000/primerjava_vrstic', podatki_za_poslat)
    // Šele ko se prvi klic (in njegovi printi) zaključi, sprožimo drugega
    const responseGrafi = await axios.post('http://localhost:8000/html-files', podatki_za_poslat)

    // shranimo v variable saj je v lastnosti data to, saj data potrebujemo, je pa še več parametrov
    const dataVrstice = responseVrstice.data
    const dataGrafi = responseGrafi.data

    // da jih lahko kadarkoli pogledamo v dev toolsih v browserju
    console.log("Podatki za tabelo:", dataVrstice)
    console.log("Podatki za grafe:", dataGrafi)

    // zavržemo odgovor stare simulacije, ce je uporabnik zacel pisati nove parametre v formo
    if (revizijaObZacetku !== revizijaVnosa) {
      return
    }

    // Vse spremenljivke posodobimo hkrati
    tableSummary.value = dataVrstice.summary
    tableRows.value = dataVrstice.rows
    grafi.value = dataGrafi.results || []
    
    // Šele zdaj pokažemo rezultate
    backendResponse.value = "true" 

  } catch (error) {
    console.error("Poskus povezave spodletel:", error)
    alert("Prisotna je težava z backendom ali pa ne teče na portu 8000!")
  } finally {
    isLoading.value = false
  }
}

// ta funkcija se izvede kot clovek kliknen na gumb graf
const showGraph = (index: number) => {
  if (grafi.value[index]) {
    // Funkcija izbere URL ustreznega grafa, 
    // ta url se nahaja v odgovoru ki ga da backend
    selectedGraphUrl.value = grafi.value[index].url
    showGraphModal.value = true
  }
}

</script>

<template>
  <div class="simulation-home">
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
              :disabled="isLoading"
              type="number" 
              placeholder="npr. 1.000 €"
              class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all placeholder:text-gray-300 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
            />
          </div>

          <!-- Monthly Contribution -->
          <div>
            <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Mesečni vložek (€)</label>
            <input 
              v-model="monthlyContribution"
              :disabled="isLoading"
              type="number" 
              placeholder="npr. 100 €"
              class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all placeholder:text-gray-300 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
            />
          </div>

          <!-- Kater indeks -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-[#1A1A1A] mb-2">Indeks</label>
              
              <div class="relative">
                <select 
                  v-model="selectedIndex"
                  :disabled="isLoading"
                  class="w-full px-4 py-3 pr-10 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] appearance-none cursor-pointer disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
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
                :disabled="isLoading"
                type="number"
                min="1"
                max="50"
                placeholder="npr. 10"
                class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-base focus:outline-none focus:ring-2 focus:ring-[#10B981] focus:border-transparent transition-all placeholder:text-gray-300 disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
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



      <!-- Results Section -->
        <div v-if="backendResponse && tableRows.length > 0" class="mt-10 flex justify-center px-6">
          
          <div class="w-full max-w-[1600px] bg-transparent">
            <div style="font-family: sans-serif;">
              <h2 class="text-2xl font-bold text-[#1A1A1A] mb-8">Rezultati simulacije</h2>
              
              <!-- Summary Section Card -->
              <div v-if="tableSummary" class="bg-white p-8 rounded-[32px] border border-gray-100 shadow-sm mb-8">
                <div class="flex flex-col gap-8">


                  <!-- Vneseni parametri -->
                  <div class="pt-8 border-t border-gray-50">
                    <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                      <span class="bg-[#10B981]/10 p-2 rounded-lg text-[#10B981]">⚙️</span>
                      Vneseni parametri
                    </h3>
                    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
                      <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100/50">
                        <div class="text-[10px] font-black text-gray-400 uppercase tracking-wider mb-1">Začetna inv.</div>
                        <div class="text-lg font-bold text-[#1A1A1A]">{{ formatNumber(Number(initialInvestment)) }} €</div>
                      </div>
                      <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100/50">
                        <div class="text-[10px] font-black text-gray-400 uppercase tracking-wider mb-1">Mesečni vložek</div>
                        <div class="text-lg font-bold text-[#1A1A1A]">{{ formatNumber(Number(monthlyContribution)) }} €</div>
                      </div>
                      <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100/50">
                        <div class="text-[10px] font-black uppercase tracking-wider mb-1">Skupaj investirano</div>
                        <div class="text-lg font-bold">{{ formatNumber(totalInvested) }} €</div>
                      </div>
                      <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100/50">
                        <div class="text-[10px] font-black text-gray-400 uppercase tracking-wider mb-1">Doba (leta)</div>
                        <div class="text-lg font-bold text-[#1A1A1A]">{{ selectedInterval }} let</div>
                      </div>
                      <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100/50">
                        <div class="text-[10px] font-black text-gray-400 uppercase tracking-wider mb-1">Indeks</div>
                        <div class="text-lg font-bold text-[#1A1A1A]">{{ selectedIndex }}</div>
                      </div>
                    </div>
                  </div>
                  <!-- Vneseni parametri konec -->
                  
                  <div>
                    <hr class="border-0 border-t border-gray-100 my-3">
                  </div>

                  <!-- Povzetek primerjave -->
                  <div>
                    <h3 class="text-xl font-bold text-gray-800 mb-6 flex items-center gap-3">
                      <span class="bg-[#10B981]/10 p-2 rounded-lg text-[#10B981]">📊</span>
                      Povzetek primerjave
                    </h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">

                      <div class="p-4 bg-gray-50 rounded-2xl border border-gray-100/50">
                        <div class="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Skupno primerjav</div>
                        <div class="text-2xl font-bold text-gray-900">{{ tableSummary.total_compared }}</div>
                      </div>

                      <div v-for="(winData, file) in tableSummary.wins" :key="file" class="p-4 rounded-2xl bg-white border border-gray-100 shadow-sm">
                        <div class="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">{{ getEtfLabel(file as string) }}</div>
                        <div class="text-2xl font-bold" :style="{ color: getEtfColor(file as string) }">
                          {{ winData.count }} <span class="text-sm font-medium opacity-60">({{ winData.procent }}%)</span>
                        </div>
                      </div>

                    </div>

                  </div>
                  <!-- Povzetek primerjave konec -->
                 
              
                </div>
              </div>
              <!-- Summary Section Card -->

              <!-- Results List (Full-width "Rows") -->
              <div class="flex flex-col gap-4">
                <div 
                  v-for="(row, index) in tableRows" 
                  :key="index" 
                  class="bg-white p-5 rounded-[24px] border border-gray-100 shadow-sm hover:shadow-md transition-all flex flex-col lg:flex-row lg:items-center gap-6"
                >
                  <!-- Date column -->
                  <div class="shrink-0 lg:w-32">
                    <div class="bg-gray-50 px-4 py-2 rounded-full text-[13px] font-black text-gray-400 border border-gray-100 uppercase tracking-[0.15em] text-center">
                      {{ row.datum }}
                    </div>
                  </div>

                  <!-- Results - Horizontal Scroll/Flex -->
                  <div class="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Best -->
                    <div class="flex items-center gap-4 p-3 rounded-[20px] bg-white border-2 shadow-md" :style="{ borderColor: getEtfColor(row.best.file) + '50' }">
                      <div class="w-8 h-8 flex items-center justify-center rounded-full text-white font-bold text-xs shadow-sm shrink-0" :style="{ background: getEtfColor(row.best.file) }">1</div>
                      <div class="flex-1 min-w-0">
                        <div class="flex flex-wrap items-center gap-2 mb-0.5">
                          <span class="text-[14px] font-black uppercase tracking-tight truncate" :style="{ color: getEtfColor(row.best.file) }">{{ getEtfLabel(row.best.file) }}</span>
                          <span class="text-[10px] text-gray-500 font-extrabold bg-gray-100 px-1.5 py-0.5 rounded-md border border-gray-200">{{ formatPercent(row.diff_best_second_pct) }}</span>
                        </div>
                        <div class="text-lg font-black text-gray-900 leading-tight">
                          {{ formatNumber(row.best.total) }} <span class="text-xs font-medium text-gray-400">€</span>
                        </div>
                      </div>
                    </div>

                    <!-- Second -->
                    <div class="flex items-center gap-4 p-3 rounded-[20px] bg-white border-2 shadow-sm" :style="{ borderColor: getEtfColor(row.second.file) + '40' }">
                      <div class="w-8 h-8 flex items-center justify-center rounded-full text-white font-bold text-xs shadow-sm shrink-0" :style="{ background: getEtfColor(row.second.file) }">2</div>
                      <div class="flex-1 min-w-0">
                        <div class="flex flex-wrap items-center gap-2 mb-0.5">
                          <span class="text-[14px] font-black uppercase tracking-tight truncate" :style="{ color: getEtfColor(row.second.file) }">{{ getEtfLabel(row.second.file) }}</span>
                          <span class="text-[10px] text-gray-500 font-extrabold bg-gray-100 px-1.5 py-0.5 rounded-md border border-gray-200">{{ formatPercent(row.diff_second_third_pct) }}</span>
                        </div>
                        <div class="text-base font-black text-gray-900 leading-tight">
                          {{ formatNumber(row.second.total) }} <span class="text-xs font-medium text-gray-400">€</span>
                        </div>
                      </div>
                    </div>

                    <!-- Third -->
                    <div class="flex items-center gap-4 p-3 rounded-[20px] bg-white border-2 shadow-sm" :style="{ borderColor: getEtfColor(row.third.file) + '40' }">
                      <div class="w-8 h-8 flex items-center justify-center rounded-full text-white font-bold text-xs shadow-sm shrink-0" :style="{ background: getEtfColor(row.third.file) }">3</div>
                      <div class="flex-1 min-w-0">
                        <div class="mb-0.5 mt-1">
                          <span class="text-[14px] font-black uppercase tracking-tight truncate" :style="{ color: getEtfColor(row.third.file) }">{{ getEtfLabel(row.third.file) }}</span>
                        </div>
                        <div class="text-base font-black text-gray-900 leading-tight">
                          {{ formatNumber(row.third.total) }} <span class="text-xs font-medium text-gray-400">€</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- Third konec-->  

                  <!-- Button column klik na gumb GRAF -->
                  <div class="shrink-0">
                    <button
                      @click="showGraph(index)"
                      style="
                        background: #10B98120;
                        color: #059669;
                        font-weight: 900;
                        padding: 12px 28px;
                        border-radius: 14px;
                        cursor: pointer;
                        transition: all 0.2s ease;
                        font-size: 0.8125rem;
                        border: 2px solid #10B98130;
                        width: 100%;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                      "
                      onmouseover="this.style.background='#10B98130'; this.style.borderColor='#10B98150'; this.style.transform='translateX(4px)'"
                      onmojuseout="this.style.background='#10B98120'; this.style.borderColor='#10B98130'; this.style.transform='translateX(0)'"
                    >
                      Graf
                    </button>
                  </div>
                  <!-- Button column konec -->
                </div>
            </div>
          </div>
        </div>

        <!-- Graph Modal -->
        <div v-if="showGraphModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showGraphModal = false"></div>
          <div class="relative w-full max-w-[95vw] h-[90vh] bg-white rounded-3xl overflow-hidden shadow-2xl flex flex-col">
            <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between bg-white">
              <h3 class="text-xl font-bold text-gray-800">Pregled grafa</h3>
              <button 
                @click="showGraphModal = false"
                class="p-2 hover:bg-gray-100 rounded-full transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="flex-1 w-full h-full bg-gray-50">
              <!-- dvopicje pomeni da je src poveza z reaktivno spremeljivko selectedGraphUrl -->
              <!-- selectedGraphUrl  = http://localhost:8000/grafi/1930-01-02--1945-01-02.html -->
              <!-- tuki je v bistvu klic na backend, na ta link -->
               <iframe :src="selectedGraphUrl" class="w-full h-full border-none"></iframe>
            </div>
            </div>
          </div>
          <!-- Graph Modal konec-->
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
