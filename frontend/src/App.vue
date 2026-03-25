<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { Menu, X, TrendingUp } from 'lucide-vue-next'
import { ref } from 'vue'

const route = useRoute()
const isMenuOpen = ref(false)

const navItems = [
  { name: 'Simulacija', path: '/' },
  { name: 'O projektu', path: '/about' },
  { name: 'Prednosti', path: '/features' },
  { name: 'Kontakt', path: '/contact' },
]
</script>

<template>
  <div class="min-h-screen flex flex-col bg-[#F8F9FA] text-[#1A1A1A] font-sans">
    <!-- Navigation -->
    <nav class="bg-white border-b border-gray-100 sticky top-0 z-50">
      <div class="max-w-screen-2xl mx-auto px-6 lg:px-10 xl:px-12">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center gap-2">
            <TrendingUp class="text-[#10B981] w-6 h-6" />
            <span class="text-xl font-semibold tracking-tight">Vzvodno</span>
          </div>
          
          <!-- Desktop Nav -->
          <div class="hidden md:flex space-x-8">
            <RouterLink 
              v-for="item in navItems" 
              :key="item.path"
              :to="item.path"
              class="text-sm font-medium transition-colors hover:text-[#10B981]"
              :class="route.path === item.path ? 'text-[#10B981]' : 'text-gray-500'"
            >
              {{ item.name }}
            </RouterLink>
          </div>

          <!-- Mobile Menu Button -->
          <div class="md:hidden">
            <button @click="isMenuOpen = !isMenuOpen" class="text-gray-500 hover:text-gray-700">
              <Menu v-if="!isMenuOpen" class="w-6 h-6" />
              <X v-else class="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Nav -->
      <div v-if="isMenuOpen" class="md:hidden bg-white border-t border-gray-100 py-4 px-4 space-y-2">
        <RouterLink 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="block py-2 text-base font-medium text-gray-600 hover:text-[#10B981]"
          @click="isMenuOpen = false"
        >
          {{ item.name }}
        </RouterLink>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="w-full max-w-2xl mx-auto py-12 px-6 lg:px-10 xl:px-12">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 py-7 mt-auto">
      <div class="max-w-screen-2xl mx-auto px-6 lg:px-10 xl:px-12 text-center">
        <p class="text-gray-400 text-sm">© 2026 Vzvodno Investiranje. Vse pravice pridržane.</p>
      </div>
    </footer>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar for a more elegant look */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
}
::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>
