<template>
  <div class="max-w-2xl mx-auto">
    <header class="mb-12 text-center">
      <h1 class="text-4xl font-bold text-[#1A1A1A] mb-4">Stopite v stik</h1>
      <p class="text-gray-500">Imate vprašanja ali predloge? Pišite nam.</p>
    </header>

    <form @submit.prevent class="space-y-6 bg-white p-10 rounded-3xl border border-gray-100 shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Ime</label>
          <input type="text" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10B981] outline-none" placeholder="Janez">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input type="email" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10B981] outline-none" placeholder="janez@primer.si">
        </div>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Sporočilo</label>
        <textarea rows="4" class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-[#10B981] outline-none" placeholder="Kako vam lahko pomagamo?"></textarea>
      </div>
      <button class="w-full py-4 bg-gray-900 text-white font-bold rounded-xl hover:bg-black transition-colors">
        Pošlji sporočilo
      </button>
    </form>

    <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
      <div>
        <div class="text-gray-400 mb-2 text-sm uppercase font-bold tracking-widest">Email</div>
        <div class="font-medium">info@vzvodno.si</div>
      </div>
      <div>
        <div class="text-gray-400 mb-2 text-sm uppercase font-bold tracking-widest">Telefon</div>
        <div class="font-medium">+386 41 000 000</div>
      </div>
      <div>
        <div class="text-gray-400 mb-2 text-sm uppercase font-bold tracking-widest">Lokacija</div>
        <div class="font-medium">Ljubljana, Slovenija</div>
      </div>
    </div>
  </div>
</template>
