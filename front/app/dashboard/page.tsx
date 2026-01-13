"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { toast } from 'sonner';
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu';
import { LogOut, User, CalendarIcon, DoorOpen, Plus } from 'lucide-react';
import RoomList from '@/components/room-list';
import BookingList from '@/components/booking-list';
import CreateRoomDialog from '@/components/create-room-dialog';
import CreateBookingDialog from '@/components/create-booking-dialog';

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'rooms' | 'bookings'>('rooms');
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  const handleLogout = async () => {
    try {
      await logout();
      toast.success('Déconnexion réussie');
      router.push('/login');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Chargement...</p>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const userInitials = `${user.first_name[0]}${user.last_name[0]}`.toUpperCase();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md shadow-lg border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Easy Booking
                </h1>
                <p className="text-xs sm:text-sm text-gray-500 dark:text-gray-400">Gestion de réservations</p>
              </div>
            </div>
            
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-10 w-10 rounded-full hover:ring-2 ring-blue-500 transition-all">
                  <Avatar className="h-10 w-10">
                    <AvatarFallback className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold">
                      {userInitials}
                    </AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium">{user.first_name} {user.last_name}</p>
                    <p className="text-xs text-muted-foreground line-clamp-1">{user.email}</p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="text-red-600 focus:text-red-600">
                  <LogOut className="mr-2 h-4 w-4" />
                  Se déconnecter
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
        <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 mb-6">
          <Button
            variant={activeTab === 'rooms' ? 'default' : 'outline'}
            onClick={() => setActiveTab('rooms')}
            className="flex items-center justify-center gap-2 w-full sm:w-auto transition-all hover:scale-105"
            size="lg"
          >
            <DoorOpen className="h-5 w-5" />
            <span className="font-semibold">Salles</span>
          </Button>
          <Button
            variant={activeTab === 'bookings' ? 'default' : 'outline'}
            onClick={() => setActiveTab('bookings')}
            className="flex items-center justify-center gap-2 w-full sm:w-auto transition-all hover:scale-105"
            size="lg"
          >
            <CalendarIcon className="h-5 w-5" />
            <span className="font-semibold">Mes Réservations</span>
          </Button>
        </div>

        <Card className="shadow-xl border-2 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
          <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 border-b-2">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div className="flex-1">
                <CardTitle className="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  {activeTab === 'rooms' ? 'Liste des salles' : 'Mes réservations'}
                </CardTitle>
                <CardDescription className="text-sm md:text-base mt-1">
                  {activeTab === 'rooms' 
                    ? 'Parcourez et réservez les salles disponibles' 
                    : 'Gérez vos réservations'}
                </CardDescription>
              </div>
              <div className="w-full sm:w-auto">
                {activeTab === 'rooms' ? (
                  <CreateRoomDialog onRoomCreated={() => setRefreshKey(prev => prev + 1)} />
                ) : (
                  <CreateBookingDialog onBookingCreated={() => setRefreshKey(prev => prev + 1)} />
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-6">
            {activeTab === 'rooms' ? (
              <RoomList key={refreshKey} onBookingCreated={() => setRefreshKey(prev => prev + 1)} />
            ) : (
              <BookingList key={refreshKey} />
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
