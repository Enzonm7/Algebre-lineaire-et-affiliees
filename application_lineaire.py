"""Classe représentant une application linéaire de R^n dans R^m."""

from vecteur import Vecteur
from matrice import Matrice

class ApplicationLineaire:
    
    def __init__(self, matrice):
        """Constructeur qui crée une application linéaire à partir de <matrice>."""
        if not isinstance(matrice, Matrice):
            raise ValueError("L'argument doit être une instance de Matrice")
        self.matrice = Matrice(matrice.data)
        
    def __str__(self):
        """Convertit <self> en une chaîne de caractères pour l'affichage."""
        n = self.matrice.nb_colonnes()
        m = self.matrice.nb_lignes()
        en_tete = "Application linéaire(R^" + str(n) + " -> R^" + str(m) + ")"
        return en_tete + "\n" + str(self.matrice)
    
    def __repr__(self):
        """Représentation formelle de <self> permettant de recréer l'objet."""
        return "Application linéaire(" + str(self.matrice.data) + ")"
    
    def image(self, vecteur):
        """Retourne l'image de <vecteur> par l'application linéaire."""
        if not isinstance(vecteur, Vecteur):
            raise ValueError("L'argument doit être une instance de Vecteur")
        return self.matrice @ vecteur
    
    def copier_tableau(self):
        """Retourne une copie de travail de self.matrice.data."""
        tableau = []
        for ligne in self.matrice.data:
            tableau.append(list(ligne))
        return tableau
        
    def trouver_pivot(self, tableau, col, ligne_pivot):
        """Retourne l'indice de la première ligne >= ligne_pivot 
        ayant un coefficient non nul dans la colonne col."""
        for i in range(ligne_pivot, len(tableau)):
            if tableau[i][col] != 0:
                return i
        return -1

    def normaliser_pivot(self, tableau, ligne_pivot, col, n):
        """Divise la ligne ligne_pivot par le pivot."""
        pivot = tableau[ligne_pivot][col]
        for k in range(n):
            tableau[ligne_pivot][k] /= pivot

    def eliminer(self, tableau, ligne_pivot, col, m, n):
        """Annule tous les coefficients de la colonne col 
        sauf celui de ligne_pivot."""
        for i in range(m):
            if i != ligne_pivot:
                facteur = tableau[i][col]
                for k in range(n):
                    tableau[i][k] -= facteur * tableau[ligne_pivot][k]
    
    def gauss(self):
        """Retourne le tableau après pivot de Gauss 
        et la liste des colonnes pivot."""
        tableau = self.copier_tableau()
        m = self.matrice.nb_lignes()
        n = self.matrice.nb_colonnes()
        ligne_pivot = 0
        colonnes_pivot = []
        for col in range(n):
            i = self.trouver_pivot(tableau, col, ligne_pivot)
            if i == -1:
                continue
            tableau[ligne_pivot], tableau[i] = tableau[i], tableau[ligne_pivot]
            self.normaliser_pivot(tableau, ligne_pivot, col, n)
            self.eliminer(tableau, ligne_pivot, col, m, n)
            colonnes_pivot.append(col)
            ligne_pivot += 1
        return tableau, colonnes_pivot
    
    def rang(self):
        """Retourne le rang de l'application linéaire."""
        tableau, colonnes_pivot = self.gauss()
        rang = 0
        for ligne in tableau:
            for coeff in ligne:
                if coeff != 0:
                    rang += 1
                    break
        return rang
    
    def est_injective(self):
        """Retourne True si l'application est injective."""
        return self.rang() == self.matrice.nb_colonnes()

    def est_surjective(self):
        """Retourne True si l'application est surjective."""
        return self.rang() == self.matrice.nb_lignes() 

    def est_bijective(self):
        """Retourne True si l'application est bijective."""
        return self.est_injective() and self.est_surjective()
    
    def colonnes_libres(self, colonnes_pivot):
        """Retourne la liste des colonnes sans pivot."""
        colonnes_libres = []
        for col in range(self.matrice.nb_colonnes()):
            if col not in colonnes_pivot:
                colonnes_libres.append(col)
        return colonnes_libres

    def construire_vecteur_noyau(self, tableau, colonnes_pivot, col_libre):
        """Construit un vecteur de base du noyau pour une colonne libre donnée."""
        n = self.matrice.nb_colonnes()
        vecteur = []
        for col in range(n):
            if col == col_libre:
                vecteur.append(1)
            elif col in colonnes_pivot:
                lig = colonnes_pivot.index(col)
                vecteur.append(-tableau[lig][col_libre])
            else:
                vecteur.append(0)
        return Vecteur(vecteur)

    def noyau(self):
        """Retourne une liste de vecteurs formant une base du noyau."""
        tableau, colonnes_pivot = self.gauss()
        cols_libres = self.colonnes_libres(colonnes_pivot)
        base_noyau = []
        for col_libre in cols_libres:
            base_noyau.append(self.construire_vecteur_noyau(tableau, colonnes_pivot, col_libre))
        return base_noyau
    
    
if __name__ == "__main__":
    m1 = Matrice([[1,2,3], [4,5,6]])
    m2 = Matrice([[1, 0], [0, 1]])
    m3 = Matrice([[1, 2, 3], [4, 5, 6]])
    f1 = ApplicationLineaire(m1)
    f2 = ApplicationLineaire(m2)
    f3 = ApplicationLineaire(m3)
    v1 = Vecteur([1,2,3])
    print(f1)
    print(repr(f1))
    print(f"Affichage f2:\n{f2}")
    print(f"Image de v1 par f1:\n{f1.image(v1)}")
    print(f"Rang de f1: {f1.rang()}")
    print(f"f1 injective: {f1.est_injective()}") 
    print(f"f1 surjective: {f1.est_surjective()}")  
    print(f"f2 bijective: {f2.est_bijective()}")
    print(f"Noyau de f4:\n{f3.noyau()}")
    print(f"Noyau de f2: {f2.noyau()}")