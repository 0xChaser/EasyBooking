"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import { Pencil } from 'lucide-react';
import api from '@/lib/axios';

interface EditRoomDialogProps {
  roomId: string;
  roomName: string;
  roomAddress: string;
  roomCapacity: number;
  roomDescription: string | null;
  onRoomUpdated?: () => void;
}

export default function EditRoomDialog({
  roomId,
  roomName,
  roomAddress,
  roomCapacity,
  roomDescription,
  onRoomUpdated,
}: EditRoomDialogProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: roomName,
    address: roomAddress,
    capacity: roomCapacity.toString(),
    description: roomDescription || '',
  });

  useEffect(() => {
    if (open) {
      setFormData({
        name: roomName,
        address: roomAddress,
        capacity: roomCapacity.toString(),
        description: roomDescription || '',
      });
    }
  }, [open, roomName, roomAddress, roomCapacity, roomDescription]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.patch(`/api/v1/room/${roomId}`, {
        name: formData.name,
        address: formData.address,
        capacity: parseInt(formData.capacity),
        description: formData.description || null,
      });

      toast.success('Salle modifiée avec succès');
      setOpen(false);
      onRoomUpdated?.();
    } catch (error: any) {
      console.error('Error updating room:', error);
      toast.error(error.response?.data?.detail || 'Erreur lors de la modification');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Pencil className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Modifier la salle</DialogTitle>
          <DialogDescription>
            Modifiez les informations de la salle
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-name">Nom de la salle</Label>
              <Input
                id="edit-name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-address">Adresse</Label>
              <Input
                id="edit-address"
                value={formData.address}
                onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-capacity">Capacité</Label>
              <Input
                id="edit-capacity"
                type="number"
                min="1"
                value={formData.capacity}
                onChange={(e) => setFormData({ ...formData, capacity: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-description">Description (optionnel)</Label>
              <Input
                id="edit-description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Annuler
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Modification...' : 'Modifier'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
