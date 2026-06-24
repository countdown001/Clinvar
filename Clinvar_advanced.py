import gzip
import os
import urllib.request
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# URL du fichier ClinVar sur le serveur FTP de NCBI
url = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz'

def banner() -> None:
    """
    Affiche la bannière ASCII du programme au démarrage.
    """
    font = r"""
   _____ _      _____ _   ___      __     _____ 
  / ____| |    |_   _| \ | \ \    / /\   |  __ \ 
 | |    | |      | | |  \| |\ \  / /  \  | |__) |
 | |    | |      | | | . ` | \ \/ / /\ \ |  _  / 
 | |____| |____ _| |_| |\  |  \  / ____ \| | \ \ 
  \_____|______|_____|_| \_|   \/_/    \_\_|  \_\
    """
    print(font)

def search_protein(Proteine_ID, fichier):
    """
    Recherche les informations cliniques d'une protéine dans la base de données ClinVar.

    Paramètres:
        Proteine_ID (str): L'identifiant unique de la protéine à rechercher.
        fichier (str): Le nom du fichier .gz à lire.

    Retourne:
        - CLN_SIG    (str | None): Signification clinique de la variante.
        - CLN_DN     (str | None): Nom de la maladie associée.
        - CLN_DISDB  (str | None): Base de données de la maladie associée.
        - CLN_REVSTAT(str | None): Statut de révision de la classification.
        - CLN_HGVS   (str | None): Nom HGVS de la variante.
        - CLN_VC     (str | None): Type de variation.
        - CLN_VCSO   (str | None): Effet sur la séquence (code SO).
        - MC         (str | None): Conséquence moléculaire.
        - GENE_INFO  (str | None): Informations sur le gène associé.
        - ORIGIN     (str | None): Origine de la variante.
        Retourne (None, None, None, None, None, None, None, None, None, None) si aucune entrée n'est trouvée.
    """
    Info = []
    # Ouverture du fichier compressé en mode lecture texte
    clinvar = gzip.open(fichier, "rt", encoding="utf-8")

    for line in clinvar:
        Colonne = line.strip().split("\t")
        # Ignorer les lignes de commentaires commençant par '#'
        if Colonne[0].startswith("#"):
            continue
        # Si l'ID correspond à la colonne 2, on sauvegarde la colonne 7
        if str(Proteine_ID) == Colonne[2]:
            Info.append(Colonne[7])
            break

    # Initialisation des variables à None au cas où elles ne seraient pas trouvées
    CLN_SIG = CLN_DN = CLN_DISDB = CLN_REVSTAT = MC = ORIGIN = CLN_HGVS = CLN_VC = CLN_VCSO = GENE_INFO = None

    # Si aucune correspondance trouvée, on retourne les valeurs None
    if len(Info) == 0:
        clinvar.close()
        return CLN_SIG, CLN_DN, CLN_DISDB, CLN_REVSTAT, CLN_HGVS, CLN_VC, CLN_VCSO, MC, GENE_INFO, ORIGIN

    # Découpage de la colonne 7 en champs séparés par ';'
    Info_Colonne = Info[0].strip().split(";")

    # Extraction des champs cliniques depuis les informations de la variante
    for index in Info_Colonne:
        if index.startswith("CLNSIG="):
            CLN_SIG = index.split("=")[1]
        elif index.startswith("CLNDN="):
            CLN_DN = index.split("=")[1]
        elif index.startswith("CLNDISDB="):
            CLN_DISDB = index.split("=")[1]
        elif index.startswith("CLNREVSTAT="):
            CLN_REVSTAT = index.split("=")[1]
        elif index.startswith("CLNHGVS="):
            CLN_HGVS = index.split("=")[1]
        elif index.startswith("CLNVC="):
            CLN_VC = index.split("=")[1]
        elif index.startswith("CLNVCSO="):
            CLN_VCSO = index.split("=")[1]
        elif index.startswith("MC="):
            MC = index.split("=")[1]
        elif index.startswith("GENEINFO="):
            GENE_INFO = index.split("=")[1]
        elif index.startswith("ORIGIN="):
            ORIGIN = index.split("=")[1]

    clinvar.close()
    return CLN_SIG, CLN_DN, CLN_DISDB, CLN_REVSTAT, CLN_HGVS, CLN_VC, CLN_VCSO, MC, GENE_INFO, ORIGIN


# Point d'entrée du programme
print("===================================================")
banner()
print("===================================================")

# Recherche du premier fichier .gz dans le répertoire courant
fichiers = os.listdir(".")
for index in fichiers:
    if index.endswith(".gz"):
        print("Fichier ClinVar trouvé localement.")
        update = str(input("Voulez-vous le mettre à jour ? (oui/non): "))
        while update.lower() not in ["oui", "non", "o", "n", "yes", "no", "y"]:
            print("Veuillez entrer 'oui' ou 'non'.")
            update = str(input("Voulez-vous le mettre à jour ? (oui/non): "))
        if update.lower() in ["oui", "o", "yes", "y"]:
            # Téléchargement de la version la plus récente depuis le serveur FTP de NCBI
            print("Téléchargement du fichier ClinVar en cours...")
            urllib.request.urlretrieve(url, "clinvar.vcf.gz")
            print("Téléchargement terminé!")
            if index != "clinvar.vcf.gz":
                os.remove(index)
            fichier = "clinvar.vcf.gz"
        else:
            # Utilisation du fichier local existant
            fichier = index
        break
else:
    # Aucun fichier .gz trouvé, proposition de téléchargement automatique
    print("Aucun fichier .gz trouvé. Veuillez télécharger le fichier ClinVar pour continuer.")
    download = str(input("Voulez-vous le télécharger maintenant ? (oui/non): "))
    while download.lower() not in ["oui", "non", "o", "n", "yes", "no", "y"]:
        print("Veuillez entrer 'oui' ou 'non'.")
        download = str(input("Voulez-vous le télécharger maintenant ? (oui/non): "))
    if download.lower() in ["oui", "o", "yes", "y"]:
        # Téléchargement depuis le serveur FTP de NCBI
        print("Téléchargement du fichier ClinVar en cours...")
        urllib.request.urlretrieve(url, "clinvar.vcf.gz")
        print("Téléchargement terminé!")
        fichier = "clinvar.vcf.gz"
    else:
        # L'utilisateur refuse le téléchargement, on quitte le programme
        print("Merci d'avoir utilisé le programme. Au revoir!")
        exit()

while True:
    # Étape 1 : Saisie et validation de l'identifiant protéique
    Proteine_ID = input("Entrez l'ID de la protéine: ").strip()
    if not (Proteine_ID.isdigit() and len(Proteine_ID) == 7):
        print("Veuillez entrer un nombre entier de 7 chiffres pour l'ID de la protéine.")
        continue

    # Étape 2 : Recherche dans la base de données
    Signification_clinique, Maladie, Base_maladie, Statut_revision, HGVS, Type_variation, Effet_sequence, Consequence_moleculaire, Information_gene, Origine = search_protein(Proteine_ID, fichier)
    reponse = [Signification_clinique, HGVS, Type_variation, Effet_sequence, Information_gene]

    # Étape 3 : Affichage des résultats
    if all(value is None for value in reponse):
        print("Aucune information trouvée pour l'ID de la protéine :", Proteine_ID)
    else:
        print("===================================================")
        print("Signification clinique       :", Signification_clinique)
        print("Maladie associée             :", Maladie)
        print("Base de données maladie      :", Base_maladie)
        print("Statut de révision           :", Statut_revision)
        print("Nom HGVS                     :", HGVS)
        print("Type de variation            :", Type_variation)
        print("Effet sur la séquence        :", Effet_sequence)
        print("Conséquence moléculaire      :", Consequence_moleculaire)
        print("Gène associé                 :", Information_gene)
        print("Origine                      :", Origine)
        print("===================================================")

    # Étape 4 : Continuer ou quitter
    Con = input("Voulez-vous faire une autre recherche ? (oui/non): ").strip()
    while Con.lower() not in ["oui", "non", "o", "n", "yes", "no", "y"]:
        print("Veuillez entrer 'oui' ou 'non'.")
        Con = input("Voulez-vous faire une autre recherche ? (oui/non): ").strip()

    if Con.lower() in ["non", "n", "no"]:
        print("Merci d'avoir utilisé le programme. Au revoir!")
        break
                                                                                                #Yamaç Seyfeli-09/05/2026
