import type { Todo, TodoList, TodoStatusEnum } from "#lib/types.ts";

//get todos
export async function getTodos(): Promise<TodoList> {
    const res = await fetch('/todos');
    if (!res.ok) {
      throw new Error(`Request failed: ${res.status}`);
    }
    return res.json(); 

}

//create todo
export async function createTodo(title: string): Promise<Todo> {
  const res = await fetch("/todo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

//update todo title
export async function updateTodoTitle(
    id: number,
    title: string
): Promise<Todo> {
    const res = await fetch(`/todo/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
    });

    if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
    }

    return res.json();
}

//update todo status
export async function updateStatus(id: number, status: TodoStatusEnum): Promise<Todo> {
  const res = await fetch(`/todo/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

//delete todo by id
export async function deleteTodoById(id: number): Promise<void> {
  const res = await fetch(`/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
}

//delete all
export async function deleteTodos(type: TodoStatusEnum): Promise<void> {
  const res = await fetch(`/delete-todos?type=${type}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
}