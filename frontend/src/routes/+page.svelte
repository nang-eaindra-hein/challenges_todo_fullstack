<script lang="ts">


</script>
<div class="relative h-screen">
    <div class="h-2/5 bg-[url('/images/bg-desktop-light.jpg')] bg-no-repeat bg-cover"></div>

    <div class="h-3/5 bg-white"></div>

    <div class="absolute w-[90%] max-w-lg top-1/5 left-1/2 transform -translate-x-1/2 flex flex-col space-y-4 items-center justify-center">
        <div class="w-full flex items-center justify-between">
            <h1 class="text-4xl font-bold text-white">TODO</h1>
            <button>
                <img src="/images/icon-moon.svg" alt="Dark Mode">
            </button>
        </div>

        <input type="text" placeholder="Create a new todo..." class="w-full p-4 mt-4 text-lg bg-white rounded-md">

        <div>
            <ul class="w-48 select-none text-sm font-medium text-heading bg-neutral-primary-soft border border-default rounded-base">
                <li class="w-full border-b border-default rounded-t-lg">
                    <div class="flex items-center ps-3">
                        <input id="vue-checkbox" type="checkbox" value="" class="w-4 h-4 border border-default-medium rounded-xs bg-neutral-secondary-medium focus:ring-2 focus:ring-brand-soft">
                        <label for="vue-checkbox" class="w-full py-3 ms-2 text-sm font-medium text-heading">Vue JS</label>
                    </div>
                </li>
                <li class="w-full border-b border-default rounded-t-lg">
                    <div class="flex items-center ps-3">
                        <input id="react-checkbox" type="checkbox" value="" class="w-4 h-4 border border-default-medium rounded-xs bg-neutral-secondary-medium focus:ring-2 focus:ring-brand-soft">
                        <label for="react-checkbox" class="w-full py-3 ms-2 text-sm font-medium text-heading">React</label>
                    </div>
                </li>
                <li class="w-full border-b border-default rounded-t-lg">
                    <div class="flex items-center ps-3">
                        <input id="angular-checkbox" type="checkbox" value="" class="w-4 h-4 border border-default-medium rounded-xs bg-neutral-secondary-medium focus:ring-2 focus:ring-brand-soft">
                        <label for="angular-checkbox" class="w-full py-3 ms-2 text-sm font-medium text-heading">Angular</label>
                    </div>
                </li>
                <li class="w-full rounded-t-lg">
                    <div class="flex items-center ps-3">
                        <input id="laravel-checkbox" type="checkbox" value="" class="w-4 h-4 border border-default-medium rounded-xs bg-neutral-secondary-medium focus:ring-2 focus:ring-brand-soft">
                        <label for="laravel-checkbox" class="w-full py-3 ms-2 text-sm font-medium text-heading">Laravel</label>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</div>