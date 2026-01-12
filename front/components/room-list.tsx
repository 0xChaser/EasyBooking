"use client";

import { useEffect, useState } from 'react';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { MapPin, Users, Trash2, Calendar } from 'lucide-react';
import CreateBookingDialog from './create-booking-dialog';
import EditRoomDialog from './edit-room-dialog';

interface Room {
  id: string;
  name: string;
  address: string;
  capacity: number;
  description: string | null;
}

interface RoomListProps {
  onBookingCreated?: () => void;
}

export default function RoomList({ onBookingCreated }: RoomListProps) {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchRooms = async () => {
    try {
      const response = await api.get('/api/v1/room/');
      setRooms(response.data.items);
    } catch (error) {
      console.error('Error fetching rooms:', error);
      toast.error('Erreur lors du chargement des salles');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette salle ?')) {
      return;
    }

    try {
      await api.delete(`/api/v1/room/${id}`);
      toast.success('Salle supprimée avec succès');
      fetchRooms();
    } catch (error) {
      console.error('Error deleting room:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  if (loading) {
    return <p className="text-center py-8">Chargement des salles...</p>;
  }

  if (rooms.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Aucune salle disponible</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
      {rooms.map((room) => (
        <Card 
          key={room.id} 
          className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/50 bg-gradient-to-br from-white to-gray-50/50 dark:from-gray-900 dark:to-gray-800/50"
        >
          <CardHeader className="pb-3">
            <CardTitle className="text-lg md:text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              {room.name}
            </CardTitle>
            <CardDescription className="flex items-center gap-1.5 text-xs md:text-sm">
              <MapPin className="h-3.5 w-3.5 flex-shrink-0 text-blue-500" />
              <span className="line-clamp-1">{room.address}</span>
            </CardDescription>
          </CardHeader>
          <CardContent className="pb-3">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-sm bg-blue-50 dark:bg-blue-950/30 p-2 rounded-lg">
                <Users className="h-4 w-4 text-blue-600 dark:text-blue-400 flex-shrink-0" />
                <span className="font-medium text-gray-700 dark:text-gray-300">
                  {room.capacity} personnes
                </span>
              </div>
              {room.description && (
                <p className="text-sm text-muted-foreground line-clamp-2 italic">
                  {room.description}
                </p>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex flex-wrap gap-2 pt-3">
            <CreateBookingDialog 
              roomId={room.id} 
              roomName={room.name}
              onBookingCreated={onBookingCreated}
            />
            <div className="flex gap-2 ml-auto">
              <EditRoomDialog
                roomId={room.id}
                roomName={room.name}
                roomAddress={room.address}
                roomCapacity={room.capacity}
                roomDescription={room.description}
                onRoomUpdated={fetchRooms}
              />
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleDelete(room.id)}
                className="hover:scale-105 transition-transform"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
}
