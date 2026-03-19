import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import useAuthStore from "./store/authStore";

// Layouts
import PublicLayout from "./layouts/PublicLayout";
import AdminLayout from "./layouts/AdminLayout";
import DeveloperLayout from "./layouts/DeveloperLayout";

// Public Pages
import LoginPage from "./pages/auth/LoginPage.jsx";
import SubmitTicketPage from "./pages/public/SubmitTicketPage";
import TrackTicketPage from "./pages/public/TrackTicketPage";

// Admin Pages
import AdminDashboardPage from "./pages/admin/DashboardPage";
import AdminTicketsPage from "./pages/admin/TicketsPage";
import AdminTicketDetailPage from "./pages/admin/TicketDetailsPage";
import AdminUsersPage from "./pages/admin/UsersPage";
import AdminOfficesPage from "./pages/admin/OfficesPage";
import AdminSystemsPage from "./pages/admin/SystemsPage";
import AdminConcernTypesPage from "./pages/admin/ConcernTypesPage";

// Developer Pages
import DeveloperDashboardPage from "./pages/developer/DashboardPage";
import DeveloperTicketsPage from "./pages/developer/TicketsPage";
import DeveloperTicketDetailsPage from "./pages/developer/TicketDetailsPage";
import NotFound from "./pages/NotFound";

/**
 * Route guard for authenticated routes.
 * Redirects to login if not authenticated.
 */

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user } = useAuthStore();

  if (!user) return <Navigate to={"/login"} replace />;
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to={"/login"} replace />;
  }

  return children;
};

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<SubmitTicketPage />} />
          <Route path="/track" element={<TrackTicketPage />} />
        </Route>

        {/* Auth Route */}
        <Route path="/login" element={<LoginPage />}></Route>

        {/* Admin Routes */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<AdminDashboardPage />} />
          <Route path="tickets" element={<AdminTicketsPage />} />
          <Route path="tickets/:ulid" element={<AdminTicketDetailPage />} />
          <Route path="users" element={<AdminUsersPage />} />
          <Route path="offices" element={<AdminOfficesPage />} />
          <Route path="systems" element={<AdminSystemsPage />} />
          <Route path="concern-types" element={<AdminConcernTypesPage />} />
        </Route>

        {/* Developer Routes */}
        <Route
          path="/developer"
          element={
            <ProtectedRoute allowedRoles={["developer"]}>
              <DeveloperLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DeveloperDashboardPage />} />
          <Route path="tickets" element={<DeveloperTicketsPage />} />
          <Route
            path="tickets/:ulid"
            element={<DeveloperTicketDetailsPage />}
          />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
