# Market Data Collector - Version Serveur

Collecteur automatique de données de marché pour déploiement sur Render.com.

## 🚀 Fonctionnalités

- Collecte automatique des données de marché (indices, actions, crypto, matières premières, etc.)
- Exécution planifiée (3 fois par jour)
- Envoi automatique par email des rapports
- Stockage des données historiques
- Volatilité historique et implicite
- Options Greeks (Delta pour actions/ETF)

## 📋 Configuration

### 1. Variables d'environnement requises

```bash
EMAIL_PASSWORD=votre_mot_de_passe_gmail