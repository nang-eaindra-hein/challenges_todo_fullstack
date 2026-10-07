<script lang="ts">

    let todos = $state([]);
    let newTodo = $state("");
    let activeTodos = $derived(todos.filter(todo => !todo.completed).length);
    let filter = $state("all");
    let filteredTodos = $derived(
        todos.filter(todo => {
            if (filter === "active") return !todo.completed;
            if (filter === "completed") return todo.completed;
            return true;
        })
    );

    function addTodo(){

        if (!newTodo.trim()) return;

        todos.push({
            text: newTodo,
            completed: false
        });

        newTodo = "";
    }

    function clearCompleted() {
        todos = todos.filter(todo => !todo.completed);
    }

</script>

<div class="relative h-screen">
    <div class="h-[300px] bg-[url('/images/bg-desktop-light.jpg')] bg-no-repeat bg-cover"></div>

    <div class="flex-1 bg-gray-50"></div>

    <div class="absolute w-[90%] max-w-[540px] top-[10%] left-1/2 -translate-x-1/2 flex flex-col space-y-4 items-center">
        <div class="w-full flex items-center justify-between">
            <h1 class="text-4xl font-bold text-gray-50">TODO</h1>
            <button>
                <img src="/images/icon-moon.svg" alt="Dark Mode">
            </button>
        </div>

        <div class="w-full flex gap-4 items-center bg-white rounded-md p-4">

            <input class="h-5 w-5" type="checkbox">

            <input class="flex-1 border-none outline-none font-[josefin-sans]" type="text" placeholder="Create a new todo..." bind:value={newTodo}  onkeydown={(event) => {if (event.key === 'Enter') addTodo();}}>

        </div>

        <div class="w-full bg-white rounded-md shadow-md overflow-hidden">
            {#each filteredTodos as todo}
                <div class="w-full flex gap-4 items-center bg-white p-4 border-b font-[josefin-sans]">
                    <input class="w-5 h-5" type="checkbox" bind:checked={todo.completed}>
                    <p class="flex-1 font-[josefin-sans]" class:text-gray-400={todo.completed} class:line-through={todo.completed}>{todo.text}</p>
                </div>
            {/each}

            <div class="w-full bg-white p-4 flex justify-between font-[josefin-sans] text-gray-400 text-sm">
                <span>{activeTodos} items left</span>

                <div class="flex gap-4 hover:text-navy-500 transition-colors">
                    <button onclick={() => filter = "all"}>All</button>
                    <button onclick={() => filter = "active"}>Active</button>
                    <button onclick={() => filter = "completed"}>Completed</button>
                </div>

                <button onclick={clearCompleted}>Clear Completed</button>
            </div>
        </div>

        <p class="text-center text-gray-400 text-sm font-[josefin-sans]">
            Drag and drop to reorder list
        </p>

    </div>
</div>
