import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function DashboardLayout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `block px-4 py-3 rounded ${
      isActive
        ? "bg-blue-600 text-white"
        : "text-gray-700 hover:bg-gray-100"
    }`;

  return (
    <div className="min-h-screen bg-gray-100">

      {/* Header */}

      <header className="bg-gray-900 text-white px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">
          AI DevOps Platform
        </h1>

        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded"
        >
          Logout
        </button>
      </header>

      <div className="flex">

        {/* Sidebar */}

        <aside className="w-64 bg-white min-h-[calc(100vh-72px)] shadow-sm p-4">

          <nav className="space-y-2">

            <NavLink
              to="/dashboard"
              className={linkClass}
            >
              Dashboard
            </NavLink>

            <NavLink
              to="/projects"
              className={linkClass}
            >
              Projects
            </NavLink>

            <NavLink
              to="/ai"
              className={linkClass}
            >
              AI Assistant
            </NavLink>

          </nav>

        </aside>

        {/* Main Content */}

        <main className="flex-1 p-6">
          <Outlet />
        </main>

      </div>

    </div>
  );
}
