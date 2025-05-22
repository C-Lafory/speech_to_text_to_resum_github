# Backend Go - Audio Transcription Service | Service de Transcription Audio

[English](#english) | [Français](#français)

<a name="english"></a>
# English Version

## 📋 Description
This backend service is designed to handle audio transcription and summary generation. It integrates with a Python service for audio processing and uses MySQL for data persistence.

## 🚀 Technology Stack
- **Go 1.23.0** - Main programming language
- **MySQL 8.0** - Database
- **Docker** - Containerization
- **gRPC** - Python service communication
- **godotenv** - Environment configuration
- **mysql-driver** - Database driver
- **uuid** - Unique identifier generation

## 🛠️ Prerequisites
- Docker and Docker Compose
- Go 1.23.0 or higher
- MySQL 8.0
- Git

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/comeclafory/speech_to_text_to_resum_github.git
cd speech_to_text_to_resum_github
```

### 2. Environment Configuration
Create a `.env` file in the `backend_golang` directory with the following variables:
```env
DB_HOST=mysql
DB_PORT=3306
DB_USER=test
DB_PASSWORD=test
DB_NAME=mydatabase
API_PORT=5048
```

### 3. Start with Docker
```bash
docker-compose -f docker-compose.golang.yml up --build
```

## 📁 Project Structure
```
backend_golang/
├── cmd/            # Application entry point
├── config/         # Configuration files
├── database/       # Database management
├── handlers/       # HTTP handlers
├── middleware/     # Middleware (logging)
├── migrations/     # Database migrations
├── pkg/           # Reusable packages
├── pythonclient/  # Python service gRPC client
└── utils/         # Utilities
```

## 🔐 API Endpoints

### File Management
- `POST /api/audio` - Upload audio file
- `GET /api/files` - List all files
- `GET /api/files/:id` - Get file details
- `DELETE /api/files/:id` - Delete file

## 🔄 Processing Workflow
1. User uploads an audio file
2. Backend stores the file and sends request to Python service
3. Python service performs transcription and summarization
4. Results are stored in database
5. User can access results via API

## 🧪 Testing
```bash
go test ./...
```

## 📊 Monitoring
- Healthcheck endpoint: `GET /health`
- Prometheus metrics: `GET /metrics`

## 🔍 Logging
Structured logs include:
- Log level
- Timestamp
- Request ID
- Message
- Metadata

## 🔒 Security
- Input validation
- CORS protection
- Rate limiting
- Data sanitization

## 🚨 Error Handling
- Standardized HTTP error codes
- Detailed error messages
- Error logging
- Retry mechanism for critical operations

## 📈 Scaling
Service is designed to be scalable:
- Stateless architecture
- Connection pooling
- Optional cache layer
- Load balancing ready

## 🔄 CI/CD
- Automated tests
- Docker builds
- Automated deployment
- Code quality checks

## 📚 Documentation
- API Documentation (Swagger)
- Technical documentation
- Deployment guides
- Troubleshooting guide

## 🤝 Contributing
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License
MIT License - See `LICENSE` file for details

## 👥 Authors
- Comeclafory - Lead Developer

## 🙏 Acknowledgments
- All contributors
- Open source community

---

<a name="français"></a>
# Version Française

## 📋 Description
Ce service backend est conçu pour gérer la transcription audio et la génération de résumés. Il s'intègre avec un service Python pour le traitement audio et utilise MySQL pour la persistance des données.

## 🚀 Technologies Utilisées
- **Go 1.23.0** - Langage principal
- **MySQL 8.0** - Base de données
- **Docker** - Conteneurisation
- **gRPC** - Communication avec le service Python
- **godotenv** - Configuration de l'environnement
- **mysql-driver** - Pilote de base de données
- **uuid** - Génération d'identifiants uniques

## 🛠️ Prérequis
- Docker et Docker Compose
- Go 1.23.0 ou supérieur
- MySQL 8.0
- Git

## 🔧 Installation

### 1. Cloner le Repository
```bash
git clone https://github.com/comeclafory/speech_to_text_to_resum_github.git
cd speech_to_text_to_resum_github
```

### 2. Configuration de l'Environnement
Créez un fichier `.env` dans le dossier `backend_golang` avec les variables suivantes :
```env
DB_HOST=mysql
DB_PORT=3306
DB_USER=test
DB_PASSWORD=test
DB_NAME=mydatabase
API_PORT=5048
```

### 3. Démarrage avec Docker
```bash
docker-compose -f docker-compose.golang.yml up --build
```

## 📁 Structure du Projet
```
backend_golang/
├── cmd/            # Point d'entrée de l'application
├── config/         # Fichiers de configuration
├── database/       # Gestion de la base de données
├── handlers/       # Gestionnaires HTTP
├── middleware/     # Middleware (logging)
├── migrations/     # Migrations de la base de données
├── pkg/           # Packages réutilisables
├── pythonclient/  # Client gRPC pour le service Python
└── utils/         # Utilitaires
```

## 🔐 Points d'Accès API

### Gestion des Fichiers
- `POST /api/audio` - Upload de fichier audio
- `GET /api/files` - Liste des fichiers
- `GET /api/files/:id` - Détails d'un fichier
- `DELETE /api/files/:id` - Suppression d'un fichier

## 🔄 Workflow de Traitement
1. L'utilisateur upload un fichier audio
2. Le backend stocke le fichier et envoie une requête au service Python
3. Le service Python effectue la transcription et le résumé
4. Les résultats sont stockés en base de données
5. L'utilisateur peut accéder aux résultats via l'API

## 🧪 Tests
```bash
go test ./...
```

## 📊 Monitoring
- Endpoint de santé : `GET /health`
- Métriques Prometheus : `GET /metrics`

## 🔍 Journalisation
Les logs structurés incluent :
- Niveau de log
- Horodatage
- ID de requête
- Message
- Métadonnées

## 🔒 Sécurité
- Validation des entrées
- Protection CORS
- Rate limiting
- Sanitization des données

## 🚨 Gestion des Erreurs
- Codes d'erreur HTTP standardisés
- Messages d'erreur détaillés
- Journalisation des erreurs
- Mécanisme de retry pour les opérations critiques

## 📈 Scaling
Le service est conçu pour être scalable :
- Architecture stateless
- Pool de connexions
- Couche de cache optionnelle
- Prêt pour le load balancing

## 🔄 CI/CD
- Tests automatisés
- Builds Docker
- Déploiement automatique
- Vérification de la qualité du code

## 📚 Documentation
- Documentation API (Swagger)
- Documentation technique
- Guides de déploiement
- Guide de dépannage

## 🤝 Contribution
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License
Licence MIT - Voir le fichier `LICENSE` pour plus de détails

## 👥 Auteurs
- Comeclafory - Développeur Principal

## 🙏 Remerciements
- Tous les contributeurs
- La communauté open source