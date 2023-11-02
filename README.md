<h2>Documentation du Projet</h2>

<h3>Description</h3>
<p>Ce dépôt contient les détails de l'intégration de RandomUser.me avec les bases de données Cassandra et MongoDB, conformément aux exigences du RGPD.</p>

<h3>Objectif</h3>
<p>L'objectif principal de ce projet est de récupérer des données à partir de RandomUser.me et de les stocker de manière sécurisée et conforme aux normes du RGPD dans les bases de données Cassandra et MongoDB.</p>

<h3>Registre des Traitements de Données Personnelles</h3>
<ol>
  <li>
    <b>Types de Données Stockées</b><p>Données personnelles issues de RandomUser.me </p>
    <ul>
      <li>Noms et prénoms</li>
      <li>Adresses e-mail</li>
      <li>Numéros de téléphone</li>
      <li>Dates de naissance</li>
      <li>Adresses (rue, ville, code postal, pays)</li>
      <li>Liens vers les photos de profil (URL)</li>
    </ul>
  </li>
  <li><b>Finalités du Traitement</b>
    <ul>
      <li>Collecte de données : <p>Acquisition de profils utilisateurs via RandomUser.me.</p></li>
      <li>Stockage dans Cassandra et MongoDB : <p>Enregistrement des profils utilisateurs dans les bases de données pour des simulations, tests et démonstrations</p></li>
    </ul>
  </li>
  
  <li><b>Mesures de Sécurité Mises en Place</b>
    <ul>
      <li>Chiffrement des Données : <p>Toutes les données stockées sont chiffrées pour assurer leur sécurité.</p></li>
      <li>Contrôle d'Accès Restreint : <p>Uniquement les individus autorisés ont accès aux données.</p></li>
      <li>Sécurité des Bases de Données : <p>Les bases de données (Cassandra et MongoDB) sont sécurisées avec des paramètres d'accès restreints et des mises à jour de sécurité régulières.</p></li>
    </ul>
  </li>
  <li><b>Durée de Conservation des Données</b>
    <ul>
      <li>Les données collectées sont conservées pour des tests et des démonstrations pendant une durée limitée, puis régulièrement purgées après utilisation.</li>
    </ul>
  </li>
  <li><b>Consentement et Droits des Personnes Concernées</b>
    <ul>
      <li>Les données collectées sont exclusivement utilisées pour les simulations et ne sont en aucun cas partagées ou utilisées à d'autres fins sans le consentement explicite des personnes concernées.</li>
    </ul>
  </li>
  <li><b>Responsabilité</b>
    <ul>
      <li>L'équipe en charge du projet est responsable de la gestion, de la sécurité et de l'utilisation adéquate des données. Toute violation ou problème de sécurité est traité conformément aux exigences du RGPD.</li>
    </ul>
  </li>
</ol>

<!-- ********** -->

<h2>Utilisation d'outils pour l'identification des données personnelles dans le data lake :</h2>
<ol>
  <li><h4>Analyse Automatisée des Données</h4>
    <ul>
      <li><h5>Traitement du Langage Naturel (NLP) : </h5>Utilisation de l'analyse sémantique pour détecter des informations telles que les noms, les adresses, les numéros de téléphone, les adresses e-mail, etc.</li>
      <li><h5>Reconnaissance de Modèles : </h5>Identification de schémas récurrents correspondant à des informations personnelles, comme les formats d'adresses, les numéros de téléphone, les identifiants personnels, etc.</li>
    </ul>
  </li>
  <li><h4>Outils de Classification et de Recherche</h4>
    <ul>
      <li><h5>Algorithmes de Classification : </h5>Utilisation d'algorithmes pour catégoriser et identifier les données stockées, en les associant à des catégories spécifiques telles que "personnelles", "sensibles", "identifiantes", etc.</li>
      <li><h5>Moteurs de Recherche : </h5>Utilisation de moteurs de recherche internes pour balayer le data lake à la recherche de termes spécifiques associés aux données personnelles.</li>
    </ul>
  </li>
  <li><h4>Exploration de Métadonnées</h4>
  <ul>
      <li><h5>Analyse des Métadonnées : </h5>Examen des métadonnées pour identifier les schémas de données, les types de fichiers, les auteurs et les propriétaires des données stockées.</li>
      <li><h5>Catalogage des Données : </h5>Utilisation de solutions de catalogage des données pour marquer, indexer et organiser les données stockées, ce qui facilite l'identification des données personnelles.</li>
    </ul>
  </li>
</ol>

<!--===== =====-->
<h2>Procédures de Tri et de Suppression des Données Personnelles en Conformité avec le RGPD</h2>

<ol>
  <li><h4>Identification des Données Personnelles</h4>
    <ul>
      <li><h5>Analyse des Données : </h5>Utilisation d'outils d'analyse pour repérer les données personnelles stockées dans le data lake, incluant les informations sensibles comme les noms, adresses, numéros de téléphone et adresses e-mail.</li>
    </ul>
  </li>

  <li><h4>Tri des Données</h4>
    <ul>
      <li><h5>Classification des Données : </h5>Catégorisation des données en fonction de leur pertinence et de leur utilité actuelle. Les données nécessaires seront conservées, tandis que les données inutiles ou trop anciennes seront marquées en vue de leur suppression.</li>
      <li><h5>Critères de Tri : </h5>Établissement de critères pour déterminer la pertinence des données, en se basant sur des facteurs tels que la dernière date d'utilisation, la nécessité pour les objectifs en cours, ainsi que le consentement des individus concernés.</li>
    </ul>
  </li>

  <li><h4>Suppression des Données</h4>
    <ul>
      <li><h5>Processus de Suppression : </h5>Élaboration d'une méthode sécurisée pour supprimer de façon permanente les données inutiles ou périmées. Ceci peut impliquer l'utilisation de procédés de destruction de données conformes aux normes du RGPD.</li>
      <li><h5>Documentation : </h5>Tenue d'un registre détaillé des données supprimées, y compris les raisons de la suppression et les détails sur le processus, pour assurer la conformité totale et la transparence en accord avec les exigences du RGPD.</li>
    </ul>
  </li>

  <li><h4>Planification et Surveillance</h4>
    <ul>
      <li><h5>Vérifications Régulières : </h5>Programmation d'audits périodiques pour trier et supprimer les données personnelles inutiles ou obsolètes, dans le but de maintenir une conformité constante avec le RGPD.</li>
      <li><h5>Révision et Ajustement : </h5>Réévaluation des critères de tri et de suppression régulièrement, pour garantir qu'ils respectent les directives du RGPD, avec ajustement si nécessaire.</li>
    </ul>
  </li>

  <li><h4>Mise en Œuvre</h4>
    <ul>
      <li><h5>Formation et Sensibilisation : </h5>Sensibilisation du personnel à la gestion des données concernant ces procédures, ainsi qu'aux implications juridiques et aux bonnes pratiques conformes au RGPD.</li>
      <li><h5>Exécution : </h5>Mise en application rigoureuse de ces procédures, garantissant ainsi leur respect et leur suivi.</li>
    </ul>
  </li>
</ol>






