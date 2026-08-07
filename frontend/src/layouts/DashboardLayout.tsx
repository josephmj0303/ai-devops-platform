import { Outlet } from "react-router-dom";

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-slate-100">
      <header className="bg-blue-700 text-white p-4 text-xl font-semibold">
        AI DevOps Platform
      </header>

      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
