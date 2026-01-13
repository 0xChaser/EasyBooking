"use client";

import { useEffect, useState } from 'react';
import api from '@/lib/axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { toast } from 'sonner';
import { MapPin, Users, Trash2, CheckCircle, XCircle, Wrench } from 'lucide-react';
import CreateBookingDialog from './create-booking-dialog';
import EditRoomDialog from './edit-room-dialog';

type RoomStatus = 'available' | 'unavailable' | 'maintenance';

interface Room {
  id: string;
  name: string;
  address: string;
  capacity: number;
  description: string | null;
  status: RoomStatus;
}

interface RoomListProps {
  onBookingCreated?: () => void;
}

const statusConfig: Record<RoomStatus, { label: string; color: string; bgColor: string; icon: React.ReactNode }> = {
  available: {
    label: 'Disponible',
    color: 'text-green-600 dark:text-green-400',
    bgColor: 'bg-green-50 dark:bg-green-950/30',
    icon: <CheckCircle className="h-4 w-4" />,
  },
  unavailable: {
    label: 'Indisponible',
    color: 'text-red-600 dark:text-red-400',
    bgColor: 'bg-red-50 dark:bg-red-950/30',
    icon: <XCircle className="h-4 w-4" />,
  },
  maintenance: {
    label: 'En maintenance',
    color: 'text-orange-600 dark:text-orange-400',
    bgColor: 'bg-orange-50 dark:bg-orange-950/30',
    icon: <Wrench className="h-4 w-4" />,
  },
};

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
      {rooms.map((room) => {
        const status = statusConfig[room.status] || statusConfig.available;
        const isAvailable = room.status === 'available';
        
        return (
          <Card 
            key={room.id} 
            className={`group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/50 bg-gradient-to-br from-white to-gray-50/50 dark:from-gray-900 dark:to-gray-800/50 ${!isAvailable ? 'opacity-75' : ''}`}
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between gap-2">
                <CardTitle className="text-lg md:text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  {room.name}
                </CardTitle>
                <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${status.bgColor} ${status.color}`}>
                  {status.icon}
                  <span className="hidden sm:inline">{status.label}</span>
                </div>
              </div>
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
              {isAvailable ? (
                <CreateBookingDialog 
                  roomId={room.id} 
                  roomName={room.name}
                  onBookingCreated={onBookingCreated}
                />
              ) : (
                <Button size="sm" className="w-full" disabled>
                  <XCircle className="h-4 w-4 mr-2" />
                  {status.label}
                </Button>
              )}
              <div className="flex gap-2 ml-auto">
                <EditRoomDialog
                  roomId={room.id}
                  roomName={room.name}
                  roomAddress={room.address}
                  roomCapacity={room.capacity}
                  roomDescription={room.description}
                  roomStatus={room.status}
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
        );
      })}
    </div>
  );
}
