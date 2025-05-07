Go utilise des pilotes pour interagir avec des bases de données. Pour MySQL, vous pouvez utiliser le package github.com/go-sql-driver/mysql.

Installez le pilote MySQL :

go get -u github.com/go-sql-driver/mysql



------------------------------------------------------------------

Étape 1 : Installer golang-migrate
Installez l'outil de migration migrate en ligne de commande :

go install -tags 'mysql' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

Assurez-vous que le dossier $GOPATH/bin est dans votre PATH pour pouvoir utiliser la commande migrate.

Étape 2 : Créer une version de migration
Utilisez la commande suivante pour créer une nouvelle version de migration :
migrate create -ext sql -dir migrations -seq create_users_table

-ext sql : Spécifie que les fichiers de migration seront au format SQL.
-dir migrations : Indique le répertoire où les fichiers de migration seront créés (par exemple, migrations).
-seq : Génère un numéro séquentiel pour la migration.
create_users_table : Nom descriptif de la migration.
Cette commande crée deux fichiers dans le répertoire migrations :

000001_create_users_table.up.sql : Contient les instructions pour appliquer la migration.
000001_create_users_table.down.sql : Contient les instructions pour annuler la migration.

Étape 3 : Écrire les instructions SQL dans les fichiers de migration
Dans 000001_create_users_table.up.sql :
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);
Dans 000001_create_users_table.down.sql :
DROP TABLE users;

Étape 4 : Appliquer la migration
Pour appliquer la migration à votre base de données MySQL, utilisez la commande suivante :
migrate -database "mysql://username:password@tcp(localhost:3306)/mydatabase" -path migrations up

-database : Spécifie la chaîne de connexion à votre base de données MySQL.
Remplacez username, password, localhost, 3306, et mydatabase par vos informations de connexion.
-path : Indique le chemin vers le répertoire contenant les fichiers de migration.
up : Applique toutes les migrations disponibles

Étape 5 : Annuler une migration (si nécessaire)
Pour annuler la dernière migration appliquée, utilisez la commande suivante :
migrate -database "mysql://username:password@tcp(localhost:3306)/mydatabase" -path migrations down

Étape 6 : Vérifier l'état des migrations
Pour vérifier quelles migrations ont été appliquées, utilisez :
migrate -database "mysql://username:password@tcp(localhost:3306)/mydatabase" -path migrations version

-------------------------------------------------------

Installer MySQL

Si ce n’est pas déjà fait, installe MySQL sur ton serveur ou en local :

sudo apt update
sudo apt install mysql-server

Démarre MySQL :

sudo systemctl start mysql
sudo systemctl enable mysql




Connectez-vous en tant qu'utilisateur système root : sudo mysql


Une fois connecté, vérifiez le plugin d'authentification pour l'utilisateur root : SELECT user, host, plugin FROM mysql.user;


Vous verrez une sortie similaire à ceci :
+------+-----------+-------------+
| user | host      | plugin      |
+------+-----------+-------------+
| root | localhost | auth_socket |
+------+-----------+-------------+
Si le plugin est auth_socket, cela signifie que MySQL utilise l'authentification par socket au lieu d'un mot de passe.

Changez le plugin d'authentification pour root en mysql_native_password :
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;

Quittez MySQL : EXIT;

Vérifiez les permissions de l'utilisateur : SHOW GRANTS FOR 'username'@'localhost';

Si l'utilisateur n'a pas les permissions nécessaires, accordez-les : GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;

Remplacez username et your_password par les informations de votre utilisateur.

Étape 4 : Redémarrez le service MySQL (si nécessaire)
Si vous avez modifié la configuration ou les permissions, redémarrez le service MySQL pour appliquer les changement : sudo systemctl restart mysql

mysql -u root -p -> mot de passe pour se connecter à la mysql : your_password


mysql -u test -p mydatabase -> pour se connecter à l'utilisateur de la database -> le mdp est test

ces commmandes que j'ai utilisé pour créer mon utilisateur: 

CREATE DATABASE mydatabase;
CREATE USER 'test'@'localhost' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'test'@'localhost';
FLUSH PRIVILEGES;




Tester si la base de données fonctionne
Vérifier si la table users existe

Connecte-toi à MySQL :

mysql -u username -p mydatabase

Puis exécute :

SHOW TABLES;

Tu devrais voir users dans la liste.

Insérer un utilisateur manuellement

INSERT INTO users (username, password, email) VALUES ('testuser', 'hashedpassword', 'test@example.com');
SELECT * FROM users;

Si les données sont insérées et affichées, c’est que ta DB est bien configurée.

je fais ma base de donné en local pour la phase dev mais pour la phase prod je vais l'initialiser sur mon server ovh

--------------------------------------------------------------------------------

Creer ma base de donée mysql : sudo apt update
                                sudo apt install mysql-server

Connectez-vous à MySQL en tant qu'utilisateur root :  mysql -u root -p
mdp : your_password




