// src/pages/admin/DashboardPage.jsx

import useDocumentTitle from "@/hooks/useDocumentTitle";

const AdminDashboardPage = () => {
  useDocumentTitle("Dashboard");
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
      <p className="text-slate-500 mt-1">Welcome back, Admin.</p>
    </div>
  );
};
export default AdminDashboardPage;
