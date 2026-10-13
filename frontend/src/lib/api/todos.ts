export type TodoStatus = "Active" | "Completed";

export type Todo = {
    id: number;
    title: string;
    status: TodoStatus;
};

export type TodoList = {
  items: Todo[];
  count: number;
}

export async function getTodos(): Promise<TodoList> {
    const res = await fetch('/todos');
    if (!res.ok) {
      throw new Error(`Request failed: ${res.status}`);
    }
    return res.json();
}

export async function createTodo(title: string): Promise<Todo> {
  const res = await fetch("/todo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export async function updateStatus(id: number, status: TodoStatus): Promise<Todo> {
  const res = await fetch(`/todo-status/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export async function deleteTodoById(id: number): Promise<void> {
  const res = await fetch(`/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
}