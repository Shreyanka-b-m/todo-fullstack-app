import { useEffect, useState } from "react";
import "./App.css";
const API_URL = "https://todo-fullstack-app-un7y.onrender.com";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [isSignup, setIsSignup] = useState(false);
  const [loading, setLoading] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [token, setToken] = useState(localStorage.getItem("token"));

  // 🔹 Fetch tasks
  const fetchTasks = async () => {
    if (!token) return;

    const res = await fetch(`${API_URL}/tasks`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    fetchTasks();
  }, [token]);

  // 🔹 LOGIN
  const login = async () => {
    setLoading(true);

    try {
      const res = await fetch(
        `${API_URL}/login?email=${email}&password=${password}`,
        {
          method: "POST",
        }
      );

      const data = await res.json();

      if (res.ok && data.token) {
        localStorage.setItem("token", data.token);
        setToken(data.token);
      } else {
        alert(data.error || data.detail || "Login failed");
      }
    } catch {
      alert("Unable to connect to server");
    }

    setLoading(false);
  };

  const signup = async () => {
    setLoading(true);

    try {
      const res = await fetch(
        `${API_URL}/signup?email=${email}&password=${password}`,
        {
          method: "POST",
        }
      );

      const data = await res.json();

      if (res.ok) {
        alert("Account created successfully!");
        setIsSignup(false);
      } else {
        alert(data.detail || "Signup failed");
      }
    } catch {
      alert("Unable to connect to server");
    }

    setLoading(false);
  };

  // 🔹 LOGOUT
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setTasks([]);
  };

  // 🔹 ADD TASK
  const addTask = async () => {
    if (!title.trim()) return;

    await fetch(`${API_URL}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title }),
    });

    setTitle("");
    fetchTasks();
  };

  // 🔹 COMPLETE
  const completeTask = async (id) => {
    await fetch(`${API_URL}/tasks/${id}`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchTasks();
  };

  // 🔹 DELETE
  const deleteTask = async (id) => {
    if (!confirm("Delete this task?")) return;

    await fetch(`${API_URL}/tasks/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    fetchTasks();
  };

  // 🔴 If NOT logged in → show login UI
  if (!token) {
    return (
      <div className="container">
        <h1>
          {isSignup ? "📝 Create Account" : "🔐 Login"}
        </h1>

        <div className="input-section">
          <input
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="input-section">
          <input
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button
          className="add-btn"
          disabled={loading}
          onClick={isSignup ? signup : login}
        >
          {loading
            ? "Please wait..."
            : isSignup
              ? "Sign Up"
              : "Login"}
        </button>
        <p style={{ marginTop: "15px" }}>
          {isSignup ? (
            <>
              Already have an account?{" "}
              <span
                style={{ cursor: "pointer", color: "#4ade80" }}
                onClick={() => setIsSignup(false)}
              >
                Login
              </span>
            </>
          ) : (
            <>
              Don't have an account?{" "}
              <span
                style={{ cursor: "pointer", color: "#4ade80" }}
                onClick={() => setIsSignup(true)}
              >
                Sign Up
              </span>
            </>
          )}
        </p>
      </div>
    );
  }

  // 🟢 If logged in → show app
  return (
    <div className="container">
      <h1>📝 My Todo App</h1>

      <button onClick={logout} style={{ marginBottom: "15px" }}>
        Logout
      </button>

      <div className="input-section">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task..."
        />
        <button className="add-btn" onClick={addTask}>
          Add
        </button>
      </div>

      {tasks.map((task) => (
        <div className="task-item" key={task.id}>
          <span
            className={`task-text ${task.completed ? "completed" : ""
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