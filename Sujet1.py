import gzip
def search_protein(Proteine_ID):
    Proteine_ID=Proteine_ID.strip()
    Info = []
    clinvar = gzip.open("clinvarpapu.gz", "rt", encoding="utf-8")
    lines = clinvar.readlines()
    for line in lines:
        Colonne = line.strip().split("\t")
        if Colonne[0].startswith("#"):
            continue
        if str(Proteine_ID) == Colonne[2]:
            Info.append(Colonne[7])
    return Info

print("====================================")
print("Debut du programme")
print("====================================")
while True:
    Proteine_ID = input("Entrez l'ID de la protéine: ")
    Proteine_ID=Proteine_ID.strip()
    if Proteine_ID.isdigit():
        break
    print("Veuillez entrer un nombre entier pour l'ID de la protéine.")
        
print(search_protein(Proteine_ID))