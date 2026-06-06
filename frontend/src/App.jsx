import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchTasks = async () => {
    const res = await fetch("http://localhost:8000/tasks");
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const addTask = async () => {
    if (!title.trim()) return;

    setLoading(true);

    await fetch("http://localhost:8000/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    });

    setTitle("");
    setLoading(false);
    fetchTasks();
  };

  const completeTask = async (id) => {
    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: "PUT",
    });
    fetchTasks();
  };

  const deleteTask = async (id) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: "DELETE",
    });
    fetchTasks();
  };

  return (
    <div className="container">
      <h1>📝 My Todo App</h1>

      <div className="input-section">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter a new task..."
        />
        <button className="add-btn" onClick={addTask}>
          {loading ? "Adding..." : "Add"}
        </button>
      </div>

      {tasks.map((task) => (
        <div className="task-item" key={task.id}>
          <span
            className={`task-text ${
              task.completed ? "completed" : ""
            }`}
          >
            {task.title}
          </span>

          <div className="actions">
            <button
              className="complete-btn"
              onClick={() => completeTask(task.id)}
            >
              ✔ Complete
            </button>

            <button
              className="delete-btn"
              onClick={() => deleteTask(task.id)}
            >
              ❌ Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default App;