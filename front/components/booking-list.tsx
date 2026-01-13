"use client";

import { useEffect, useState } from 'react';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import { Calendar, Clock, MapPin, Trash2, CheckCircle, XCircle, CalendarCheck, CalendarClock, User } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

type BookingStatus = 'scheduled' | 'confirmed' | 'cancelled' | 'completed';

interface Booking {
  id: string;
  room_id: string;
  user_id: string;
  start_time: string;
  end_time: string;
  status: BookingStatus;
  created_at: string;
  room?: {
    id: string;
    name: string;
    address: string;
  };
  user?: {
    id: string;
    email: string;
    first_name: string;
    last_name: string;
  };
}

const statusConfig: Record<BookingStatus, { label: string; color: string; bgColor: string; icon: React.ReactNode }> = {
  scheduled: {
    label: 'Prévue',
    color: 'text-blue-600 dark:text-blue-400',
    bgColor: 'bg-blue-50 dark:bg-blue-950/30',
    icon: <CalendarClock className="h-4 w-4" />,
  },
  confirmed: {
    label: 'Confirmée',
    color: 'text-green-600 dark:text-green-400',
    bgColor: 'bg-green-50 dark:bg-green-950/30',
    icon: <CheckCircle className="h-4 w-4" />,
  },
  cancelled: {
    label: 'Annulée',
    color: 'text-red-600 dark:text-red-400',
    bgColor: 'bg-red-50 dark:bg-red-950/30',
    icon: <XCircle className="h-4 w-4" />,
  },
  completed: {
    label: 'Terminée',
    color: 'text-gray-600 dark:text-gray-400',
    bgColor: 'bg-gray-50 dark:bg-gray-950/30',
    icon: <CalendarCheck className="h-4 w-4" />,
  },
};

export default function BookingList() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchBookings = async () => {
    try {
      const response = await api.get('/api/v1/booking/');
      setBookings(response.data.items);
    } catch (error) {
      console.error('Error fetching bookings:', error);
      toast.error('Erreur lors du chargement des réservations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const handleCancel = async (id: string) => {
    if (!confirm('Êtes-vous sûr de vouloir annuler cette réservation ?')) {
      return;
    }

    try {
      await api.patch(`/api/v1/booking/${id}`, { status: 'cancelled' });
      toast.success('Réservation annulée avec succès');
      fetchBookings();
    } catch (error) {
      console.error('Error cancelling booking:', error);
      toast.error('Erreur lors de l\'annulation');
    }
  };

  if (loading) {
    return <p className="text-center py-8">Chargement des réservations...</p>;
  }

  if (bookings.length === 0) {
    return (
      <div className="text-center py-12 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 rounded-lg">
        <Calendar className="h-16 w-16 text-blue-500 mx-auto mb-4" />
        <p className="text-lg font-medium text-muted-foreground">Aucune réservation</p>
        <p className="text-sm text-muted-foreground mt-2">Créez votre première réservation</p>
      </div>
    );
  }

  return (
    <>
      <div className="hidden md:block rounded-lg border-2 border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm">
        <Table>
          <TableHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700">
            <TableRow>
              <TableHead className="font-semibold">Salle</TableHead>
              <TableHead className="font-semibold">Adresse</TableHead>
              <TableHead className="font-semibold">Utilisateur</TableHead>
              <TableHead className="font-semibold">Début</TableHead>
              <TableHead className="font-semibold">Fin</TableHead>
              <TableHead className="font-semibold">Statut</TableHead>
              <TableHead className="text-right font-semibold">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {bookings.map((booking) => {
              const status = statusConfig[booking.status] || statusConfig.scheduled;
              const canCancel = booking.status === 'scheduled' || booking.status === 'confirmed';

              return (
                <TableRow key={booking.id} className={`hover:bg-blue-50/50 dark:hover:bg-gray-800/50 transition-colors ${booking.status === 'cancelled' ? 'opacity-60' : ''}`}>
                  <TableCell className="font-medium">
                    {booking.room?.name || 'Salle inconnue'}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                      <MapPin className="h-3.5 w-3.5 text-blue-500" />
                      {booking.room?.address || '-'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1.5 text-sm font-medium">
                      <User className="h-3.5 w-3.5 text-indigo-500" />
                      {booking.user ? `${booking.user.first_name} ${booking.user.last_name}` : 'N/A'}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1.5 text-sm">
                      <Calendar className="h-3.5 w-3.5 text-green-600" />
                      {format(new Date(booking.start_time), 'PPp', { locale: fr })}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1.5 text-sm">
                      <Clock className="h-3.5 w-3.5 text-orange-600" />
                      {format(new Date(booking.end_time), 'PPp', { locale: fr })}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${status.bgColor} ${status.color}`}>
                      {status.icon}
                      {status.label}
                    </div>
                  </TableCell>
                  <TableCell className="text-right">
                    {canCancel && (
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleCancel(booking.id)}
                        className="hover:scale-105 transition-transform"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      <div className="md:hidden space-y-4">
        {bookings.map((booking) => {
          const status = statusConfig[booking.status] || statusConfig.scheduled;
          const canCancel = booking.status === 'scheduled' || booking.status === 'confirmed';

          return (
            <Card
              key={booking.id}
              className={`hover:shadow-lg transition-all duration-300 border-2 hover:border-primary/50 bg-gradient-to-br from-white to-gray-50/50 dark:from-gray-900 dark:to-gray-800/50 ${booking.status === 'cancelled' ? 'opacity-60' : ''}`}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-2">
                  <CardTitle className="text-lg font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                    {booking.room?.name || 'Salle inconnue'}
                  </CardTitle>
                  <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${status.bgColor} ${status.color}`}>
                    {status.icon}
                    {status.label}
                  </div>
                </div>
                <CardDescription className="flex items-center gap-1.5">
                  <MapPin className="h-3.5 w-3.5 text-blue-500 flex-shrink-0" />
                  <span className="line-clamp-1">{booking.room?.address || '-'}</span>
                  {booking.user && (
                    <div className="flex items-center gap-1 ml-2 pl-2 border-l border-gray-300 dark:border-gray-600">
                      <User className="h-3.5 w-3.5 text-indigo-500 flex-shrink-0" />
                      <span className="text-sm font-medium">{booking.user.first_name} {booking.user.last_name}</span>
                    </div>
                  )}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-center gap-2 text-sm bg-green-50 dark:bg-green-950/30 p-2 rounded-lg">
                  <Calendar className="h-4 w-4 text-green-600 dark:text-green-400 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-gray-700 dark:text-gray-300">Début</p>
                    <p className="text-xs text-muted-foreground">
                      {format(new Date(booking.start_time), 'PPp', { locale: fr })}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm bg-orange-50 dark:bg-orange-950/30 p-2 rounded-lg">
                  <Clock className="h-4 w-4 text-orange-600 dark:text-orange-400 flex-shrink-0" />
                  <div>
                    <p className="font-medium text-gray-700 dark:text-gray-300">Fin</p>
                    <p className="text-xs text-muted-foreground">
                      {format(new Date(booking.end_time), 'PPp', { locale: fr })}
                    </p>
                  </div>
                </div>
              </CardContent>
              {canCancel && (
                <CardFooter>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleCancel(booking.id)}
                    className="w-full hover:scale-105 transition-transform"
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Annuler la réservation
                  </Button>
                </CardFooter>
              )}
            </Card>
          );
        })}
      </div>
    </>
  );
}
