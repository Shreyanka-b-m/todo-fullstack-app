import { useEffect, useState } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  // Fetch tasks
  const fetchTasks = async () => {
    const res = await fetch("http://localhost:8000/tasks");
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Add task
  const addTask = async () => {
    await fetch("http://localhost:8000/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    });

    setTitle("");
    fetchTasks();
  };

  // Mark complete
  const completeTask = async (id) => {
    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: "PUT",
    });

    fetchTasks();
  };

  // Delete task
  const deleteTask = async (id) => {
    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: "DELETE",
    });

    fetchTasks();
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Todo App</h1>

      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter task"
      />
      <button onClick={addTask}>Add</button>

      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {task.title} - {task.completed ? "Done" : "Pending"}

            <button onClick={() => completeTask(task.id)}>✔</button>
            <button onClick={() => deleteTask(task.id)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;







// Understand This (Very Important)
// Fetch Data
// fetch("http://localhost:8000/tasks")

// 👉 Calls your FastAPI GET API

// Add Task
// method: "POST"

// 👉 Calls your POST API

// Complete Task
// method: "PUT"

// 👉 Calls your PUT API

// Delete Task
// method: "DELETE"

// 👉 Calls your DELETE API

// 🔁 Full Flow Now
// React UI
//    ↓
// fetch()
//    ↓
// FastAPI
//    ↓
// SQL Query
//    ↓
// MariaDB
//    ↓
// Response
//    ↓
// React updates UI