"""Classe représentant un vecteur en dimension finie."""

class Vecteur:
    
    def __init__(self, coordonnees):
        """Constructeur qui place dans l'attribut coordonnees le tuple 
        contenant les valeurs de <coordonnees>"""
        self.coordonnees = tuple(coordonnees)
    
    def __str__(self):
        """Convertit <self> en une chaîne de caractères pour l'affichage 
        pour un utilisateur humain."""
        return str(self.coordonnees)
    
    def __repr__(self):
        """Représentation en colonne du vecteur."""
        col = ""
        for coord in self.coordonnees:
            col += str(coord) + "\n"
        col = col[:-1]
        return f"[\n{col}\n]"
    
    def dimension(self):
        """Fournit le nombre de coordonnées du vecteur <self>."""
        return len(self.coordonnees)

    def __getitem__(self, key):
        """Retourne la composante d'indice <key> dans le vecteur <self>."""
        return self.coordonnees[key]
        
    def __add__(self, other):
        """Retourne la somme de <self> et <other>."""
        v = []
        for i in range(0, self.dimension()):
            add = self[i] + other[i]
            v.append(add)
        return Vecteur(v)
    
    def multvec(self, other):
        """Retourne le produit coordonnée par coordonnée de <self> et <other>."""
        v =  []
        for i in range(0, self.dimension()):
            v.append(self[i] * other[i])
        return Vecteur(v)
    
    def __mul__(self, coefficient):
        """Retourne <coefficient> fois le vecteur <self>."""
        v = []
        for c in self.coordonnees:
            mult = c * coefficient
            v.append(mult)
        return Vecteur(v) 
    
    def __matmul__(self, other):
        """Retourne le produit scalaire de <self> et de <other>."""
        valeur = 0
        for i in range(0, self.dimension()):
            scalaire = self[i] * other[i]
            valeur += scalaire
        return valeur   
    
    def norme_carre(self):
        """Retourne le carré de la norme de <self>."""
        valeur = 0
        for elt in self.coordonnees:
            carre = elt * elt
            valeur += carre
        return valeur
        
    def norme(self):
        """Retourne la norme de <self>."""
        return self.norme_carre() ** 0.5     
        
    def normaliser(self):
        """Retourne un vecteur ayant même direction et même sens que <self> 
        mais dont la norme vaut 1."""
        v = []
        n = self.norme()
        for c in self.coordonnees:
            v.append(c/n)
        return Vecteur(v)
        

if __name__ == "__main__":
    v1 = Vecteur([1,2])
    v2 = Vecteur([3,5,7])
    v3 = Vecteur([0,3,4])
    print(v1)
    print(v2)
    print(f"Dimension du Vecteur 1:{v1.dimension()}")
    print(f"Dimension du Vecteur 2:{v2.dimension()}")
    print(f"Affichage en colonne du vecteur:\n{repr(v2)}")
    print(f"v2[0] = {v2[0]}")
    print(f"v2[0] = {v2[1]}")
    print(v2 + v3)    
    print(v2.multvec(v3))    
    print(v1 * 3)
    print(v1 @ v2)
    print(v1.norme_carre())
    print(v3.normaliser())