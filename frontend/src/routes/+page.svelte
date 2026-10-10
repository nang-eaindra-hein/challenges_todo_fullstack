<script lang="ts">
    import "../app.css";

    const filters = ["all", "active", "completed"] as const;
    type Todo = { text: string; completed: boolean };

    let isDarkMode = $state(false);
    let todos = $state<Todo[]>([]);
    let newTodo = $state("");
    let activeTodos = $derived(todos.filter(todo => !todo.completed).length);
    let filter = $state<typeof filters[number]>("all");
    let filteredTodos = $derived(
        todos.filter(todo => {
            if (filter === "active") return !todo.completed;
            if (filter === "completed") return todo.completed;
            return true;
        })
    );

    function toggleDarkMode() {
        isDarkMode = !isDarkMode;
    }

    function addTodo(){

        if (!newTodo.trim()) return;

        todos.push({
            text: newTodo,
            completed: false
        });

        newTodo = "";
    }

    function deleteTodo(todo: Todo) {
        todos = todos.filter(t => t !== todo);
    }

    function clearCompleted() {
        todos = todos.filter(todo => !todo.completed);
    }

</script>

{#snippet filterButtons()}
    {#each filters as f}
        <button
            class={[
                "capitalize font-bold transition-colors",
                filter === f
                    ? "text-primary-blue-500"
                    : "hover:text-light-navy-850 dark:hover:text-dark-purple-100"
                ]}
            onclick={() => filter = f}>{f}</button>
    {/each}
{/snippet}

<div class:dark={isDarkMode} class="relative min-h-screen flex flex-col bg-light-gray-50 dark:bg-dark-navy-950">

    <div class="absolute inset-x-0 top-0 h-50 md:h-75 bg-no-repeat bg-cover bg-[url('/images/bg-mobile-light.jpg')] dark:bg-[url('/images/bg-mobile-dark.jpg')] md:bg-[url('/images/bg-desktop-light.jpg')] md:dark:bg-[url('/images/bg-desktop-dark.jpg')] "></div>

    <main class="relative flex-1 w-[90%] max-w-135 mx-auto pt-12 md:pt-[10vh] flex flex-col space-y-4 items-center text-xs md:text-lg">
        <div class="w-full flex items-center justify-between">
            <h1 class="text-2xl md:text-4xl font-bold tracking-[0.4em] text-light-gray-50">TODO</h1>
            <button onclick={toggleDarkMode}>
                {#if isDarkMode}
                        <img src="/images/icon-sun.svg" alt="Switch to light mode" class="w-5 md:w-auto">
                    {:else}
                        <img src="/images/icon-moon.svg" alt="Switch to dark mode" class="w-5 md:w-auto">
                    {/if}
            </button>
        </div>

        <div class="w-full flex gap-3 md:gap-4 items-center rounded-md p-3.5 md:p-4 shadow-md bg-white dark:bg-dark-navy-900 text-light-navy-850 dark:text-dark-purple-100">

            <div class="w-5 h-5 shrink-0 rounded-full border border-light-gray-300 dark:border-dark-purple-800"></div>
            <input class="flex-1 outline-none caret-primary-blue-500 placeholder:text-light-gray-600 dark:placeholder:text-dark-purple-600" type="text" placeholder="Create a new todo..." bind:value={newTodo}  onkeydown={(event) => {if (event.key === 'Enter') addTodo();}}>

        </div>

        <div class="w-full bg-white dark:bg-dark-navy-900 rounded-md shadow-md overflow-hidden">
            {#each filteredTodos as todo}
                <div class="group w-full flex gap-3 md:gap-4 items-center bg-white dark:bg-dark-navy-900 p-4 border-b border-dark-purple-100 dark:border-dark-purple-800">
                    <button
                        aria-label="Toggle completion"
                        class={["w-5 h-5 shrink-0 rounded-full p-px flex items-center justify-center", todo.completed ? "bg-linear-to-br from-check-start to-check-end" : "bg-light-gray-300 dark:bg-dark-purple-800 hover:bg-linear-to-br hover:from-check-start hover:to-check-end"]}
                        onclick={() => todo.completed = !todo.completed}
                    >
                        {#if todo.completed}
                            <img src="/images/icon-check.svg" alt="Completed">
                        {:else}
                            <span class=" block w-full h-full rounded-full bg-white dark:bg-dark-navy-900"></span>
                        {/if}
                    </button>

                    <p class={["flex-1", todo.completed ? "line-through text-light-gray-300 dark:text-dark-purple-700" : "text-light-navy-850 dark:text-light-purple-300"]}>
                        {todo.text}
                    </p>

                    <button
                        aria-label="Delete todo"
                        class="md:opacity-0 md:group-hover:opacity-100 md:focus:opacity-100 transition-opacity"
                        onclick={() => deleteTodo(todo)}
                    >
                        <img src="/images/icon-cross.svg" alt="">
                    </button>
                </div>
            {/each}

            <div class="p-4 flex justify-between text-xs md:text-sm text-light-gray-600 dark:text-dark-purple-600">
                <span>{activeTodos} items left</span>

                <div class="hidden md:flex gap-4">
                    {@render filterButtons()}
                </div>

                <button onclick={clearCompleted} class="hover:text-light-navy-850 dark:hover:text-dark-purple-100 transition-colors">Clear Completed</button>
            </div>
        </div>

        <div class="md:hidden w-full flex justify-center gap-5 p-4 rounded-md shadow-md text-sm text-light-gray-600 dark:text-dark-purple-600 bg-white dark:bg-dark-navy-900">
            {@render filterButtons()}
        </div>
    </main>

    <p class="py-10 text-center text-sm text-light-gray-600 dark:text-dark-purple-600">
            Drag and drop to reorder list
    </p>
</div>
