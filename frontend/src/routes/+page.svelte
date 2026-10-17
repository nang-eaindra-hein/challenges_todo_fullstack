<script lang="ts">
  // import {onMount} from "svelte";
  import {
    getTodos,
    createTodo,
    updateStatus,
    deleteTodoById,
    updateTodoTitle,
    deleteTodos,
  } from "../lib/api/todos";
  import "../app.css";
  import { PencilIcon } from "@lucide/svelte";
  import toast, { Toaster } from "svelte-5-french-toast";
  import { createQuery } from "@tanstack/svelte-query";
  import { createMutation, useQueryClient } from "@tanstack/svelte-query";
  import { TodoStatusEnum, type Todo } from "../lib/types";

  const filters = [
    TodoStatusEnum.All,
    TodoStatusEnum.Completed,
    TodoStatusEnum.Active,
  ] as const;
  let deleteListConfirmationModal = $state(false);
  let deleteListsConfirmationModal = $state(false);

  const todosQuery = createQuery(() => ({
    queryKey: ["todos"],
    queryFn: getTodos,
  }));

  const queryClient = useQueryClient();

  const addTodoMutation = createMutation(() => ({
    mutationFn: createTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
      toast.success("Successfully created a list!");
    },
    onError: (error) => {
      toast.error("A todo with this title already exists.");
    },
  }));

  const updateStatusMutation = createMutation(() => ({
    mutationFn: ({ id, status }: { id: number; status: Todo["status"] }) =>
      updateStatus(id, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  }));

  const editTodoMutation = createMutation(() => ({
    mutationFn: ({ id, title }: { id: number; title: string }) =>
      updateTodoTitle(id, title),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["todos"] });

      toast.success("Successfully updated a list!");
    },
  }));

  const deleteTodoMutation = createMutation(() => ({
    mutationFn: deleteTodoById,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["todos"] });

      toast.success("Successfully delete a list!");
      deleteListConfirmationModal = false;
    },
  }));

  const deleteTodosMutation = createMutation(() => ({
    mutationFn: deleteTodos,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["todos"] });
      toast.success("Successfully clear all lists!");
      deleteListsConfirmationModal = false;
    },
  }));

  let isDarkMode = $state(false);
  let todos = $derived(todosQuery.data?.items ?? []);
  let newTodo = $state("");
  let editingTodoId = $state<number | null>(null);
  let editedTitle = $state("");

  let filter = $state<(typeof filters)[number]>(TodoStatusEnum.All);
  let filteredTodos = $derived(
    todos.filter((todo: any) => {
      if (filter === TodoStatusEnum.Active)
        return todo.status === TodoStatusEnum.Active;
      if (filter === TodoStatusEnum.Completed)
        return todo.status === TodoStatusEnum.Completed;
      return true;
    }),
  );
  let itemCounts = $derived(filteredTodos.length);

  function toggleDarkMode() {
    isDarkMode = !isDarkMode;
  }

  async function addTodo() {
    const title = newTodo.trim();
    if (!title) return;

    await addTodoMutation.mutateAsync(title);
    newTodo = "";
  }

  function startEditing(todo: Todo) {
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

    await editTodoMutation.mutateAsync({
      id: todo.id,
      title,
    });

    editingTodoId = null;
  }

  async function toggleTodo(todo: Todo) {
    const newStatus =
      todo.status === TodoStatusEnum.Active
        ? TodoStatusEnum.Completed
        : TodoStatusEnum.Active;

    await updateStatusMutation.mutateAsync({
      id: todo.id,
      status: newStatus,
    });
  }

  async function deleteOnetodo(todo: Todo) {
    await deleteTodoMutation.mutateAsync(todo.id);
  }

  function deletefilterTodos() {
    const type =
      filter === TodoStatusEnum.Active
        ? TodoStatusEnum.Active
        : filter === TodoStatusEnum.Completed
          ? TodoStatusEnum.Completed
          : TodoStatusEnum.All;

    deleteTodosMutation.mutate(type);
  }
</script>

{#snippet filterButtons()}
  {#each filters as f}
    <button
      class={[
        "capitalize font-bold transition-colors",
        filter === f
          ? "text-primary-blue-500"
          : "hover:text-light-navy-850 dark:hover:text-dark-purple-100",
      ]}
      onclick={() => (filter = f)}>{f}</button
    >
  {/each}
{/snippet}

<div
  class:dark={isDarkMode}
  class="relative min-h-screen flex flex-col bg-light-gray-50 dark:bg-dark-navy-950"
>
  <div
    class="absolute inset-x-0 top-0 h-50 md:h-75 bg-no-repeat bg-cover bg-[url('/images/bg-mobile-light.jpg')] dark:bg-[url('/images/bg-mobile-dark.jpg')] md:bg-[url('/images/bg-desktop-light.jpg')] md:dark:bg-[url('/images/bg-desktop-dark.jpg')]"
  ></div>

  <main
    class="relative flex-1 w-[90%] max-w-135 mx-auto pt-12 md:pt-[10vh] flex flex-col space-y-4 items-center text-xs md:text-lg"
  >
    <div class="w-full flex items-center justify-between">
      <h1
        class="text-2xl md:text-4xl font-bold tracking-[0.4em] text-light-gray-50"
      >
        TODO
      </h1>
      <button onclick={toggleDarkMode}>
        {#if isDarkMode}
          <img
            src="/images/icon-sun.svg"
            alt="Switch to light mode"
            class="w-5 md:w-auto"
          />
        {:else}
          <img
            src="/images/icon-moon.svg"
            alt="Switch to dark mode"
            class="w-5 md:w-auto"
          />
        {/if}
      </button>
    </div>

    <div
      class="w-full flex gap-3 md:gap-4 items-center rounded-md p-3.5 md:p-4 shadow-md bg-white dark:bg-dark-navy-900 text-light-navy-850 dark:text-dark-purple-100"
    >
      <div
        class="w-5 h-5 shrink-0 rounded-full border border-light-gray-300 dark:border-dark-purple-800"
      ></div>
      <input
        class="flex-1 outline-none caret-primary-blue-500 placeholder:text-light-gray-600 dark:placeholder:text-dark-purple-600"
        type="text"
        placeholder="Create a new todo..."
        bind:value={newTodo}
        onkeydown={(event) => {
          if (event.key === "Enter") addTodo();
        }}
      />
    </div>

    <div
      class="w-full bg-white dark:bg-dark-navy-900 rounded-md shadow-md overflow-hidden"
    >
      {#each filteredTodos as todo (todo.id)}
        <div
          class="group w-full flex gap-3 md:gap-4 items-center bg-white dark:bg-dark-navy-900 p-4 border-b border-dark-purple-100 dark:border-dark-purple-800"
        >
          <button
            aria-label="Toggle completion"
            class={[
              "w-5 h-5 shrink-0 rounded-full p-px flex items-center justify-center",
              todo.status === TodoStatusEnum.Completed
                ? "bg-linear-to-br from-check-start to-check-end"
                : "bg-light-gray-300 dark:bg-dark-purple-800 hover:bg-linear-to-br hover:from-check-start hover:to-check-end",
            ]}
            onclick={() => toggleTodo(todo)}
          >
            {#if todo.status === TodoStatusEnum.Completed}
              <img src="/images/icon-check.svg" alt="Completed" />
            {:else}
              <span
                class=" block w-full h-full rounded-full bg-white dark:bg-dark-navy-900"
              ></span>
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
            <p
              class="{todo.status === TodoStatusEnum.Completed
                ? 'line-through text-light-gray-300 dark:text-dark-purple-700'
                : 'text-light-navy-850 dark:text-light-purple-300'} flex-1"
            >
              {todo.title}
            </p>
          {/if}

          <button
            aria-label="Edit todo"
            onclick={() => startEditing(todo)}
            class={[
              "text-md transition-colors",
              editingTodoId === todo.id
                ? "text-primary-blue-500"
                : "text-light-gray-600 dark:text-dark-purple-600 hover:text-primary-blue-500",
            ]}
          >
            <PencilIcon />
          </button>

          <button
            aria-label="Delete todo"
            class="md:opacity-0 md:group-hover:opacity-100 md:focus:opacity-100 transition-opacity"
            onclick={() => {
              deleteListConfirmationModal = true;
            }}
          >
            <img src="/images/icon-cross.svg" alt="" />
          </button>
          {#if deleteListConfirmationModal}
            <div class=" inset-0 flex fixed justify-center items-center z-999">
              <div
                class="w-fit h-fit p-4 rounded-lg bg-white opacity-70 shadow-lg text-lg md:text-2xl text-light-gray-500"
              >
                Are you sure you want to delete this list?
                <div class="flex justify-end gap-2 text-sm text-white pt-4">
                  <button
                    class="bg-purple-400 rounded-lg px-2 py-1 hover:bg-purple-300"
                    onclick={() => deleteOnetodo(todo)}>Confirm</button
                  >
                  <button
                    class="bg-purple-400 rounded-lg px-2 py-1 hover:bg-purple-300"
                    onclick={() => {
                      deleteListConfirmationModal = false;
                    }}>Cancel</button
                  >
                </div>
              </div>
            </div>
          {/if}
        </div>
      {/each}

      <div
        class="p-4 flex justify-between text-xs md:text-sm text-light-gray-600 dark:text-dark-purple-600"
      >
        <span>{itemCounts} {filter} items</span>

        <div class="hidden md:flex gap-4">
          {@render filterButtons()}
        </div>

        <button
          onclick={() => (deleteListsConfirmationModal = true)}
          class="hover:text-light-navy-850 dark:hover:text-dark-purple-100 transition-colors"
          >Clear {filter}</button
        >
        {#if deleteListsConfirmationModal}
          <div class=" inset-0 flex fixed justify-center items-center z-999">
            <div
              class="w-fit h-fit p-4 rounded-lg bg-white shadow-lg text-lg md:text-2xl text-light-gray-500"
            >
              Are you sure you want to delete all lists?
              <div class="flex justify-end gap-2 text-sm text-white pt-4">
                <button
                  class="bg-purple-400 rounded-lg px-2 py-1 hover:bg-purple-300"
                  onclick={deletefilterTodos}>Confirm</button
                >
                <button
                  class="bg-purple-400 rounded-lg px-2 py-1 hover:bg-purple-300"
                  onclick={() => {
                    deleteListsConfirmationModal = false;
                  }}>Cancel</button
                >
              </div>
            </div>
          </div>
        {/if}
      </div>
    </div>

    <div
      class="md:hidden w-full flex justify-center gap-5 p-4 rounded-md shadow-md text-sm text-light-gray-600 dark:text-dark-purple-600 bg-white dark:bg-dark-navy-900"
    >
      {@render filterButtons()}
    </div>
  </main>

  <!-- <p class="py-10 text-center text-sm text-light-gray-600 dark:text-dark-purple-600">
            Drag and drop to reorder list
    </p> -->
</div>
<Toaster />
