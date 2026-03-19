// src/pages/admin/DashboardPage.jsx

import useDocumentTitle from "@/hooks/useDocumentTitle";

const DeveloperDashboardPage = () => {
  useDocumentTitle("Dashboard");
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
      <p className="text-slate-500 mt-1">Welcome back, Developer.</p>
    </div>
  );
};
export default DeveloperDashboardPage;
