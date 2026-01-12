"use client";

import { useEffect, useState } from 'react';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import { Calendar, Clock, MapPin, Trash2 } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

interface Booking {
  id: string;
  room_id: string;
  user_id: string;
  start_time: string;
  end_time: string;
  created_at: string;
  room?: {
    id: string;
    name: string;
    address: string;
  };
}

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

  const handleDelete = async (id: string) => {
    if (!confirm('Êtes-vous sûr de vouloir annuler cette réservation ?')) {
      return;
    }

    try {
      await api.delete(`/api/v1/booking/${id}`);
      toast.success('Réservation annulée avec succès');
      fetchBookings();
    } catch (error) {
      console.error('Error deleting booking:', error);
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
              <TableHead className="font-semibold">Début</TableHead>
              <TableHead className="font-semibold">Fin</TableHead>
              <TableHead className="text-right font-semibold">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {bookings.map((booking) => (
              <TableRow key={booking.id} className="hover:bg-blue-50/50 dark:hover:bg-gray-800/50 transition-colors">
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
                <TableCell className="text-right">
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleDelete(booking.id)}
                    className="hover:scale-105 transition-transform"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="md:hidden space-y-4">
        {bookings.map((booking) => (
          <Card 
            key={booking.id} 
            className="hover:shadow-lg transition-all duration-300 border-2 hover:border-primary/50 bg-gradient-to-br from-white to-gray-50/50 dark:from-gray-900 dark:to-gray-800/50"
          >
            <CardHeader className="pb-3">
              <CardTitle className="text-lg font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                {booking.room?.name || 'Salle inconnue'}
              </CardTitle>
              <CardDescription className="flex items-center gap-1.5">
                <MapPin className="h-3.5 w-3.5 text-blue-500 flex-shrink-0" />
                <span className="line-clamp-1">{booking.room?.address || '-'}</span>
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
            <CardFooter>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(booking.id)}
                className="w-full hover:scale-105 transition-transform"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Annuler la réservation
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </>
  );
}
