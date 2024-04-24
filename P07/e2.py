GENES = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6_269P": "ENSG00000212379",
    "MIR633": "ENSG00000207552",
    "TTTY4C": "ENSG00000228296",
    "RBMY2YP": "ENSG00000227633",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
} #me creo un diccionario con clave: nombre de gener; valor: traduccion para la gente de ensembel del gen (el identificador).

print()
print("Dictionary of Genes!")
print(f"There are {len(GENES)} genes in the dictionary:")
print()

for gene, id in GENES.items(): #items devuelve todas las parejas clave-valor. NO es imprescindible poner items.
    print(f"{gene}: --> {id}")
