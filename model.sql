-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;

DROP TABLE `Rel_champs_savants`;


DROP TABLE `Liens`;


DROP TABLE `Savants`;


DROP TABLE `Type_lien`;


DROP TABLE `Type_eminence`;


DROP TABLE `Champs`;



-- ************************************** `Type_lien`

CREATE TABLE `Type_lien`
(
 `id_type_lien` tinyint NOT NULL COMMENT 'Identifiant du type de lien entre les savants' ,
 `type_lien`    varchar(45) NOT NULL COMMENT 'Type de lien entre les savants' ,
PRIMARY KEY (`id_type_lien`)
);






-- ************************************** `Type_eminence`

CREATE TABLE `Type_eminence`
(
 `id_type_eminence` tinyint unsigned NOT NULL COMMENT 'Identifiant du type d''éminence' ,
 `type_eminence`    varchar(3) NOT NULL COMMENT 'Type d''éminence du savant pouvant prendre quatre valeurs: AAA, AA, A ou B.' ,
PRIMARY KEY (`id_type_eminence`)
);






-- ************************************** `Champs`

CREATE TABLE `Champs`
(
 `id_champ` tinyint unsigned NOT NULL COMMENT 'Identifiant du champ' ,
 `champ`    varchar(20) NOT NULL COMMENT 'Champ de travail du savant (équivalent à la catégorie DSB pour les savants de type A)' ,
PRIMARY KEY (`id_champ`)
);






-- ************************************** `Savants`

CREATE TABLE `Savants`
(
 `id_savant`                integer NOT NULL COMMENT 'Numéro du savant' ,
 `type_savant`              char(1) NOT NULL COMMENT 'Type de savant : A (grand savant) ou B (petit savant)' ,
 `nom`                      varchar(45) NOT NULL COMMENT 'Nom du savant' ,
 `prenom`                   varchar(45) NOT NULL COMMENT 'Prénom du savant' ,
 `naissance_date`           smallint NOT NULL COMMENT 'Année de naissance' ,
 `naissance_date_certitude` binary(1) NOT NULL COMMENT 'Sommes-nous certains de l’année de naissance ? 0 pour non, 1 pour oui' ,
 `naissance_date_comment`   varchar(45) COMMENT 'En cas d’incertitude sur l’année de naissance, quelle est cette incertitude ?' ,
 `mort_date`                smallint NOT NULL COMMENT 'Année de décès' ,
 `mort_date_certitude`      binary(1) NOT NULL COMMENT 'Sommes-nous certains de l’année de décès ?' ,
 `mort_date_comment`        varchar(45) NOT NULL COMMENT 'En cas d’incertitude sur l’année de décès quelle est cette incertitude ?' ,
 `naissance_lieu`           varchar(45) NOT NULL COMMENT 'Lieu de naissance' ,
 `mort_lieu`                varchar(50) NOT NULL COMMENT 'Lieu de décès' ,
 `pays_principal`           varchar(45) COMMENT 'Pays dans lequel le savant a exercé l’essentiel de ses activités' ,
 `pays_2`                   varchar(45) COMMENT 'Autre pays dans lequel a vécu le savant.' ,
 `pays_3`                   varchar(45) COMMENT 'Autre pays dans lequel a vécu le savant.' ,
 `empire`                   varchar(45) COMMENT 'Empire du lieu de vie et du lieu de travail' ,
 `lieu_1`                   varchar(45) COMMENT 'Lieu de travail (ville)' ,
 `lieu_2`                   varchar(45) COMMENT 'Autre lieu de travail (ville)' ,
 `lieu_3`                   varchar(45) COMMENT 'Autre lieu de travail (ville)' ,
 `lieu_4`                   varchar(45) COMMENT 'Autre lieu de travail (ville)' ,
 `discipl_1`                varchar(45) NOT NULL COMMENT 'Discipline scientifique (second niveau)' ,
 `discipl_2`                varchar(45) COMMENT 'Discipline scientifique (second niveau)' ,
 `discipl_3`                varchar(45) COMMENT 'Discipline scientifique (second niveau)' ,
 `discipl_4`                varchar(45) COMMENT 'Discipline scientifique (second niveau)' ,
 `discipl_5`                varchar(45) COMMENT 'Discipline scientifique (second niveau)' ,
 `a_paris`                  varchar(45) COMMENT 'Académie des sciences de Paris (y a appartenu et à quelles dates)' ,
 `a_londres`                varchar(45) COMMENT 'Académie des sciences de Londres (y a appartenu et à quelles dates)' ,
 `a_berlin`                 varchar(45) COMMENT 'Académie des sciences de Berlin (y a appartenu et à quelles dates)' ,
 `a_petersb`                varchar(45) COMMENT 'Académie des sciences de Saint-Pétersbourg (y a appartenu et à quelles dates)' ,
 `a_stockh`                 varchar(45) COMMENT 'Académie des sciences de Stockholm (y a appartenu et à quelles dates)' ,
 `a_bologne`                varchar(45) COMMENT 'Académie des sciences de Bologne y a appartenu et à quelles dates)' ,
 `acad_7`                   varchar(45) COMMENT 'Autre académie des sciences à laquelle le savant a appartenu' ,
 `acad_8`                   varchar(45) COMMENT 'Autre académie des sciences à laquelle le savant a appartenu' ,
 `acad_9`                   varchar(45) COMMENT 'Autre académie des sciences à laquelle le savant a appartenu' ,
 `pos_acad_1`               varchar(45) COMMENT 'Première position académique' ,
 `pos_acad_2`               varchar(45) COMMENT 'Deuxième position académique' ,
 `prix_1`                   varchar(45) COMMENT 'Prix' ,
 `prix_2`                   varchar(45) COMMENT 'Prix' ,
 `nbre_acad`                tinyint unsigned NOT NULL COMMENT 'Nombre d’affiliations académiques' ,
 `gasc`                     binary(1) NOT NULL COMMENT 'Présent dans le « Historical Catalogue of Scientists and Scientific Books » (1984) de Robert M. Gascoigne ?' ,
 `dsb`                      binary(1) COMMENT 'Présent dans le « Dictionary of Scientific Biography » ?' ,
 `macmill`                  binary(1) COMMENT 'Présent dans le « Macmillan Dictionary of the History of Science » (1981) ?' ,
 `id_type_eminence`         tinyint unsigned NOT NULL COMMENT 'Éminence scientifique (1 = AAA ou A++, 2 = AA ou A+, 3 = A ou A-, 4 = B)' ,
 `remarques`                text COMMENT 'Remarques, commentaires' ,
 `source_1`                 varchar(45) COMMENT 'Source de type DSB (pour les A) ou Gasc. (pour les B)' ,
 `source_2`                 varchar(45) COMMENT 'Source de type Poggendorff (ou Linée ou Bernoulli)' ,
 `source_3`                 varchar(45) COMMENT 'Source de type « World Biographical Information System » (WBIS)' ,
 `source_4`                 varchar(45) COMMENT 'Source de type Wikipedia ou internet' ,
 `source_5`                 varchar(45) COMMENT 'Source de type recueils nationaux, bibliographies nationales ou livre sur le savant' ,
 `equipement`               text COMMENT 'Équipements du savant (laboratoires, observatoires, etc.)' ,
PRIMARY KEY (`id_savant`, `type_savant`),
KEY `fkIdx_175` (`id_type_eminence`),
CONSTRAINT `FK_175` FOREIGN KEY `fkIdx_175` (`id_type_eminence`) REFERENCES `Type_eminence` (`id_type_eminence`)
) COMMENT='Table principale de base';






-- ************************************** `Rel_champs_savants`

CREATE TABLE `Rel_champs_savants`
(
 `type_savant`     char(1) NOT NULL COMMENT 'Type de savant' ,
 `id_savant`       integer NOT NULL COMMENT 'Identifiant du savant' ,
 `id_champ`        tinyint unsigned NOT NULL COMMENT 'Identifiant du champ de travail du savant' ,
 `champ_interpret` binary(1) NOT NULL COMMENT 'Est-ce une interprétation personnelle du champ scientifique (1) ou est-ce que ça vient d’un dictionnaire (0) ?' ,
 `champ_principal` binary(1) NOT NULL COMMENT 'Est-ce le champ principal de ce savant ?' ,
PRIMARY KEY (`type_savant`, `id_savant`, `id_champ`),
KEY `fkIdx_187` (`id_savant`, `type_savant`),
CONSTRAINT `FK_187` FOREIGN KEY `fkIdx_187` (`id_savant`, `type_savant`) REFERENCES `Savants` (`id_savant`, `type_savant`),
KEY `fkIdx_199` (`id_champ`),
CONSTRAINT `FK_199` FOREIGN KEY `fkIdx_199` (`id_champ`) REFERENCES `Champs` (`id_champ`)
);






-- ************************************** `Liens`

CREATE TABLE `Liens`
(
 `id_lien`           integer NOT NULL COMMENT 'Identifiant du lien' ,
 `id_savant`         integer NOT NULL COMMENT 'Numéro id du premier savant' ,
 `type_savant`       char(1) NOT NULL COMMENT 'Type du premier savant (A ou B)' ,
 `id_savant_1`       integer NOT NULL COMMENT 'Numéro id du second savant' ,
 `type_savant_1`     char(1) NOT NULL COMMENT 'Type du second savant (A ou B)' ,
 `id_type_lien`      tinyint NOT NULL COMMENT 'Lien entre le premier savant et le second savant, tel que le second savant est le … du premier savant' ,
 `type_lien_comment` varchar(45) COMMENT 'Information supplémentaire sur le lien' ,
 `lien_intensite`    tinyint NOT NULL COMMENT 'Intensité du lien, allant de 1 à 4' ,
PRIMARY KEY (`id_lien`),
KEY `fkIdx_168` (`id_type_lien`),
CONSTRAINT `FK_168` FOREIGN KEY `fkIdx_168` (`id_type_lien`) REFERENCES `Type_lien` (`id_type_lien`),
KEY `fkIdx_65` (`id_savant`, `type_savant`),
CONSTRAINT `FK_65` FOREIGN KEY `fkIdx_65` (`id_savant`, `type_savant`) REFERENCES `Savants` (`id_savant`, `type_savant`),
KEY `fkIdx_69` (`id_savant_1`, `type_savant_1`),
CONSTRAINT `FK_69` FOREIGN KEY `fkIdx_69` (`id_savant_1`, `type_savant_1`) REFERENCES `Savants` (`id_savant`, `type_savant`)
);





