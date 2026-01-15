# Plan de Test - EasyBooking
---

## 1. Introduction
Ce document décrit la stratégie de tests pour l'application EasyBooking. L'objectif est de garantir la stabilité de l'API Backend (FastAPI) et l'utilisabilité de l'interface Frontend (Next.js).

## 2. Portée des Tests (Scope)

### 2.1 Backend (Priorité Haute)
- **Tests Unitaires** : Vérification isolée des fonctions utilitaires et services.
- **Tests d'Intégration** : Vérification des endpoints API (Routes) avec base de données de test.
- **Couverture de Code** : Objectif > 90%.
- **Tests de Sécurité** : Vérification de la configuration de production.

## 3. Environnements de Test
- **Local** : Docker pour la BDD.
- **CI/CD** : GitHub Actions (Exécution automatique à chaque Push/PR sur la branche main).

## 4. Outils
- **Backend** : `pytest`, `pytest-cov`, `httpx` (client async), `pytest-benchmark`, `bandit`
- **CI** : GitHub Actions (Workflow existant `.github/workflows/backend-ci.yml`).

## 5. Stratégie d'Exécution
- **Automatique** : Les tests unitaires/intégration Backend sont lancés par la CI.

## 6. Critères d'Acceptation
- 100% des tests automatisés passent.
- Pas de régressions critiques sur les parcours manuels.
