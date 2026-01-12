# Easy Booking - Frontend

Application de gestion de réservations de salles avec authentification JWT.

## Fonctionnalités

- ✅ Authentification (Login/Register/Logout)
- ✅ Gestion des salles (Liste, Création, Suppression)
- ✅ Gestion des réservations (Création, Liste, Annulation)
- ✅ Interface moderne avec shadcn/ui
- ✅ Responsive design

## Prérequis

- Node.js 18+
- Backend Easy Booking en cours d'exécution sur http://localhost:8000

## Installation

```bash
cd front
npm install
```

## Configuration

Créez un fichier `.env.local` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Démarrage

```bash
npm run dev
```

L'application sera disponible sur http://localhost:3000

## Structure

```
app/
├── login/page.tsx          # Page de connexion
├── register/page.tsx       # Page d'inscription
├── dashboard/page.tsx      # Dashboard principal
└── layout.tsx              # Layout avec AuthProvider

components/
├── room-list.tsx           # Liste des salles
├── booking-list.tsx        # Liste des réservations
├── create-room-dialog.tsx  # Dialog de création de salle
└── create-booking-dialog.tsx # Dialog de création de réservation

lib/
├── auth-context.tsx        # Context d'authentification
└── axios.ts                # Configuration axios avec intercepteurs
```

## Utilisation

1. **Inscription** : Créez un compte sur `/register`
2. **Connexion** : Connectez-vous sur `/login`
3. **Dashboard** : 
   - Onglet "Salles" : Visualisez et créez des salles
   - Onglet "Mes Réservations" : Gérez vos réservations
4. **Réservation** : Cliquez sur "Réserver" sur une salle pour créer une réservation

## Technologies

- Next.js 16
- React 19
- shadcn/ui (Radix UI)
- TailwindCSS
- Axios
- date-fns
- Zod
- React Hook Form
