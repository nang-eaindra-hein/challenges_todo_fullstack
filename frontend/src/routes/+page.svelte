<script lang="ts">
    import {onMount} from "svelte";
    import { getTodos, createTodo, updateStatus, deleteTodoById, updateTodoTitle, deleteTodos, type Todo } from "../lib/api/todos";;
    import "../app.css";
    import PencilIcon from '~icons/lucide/pencil';

    const filters = ["all", "active", "completed"] as const;
    
    let isDarkMode = $state(false);
    let todos = $state<Todo[]>([]);
    let newTodo = $state("");
    let editingTodoId = $state<number | null>(null);
    let editedTitle = $state("");
    
    let filter = $state<typeof filters[number]>("all");
    let filteredTodos = $derived(
        todos.filter(todo => {
            if (filter === "active") return todo.status === "Active";
            if (filter === "completed") return todo.status === "Completed";
            return true;
        })
    );
    let itemCounts =$derived(filteredTodos.length);
    
    async function toggleDarkMode() {
        isDarkMode = !isDarkMode;
    }

    onMount(async () => {
        const data = await getTodos();
        todos = data.items;
    });

    async function addTodo() {
        const title = newTodo.trim();
        if (!title) return;

        const created = await createTodo(title);
        todos.push(created);
        newTodo = "";
    }

    async function startEditing(todo: Todo) {
        if (editingTodoId === todo.id) {
            // Cancel editing
            editingTodoId = null;
            editedTitle = "";
        } else {
            // Start editing
            editingTodoId = todo.id;
            editedTitle = todo.title;
        }
    }

    async function saveTodo(todo: Todo) {
        const title = editedTitle.trim();

        if (!title) return;

        const updated = await updateTodoTitle(todo.id, title);
        todos = todos.map((t) => t.id === todo.id ? updated : t);

        editingTodoId = null;
    }

    async function toggleTodo(todo: Todo) {
        const newStatus = todo.status === "Active" ? "Completed" : "Active";
        const updated = await updateStatus(todo.id, newStatus);
        todo.status = updated.status;
    }

    async function deleteOnetodo(todo: Todo) {
        await deleteTodoById(todo.id);
        todos = todos.filter(t => t.id !== todo.id);
    }

    async function deletefilterTodos() {
         const type = filter === "active" ? "Active" : filter === "completed" ? "Completed" : "All";

        await deleteTodos(type);

        todos = todos.filter(todo => {
            if (filter === "active") return todo.status !== "Active";
            if (filter === "completed") return todo.status !== "Completed";
            return false;
        });
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
            {#each filteredTodos as todo(todo.id)}
                <div class="group w-full flex gap-3 md:gap-4 items-center bg-white dark:bg-dark-navy-900 p-4 border-b border-dark-purple-100 dark:border-dark-purple-800">
                    <button
                        aria-label="Toggle completion"
                        class={["w-5 h-5 shrink-0 rounded-full p-px flex items-center justify-center", todo.status === "Completed" ? "bg-linear-to-br from-check-start to-check-end" : "bg-light-gray-300 dark:bg-dark-purple-800 hover:bg-linear-to-br hover:from-check-start hover:to-check-end"]}
                        onclick={() => toggleTodo(todo)}
                    >
                        {#if todo.status === "Completed"}
                            <img src="/images/icon-check.svg" alt="Completed">
                        {:else}
                            <span class=" block w-full h-full rounded-full bg-white dark:bg-dark-navy-900"></span>
                        {/if}
                    </button>

                   {#if editingTodoId === todo.id}
                        <input
                            type="text"
                            class="flex-1 min-w-0 bg-transparent outline outline-light-navy-850 dark:outline-light-purple-300 p-2 rounded caret-primary-blue-500 text-light-navy-850 dark:text-light-purple-300"
                            bind:value={editedTitle}
                            onkeydown={(event) => {
                                if (event.key === "Enter") {
                                    saveTodo(todo);
                                }
                                
                            }}
                            onblur={() => {
                                editingTodoId = null;
                                editedTitle = "";
                            }}
                        />
                    {:else}
                        <p class={["flex-1", todo.status === "Completed" ? "line-through text-light-gray-300 dark:text-dark-purple-700" : "text-light-navy-850 dark:text-light-purple-300"]}>
                            {todo.title}
                        </p>
                    {/if}

                    <button aria-label="Edit todo" onclick={() => startEditing(todo)} class={["text-md transition-colors", editingTodoId === todo.id ? "text-primary-blue-500": "text-light-gray-600 dark:text-dark-purple-600 hover:text-primary-blue-500"]}>
                        <PencilIcon />
                    </button>

                    <button
                        aria-label="Delete todo"
                        class="md:opacity-0 md:group-hover:opacity-100 md:focus:opacity-100 transition-opacity"
                        onclick={() => deleteOnetodo(todo)}
                    >
                        <img src="/images/icon-cross.svg" alt="">
                    </button>
                </div>
            {/each}

            <div class="p-4 flex justify-between text-xs md:text-sm text-light-gray-600 dark:text-dark-purple-600">
                <span>{itemCounts} {filter} items</span>

                <div class="hidden md:flex gap-4">
                    {@render filterButtons()}
                </div>

                <button onclick={deletefilterTodos} class="hover:text-light-navy-850 dark:hover:text-dark-purple-100 transition-colors">Clear {filter}</button>
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
