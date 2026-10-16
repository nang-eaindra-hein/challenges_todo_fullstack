export enum TodoStatusEnum {
  Active = "Active",
  Completed = "Completed",
  All = "All"
}
export type Todo = {
    id: number;
    title: string;
    status: TodoStatusEnum;
};

export type TodoList = {
  items: Todo[];
  count: number;
}

