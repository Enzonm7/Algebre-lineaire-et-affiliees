"""Classe représentant une matrice à coefficients réels."""

from vecteur import Vecteur

class Matrice:
    
    def __init__(self, data):
        """Constructeur qui place dans l'attribut data une copie de <data>.
        <data> doit être une liste de listes non vide, toutes de même longueur."""
        self.data = data
        self.verifier_validite()
        copie = []
        for ligne in data:
            copie.append(list(ligne)) 
        self.data = copie
            
    def verifier_validite(self):
        """Vérifie la validité des coordonnées de la matrice."""
        if len(self.data) == 0:
            raise ValueError("Matrice vide non autorisée !")
        for i in range(len(self.data)):
            if len(self.data[i]) == 0:
                raise ValueError("Matrice vide non autorisée !")
            elif len(self.data[i]) != len(self.data[0]):
                raise ValueError("Les lignes sont de longueurs différentes!")
    
    def __str__(self):
        """Convertit <self> en une chaîne de caractères pour l'affichage
        pour un utilisateur humain."""
        m = ""
        for i in range(len(self.data)):
            if i == 0:
                m += str(self.data[i]) 
            else:
                m += "\n" + str(self.data[i])  
        return m
            
    def __repr__(self):
        """Représentation formelle de <self> permettant de recréer l'objet."""
        return "Matrice(" + str(self.data) + ")"
    
    def nb_lignes(self):
        """Fournit le nombre de lignes de la matrice <self>."""
        return len(self.data)
    
    def nb_colonnes(self):
        """Fournit le nombre de colonnes de la matrice <self>."""
        return len(self.data[0])
    
    def __add__(self, other):
        """Retourne la somme de <self> et <other>."""
        res = []
        if self.nb_lignes() != other.nb_lignes() or self.nb_colonnes() != other.nb_colonnes():
            raise ValueError("Matrices de dimensions différentes!")
        for i in range(self.nb_lignes()):
            ligne = []
            for j in range(self.nb_colonnes()):
                ligne.append(self.data[i][j] + other.data[i][j])
            res.append(ligne)
        return Matrice(res)    
    
    def __sub__(self, other):
        """Retourne la différence de <self> et <other>."""
        res = []
        if self.nb_lignes() != other.nb_lignes() or self.nb_colonnes() != other.nb_colonnes():
            raise ValueError("Matrices de dimensions différentes!")
        for i in range(self.nb_lignes()):
            ligne = []
            for j in range(self.nb_colonnes()):
                ligne.append(self.data[i][j] - other.data[i][j])
            res.append(ligne)
        return Matrice(res)   
    
    def __mul__(self, coefficient):
        """Retourne <coefficient> fois la matrice <self>."""
        res = []
        for i in range(self.nb_lignes()):
            ligne = []
            for j in range(self.nb_colonnes()):
                ligne.append(self.data[i][j] * coefficient)
            res.append(ligne)
        return Matrice(res)       
    
    def __matmul__(self, other):
        """Retourne le produit matriciel de <self> et <other>."""
        # Cas 1 : other est un Vecteur
        if isinstance(other, Vecteur):
            if self.nb_colonnes() != len(other):
                raise ValueError("...")
            res = []
            for i in range(self.nb_lignes()):
                somme = 0
                for k in range(self.nb_colonnes()):
                    somme += self.data[i][k] * other[k]
                res.append(somme)
            return Vecteur(res)
        # Cas 2 : other est une Matrice
        else:
            res = []
            if self.nb_colonnes() != other.nb_lignes():
                raise ValueError("Le nombre de colonnes de self doit être égal au nombre de ligne de other")
            for i in range(self.nb_lignes()):
                ligne = []
                for j in range(other.nb_colonnes()):
                    somme = 0
                    for k in range(0, self.nb_colonnes()):
                        somme += self.data[i][k] * other.data[k][j]
                    ligne.append(somme)
                res.append(ligne)
            return Matrice(res)
    
    def transposee(self):
        """Retourne la transposée de <self> : Une matrice m×n donne une matrice n×m."""
        res = []
        for j in range(self.nb_colonnes()):
            ligne = []
            for i in range(self.nb_lignes()):
                ligne.append(self.data[i][j])
            res.append(ligne)
        return Matrice(res)
    
    def sous_matrice(self, j):
        """Retourne la sous-matrice de <self> obtenue en supprimant
        la ligne 0 et la colonne <j>."""
        res = []
        for i in range(1, self.nb_lignes()):
            ligne = []
            for k in range(self.nb_colonnes()):
                if k != j:
                    ligne.append(self.data[i][k])
            res.append(ligne)
        return Matrice(res)            
                
    def determinant(self):
        """Retourne le déterminant de <self>."""
        if self.nb_lignes() != self.nb_colonnes():
            raise ValueError("La matrice n'est pas carrée")
        if self.nb_lignes() == 1:
            return self.data[0][0]
        det = 0
        for j in range(self.nb_colonnes()):
            signe = +1 if j%2 == 0 else -1
            sous_mat = self.sous_matrice(j)
            det += signe * self.data[0][j] * sous_mat.determinant()
        return det
    
    def identite(n):
        """Retourne la matrice identité de taille n×n"""
        res = []
        for i in range(n):
            ligne = []
            for j in range(n):
                if i == j:
                    ligne.append(1)
                else:
                    ligne.append(0)
            res.append(ligne)
        return Matrice(res)
    
    def concat_horizontale(self, other):
        """Retourne la matrice obtenue en accolant <other> à droite de <self>."""
        res = []
        if self.nb_lignes() != other.nb_lignes():
            raise ValueError("Les matrices self et other doivent avoir le même nombre de lignes")
        for i in range(self.nb_lignes()):
            ligne = self.data[i] + other.data[i]
            res.append(ligne)
        return Matrice(res)
            
    def normaliser_ligne(self, aug, j, n):
        """Divise chaque élément de la ligne j de <aug> par le pivot aug.data[j][j]
        de sorte que aug.data[j][j] vaille 1 après l'opération."""
        pivot = aug.data[j][j]
        for k in range(2*n):
            aug.data[j][k] /= pivot

    def eliminer_colonne(self, aug, j, n):
        """Pour chaque ligne i différente de j, soustrait un multiple de la ligne j
        à la ligne i de sorte que aug.data[i][j] vaille 0 après l'opération."""
        for i in range(n):
            if i != j:
                facteur = aug.data[i][j]
                for k in range(2*n):
                    aug.data[i][k] -= facteur * aug.data[j][k]
    
    def inverse(self):
        """Retourne l'inverse de <self> par la méthode de Gauss-Jordan."""
        res = []
        if self.nb_lignes() != self.nb_colonnes():
            raise ValueError("La matrice n'est pas carrée")
        if self.determinant() == 0:
            raise ValueError("La matrice n'est pas inversible")
        n = self.nb_lignes()
        aug = self.concat_horizontale(Matrice.identite(n))
        for j in range(n):
            self.normaliser_ligne(aug, j, n)
            self.eliminer_colonne(aug, j, n)
        for i in range(n):         
            res.append(aug.data[i][n:])
        return Matrice(res)        
                
                
if __name__ == "__main__":
    m1 = Matrice([[1,2,3], [4,5,6], [7,8,9]])
    m2 = Matrice([[1,0], [0,1]])
    m3 = Matrice([[1,2], [4,5], [3,7]])
    m4 = Matrice([[2,6], [5,3], [4,1]])
    m5 = Matrice([[5,6], [9,7], [8,3]])
    m6 = Matrice([[1,2], [3,4]])
    v = Vecteur([1, 2, 3])
    print(m1)
    print(repr(m2))
    print(repr(m3))
    print(f"Nombre de lignes: {m3.nb_lignes()}")
    print(f"Nombre de colonnes: {m2.nb_colonnes()}")
    print(f"Addition de deux matrices:\n{m3 + m4}")
    print(f"Soustraction de deux matrices:\n{m5 - m4}")
    print(f"Produit d'une matrice avec un scalaire:\n{m1 * 3}")
    print(f"Produit d'une matrice et d'un vecteur:\n{m1 @ v}")
    print(f"Produit matricielle:\n{m1 @ m3}")
    print(f"La transposée de ma matrice:\n{m5.transposee()}")
    print(f"Ma sous-matrice:\n{m1.sous_matrice(0)}")
    print(f"Les déterminants de mes matrices: {m6.determinant()} et {m1.determinant()}")
    print(f"Matrice identité de taille n:\n{Matrice.identite(4)}")
    print(f"Matrice identité de taille n:\n{m3.concat_horizontale(m4)}")
    print(f"L'inverse de ma matrice:\n{m6.inverse()}")
    print(f"Ma matrice identité:\n{m6 @ m6.inverse()}")