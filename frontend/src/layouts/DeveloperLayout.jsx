import { useState } from 'react'
import { Outlet, NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  TicketCheck,
  ChevronLeft,
  LogOut,
  Menu,
} from 'lucide-react'
import { cn } from '@/utils/cn'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Sheet, SheetContent, SheetTitle, SheetDescription } from '@/components/ui/sheet'
import { VisuallyHidden } from '@radix-ui/react-visually-hidden'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import useAuth from '@/hooks/useAuth'
import useAuthStore from '@/store/authStore'

const navGroups = [
  {
    label: 'Main',
    items: [
      { label: 'Dashboard', icon: LayoutDashboard, to: '/developer', end: true },
      { label: 'My Tickets', icon: TicketCheck, to: '/developer/tickets' },
    ],
  },
]

const pageTitles = {
  '/developer': 'Dashboard',
  '/developer/tickets': 'My Tickets',
}

const NavItem = ({ item }) => {
  const Icon = item.icon
  return (
    <NavLink
      to={item.to}
      end={item.end}
      className={({ isActive }) =>
        cn(
          'flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
          isActive
            ? 'bg-slate-100 text-slate-900 font-medium'
            : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
        )
      }
    >
      <Icon className="h-4 w-4 shrink-0" />
      <span>{item.label}</span>
    </NavLink>
  )
}

const SidebarContent = ({ user, onLogout, onClose }) => (
  <div className="flex flex-col h-full">

    {/* Logo */}
    <div className="flex items-center justify-between h-14 px-4 border-b border-slate-100">
      <div className="flex items-center gap-2">
        <div className="h-6 w-6 rounded-md bg-slate-900 flex items-center justify-center">
          <TicketCheck className="h-3.5 w-3.5 text-white" />
        </div>
        <span className="text-sm font-semibold text-slate-900">SDD Tickets</span>
      </div>
      {onClose && (
        <Button variant="ghost" size="icon" onClick={onClose} className="h-7 w-7 lg:hidden">
          <ChevronLeft className="h-4 w-4" />
        </Button>
      )}
    </div>

    {/* Nav */}
    <nav className="flex-1 overflow-y-auto px-3 py-4 flex flex-col gap-6">
      {navGroups.map((group) => (
        <div key={group.label}>
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider px-3 mb-2">
            {group.label}
          </p>
          <div className="flex flex-col gap-0.5">
            {group.items.map((item) => (
              <NavItem key={item.to} item={item} />
            ))}
          </div>
        </div>
      ))}
    </nav>

    <Separator />

    {/* User */}
    <div className="p-3">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <button className="flex items-center gap-3 w-full rounded-md px-3 py-2 hover:bg-slate-50 transition-colors text-left">
            <Avatar className="h-7 w-7 shrink-0">
              <AvatarFallback className="bg-slate-200 text-slate-600 text-xs font-semibold">
                {user?.first_name?.[0]}{user?.last_name?.[0]}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-medium text-slate-900 truncate leading-tight">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-xs text-slate-400 truncate leading-tight">{user?.email}</p>
            </div>
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent side="top" align="start" className="w-56">
          <DropdownMenuLabel className="font-normal">
            <p className="font-medium text-sm">{user?.first_name} {user?.last_name}</p>
            <p className="text-xs text-slate-400">{user?.email}</p>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem
            onClick={onLogout}
            className="text-red-600 focus:text-red-600 focus:bg-red-50 cursor-pointer"
          >
            <LogOut className="mr-2 h-4 w-4" />
            Sign out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>

  </div>
)

const DeveloperLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const { handleLogout } = useAuth()
  const { user } = useAuthStore()
  const location = useLocation()

  const pageTitle =
    pageTitles[location.pathname] ||
    Object.entries(pageTitles).find(
      ([key]) => location.pathname.startsWith(key) && key !== '/developer'
    )?.[1] ||
    'Dashboard'

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">

      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex flex-col w-56 border-r border-slate-200 bg-white shrink-0">
        <SidebarContent user={user} onLogout={handleLogout} />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetContent side="left" className="w-56 p-0 border-r border-slate-200">
          <VisuallyHidden>
            <SheetTitle>Navigation Menu</SheetTitle>
            <SheetDescription>Main navigation sidebar</SheetDescription>
          </VisuallyHidden>
          <SidebarContent
            user={user}
            onLogout={handleLogout}
            onClose={() => setMobileOpen(false)}
          />
        </SheetContent>
      </Sheet>

      {/* Main content */}
      <div className="flex flex-col flex-1 overflow-hidden">

        {/* Mobile topbar */}
        <header className="lg:hidden flex items-center h-14 px-4 border-b border-slate-200 bg-white gap-3">
          <Button variant="ghost" size="icon" onClick={() => setMobileOpen(true)} className="h-8 w-8">
            <Menu className="h-4 w-4" />
          </Button>
          <div className="flex items-center gap-2">
            <div className="h-6 w-6 rounded-md bg-slate-900 flex items-center justify-center">
              <TicketCheck className="h-3.5 w-3.5 text-white" />
            </div>
            <span className="text-sm font-semibold text-slate-900">SDD Tickets</span>
          </div>
        </header>

        {/* Desktop topbar */}
        <header className="hidden lg:flex items-center justify-between h-14 px-6 border-b border-slate-200 bg-white shrink-0">
          <h1 className="text-sm font-semibold text-slate-900">{pageTitle}</h1>
          <Avatar className="h-7 w-7">
            <AvatarFallback className="bg-slate-200 text-slate-600 text-xs font-semibold">
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </AvatarFallback>
          </Avatar>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>

      </div>
    </div>
  )
}

export default DeveloperLayout