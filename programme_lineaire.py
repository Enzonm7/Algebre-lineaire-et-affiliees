"""Classe représentant un programme linéaire sous forme standard."""

from vecteur import Vecteur
from matrice import Matrice

class ProgrammeLineaire:
    
    def __init__(self, fonction, matrice, vecteur):
        """Constructeur qui crée un programme linéaire à partir de <fonction>,
        <matrice> et <vecteur>."""
        self.fonction = fonction
        self.matrice = matrice
        self.vecteur = vecteur
        self.verifier_validite()
        self.fonction = Vecteur(fonction.coordonnees)
        self.matrice = Matrice(matrice.data)
        self.vecteur = Vecteur(vecteur.coordonnees)
        
    def verifier_validite(self):
        """Vérifie la validité des arguments du programme linéaire."""
        if not isinstance(self.fonction, Vecteur):
            raise ValueError("fonction doit être une instance de Vecteur")
        if not isinstance(self.matrice, Matrice):
            raise ValueError("matrice doit être une instance de Matrice")
        if not isinstance(self.vecteur, Vecteur):
            raise ValueError("vecteur doit être une instance de Vecteur")
        if len(self.fonction) != self.matrice.nb_colonnes():
            raise ValueError("fonction doit avoir autant de composantes que de colonnes dans matrice")
        if len(self.vecteur) != self.matrice.nb_lignes():
            raise ValueError("vecteur doit avoir autant de composantes que de lignes dans matrice")
        for i in range(len(self.vecteur)):
            if self.vecteur[i] < 0:
                raise ValueError("Les composantes de vecteur doivent être positives ou nulles")
    
    def __str__(self):
        """Convertit <self> en une chaîne de caractères pour l'affichage."""
        m = self.matrice.nb_lignes()
        n = len(self.fonction)
        tableau = self.construire_tableau()
        chaine = "     x   y"
        for i in range(m):
            chaine += "  e" + str(i + 1)
        chaine += "  Obj\n"
        chaine += "Max " + str(tableau[0][:-1]) + " | " + str(tableau[0][-1]) + "\n"
        for i in range(1, m + 1):
            chaine += "e" + str(i) + "  " + str(tableau[i][:-1]) + " | " + str(tableau[i][-1]) + "\n"
        return chaine
        
    def __repr__(self):
        """Représentation formelle de <self> permettant de recréer l'objet."""
        return "Programme linéaire(" + repr(self.fonction) + ", \n" + repr(self.matrice) + " " + repr(self.vecteur) + ")"
    
    def construire_ligne_max(self, m, n):
        """Construit la ligne Max du tableau du simplex : coefficients de la
        fonction objectif, zéros pour les variables d'écart, zéro pour l'objectif."""
        ligne_max = []
        for i in range(n):
            ligne_max.append(self.fonction[i])
        for i in range(m):
            ligne_max.append(0)
        ligne_max.append(0)
        return ligne_max

    def construire_ligne_contrainte(self, i, m, n):
        """Construit les lignes de contraintes avec variables d'écart : coefficients de la
        contrainte i, ligne i de la matrice identité, second membre i."""
        ligne = []
        for j in range(n):
            ligne.append(self.matrice.data[i][j])
        for k in range(m):
            if k == i:
                ligne.append(1)
            else:
                ligne.append(0)
        ligne.append(self.vecteur[i])
        return ligne
    
    def construire_tableau(self):
        """Construit et retourne le tableau du simplex initial."""
        m = self.matrice.nb_lignes()
        n = self.matrice.nb_colonnes()
        tableau = []
        tableau.append(self.construire_ligne_max(m, n))
        for i in range(m):
            tableau.append(self.construire_ligne_contrainte(i, m, n))
        return tableau
            
    def colonne_pivot(self, tableau):
        """Retourne l'indice de la colonne pivot selon le 1er critère de Dantzig, ou -1 si aucun."""
        col_pivot = -1
        max_val = 0
        for j in range(len(tableau[0]) - 1):
            if tableau[0][j] > max_val:
                max_val = tableau[0][j]
                col_pivot = j
        return col_pivot
        
    def ligne_pivot(self, tableau, col):
        """Retourne l'indice de la ligne pivot selon le 2eme critère de Dantzig, ou -1 si aucun coefficient positif."""
        lig_pivot = -1
        min_rapport = -1
        for i in range(1, len(tableau)):
            if tableau[i][col] > 0:
                rapport = tableau[i][-1] / tableau[i][col]
                if min_rapport == -1 or rapport < min_rapport:
                    min_rapport = rapport
                    lig_pivot = i
        return lig_pivot
    
    def pivoter(self, tableau, lig, col):
        """Effectue le pivot sur la ligne <lig> et la colonne <col> :
        normalise la ligne pivot puis élimine sur toutes les autres lignes."""
        n = len(tableau[0])
        # Étape 1 — on veut 1 au niveau du pivot
        pivot = tableau[lig][col]
        for j in range(n):
            tableau[lig][j] /= pivot
        # Étape 2 — on veut 0 au dessus et en dessous du pivot
        for i in range(len(tableau)):
            if i != lig:
                facteur = tableau[i][col]
                for j in range(n):
                    tableau[i][j] -= facteur * tableau[lig][j]
        
    def resoudre(self):
        """Résout le programme linéaire par la méthode du simplex et
        retourne le tableau final optimisé."""
        tableau = self.construire_tableau()
        col = self.colonne_pivot(tableau)
        while col != -1:
            lig = self.ligne_pivot(tableau, col)
            if lig == -1:
                raise ValueError("Le programme linéaire n'est pas borné")
            self.pivoter(tableau, lig, col)
            col = self.colonne_pivot(tableau)
        return tableau
        
    def solution(self):
        """Retourne la solution optimale sous forme de Vecteur et la valeur
        optimale de la fonction objectif."""
        tableau = self.resoudre()
        m = self.matrice.nb_lignes()
        n = len(self.fonction)
        solution = []
        for j in range(n):
            valeur = 0
            for i in range(1, m + 1):
                if tableau[i][j] == 1:
                    valeur = tableau[i][-1]
            solution.append(valeur)
        valeur_optimale = -tableau[0][-1]
        return Vecteur(solution), valeur_optimale
    
    
if __name__ == "__main__":
    v1 = Vecteur([40, 50])
    m1 = Matrice([[10, 10], [10, 20], [20, 10]])
    v = Vecteur([50, 80, 80])
    prog1 = ProgrammeLineaire(v1, m1, v)
    print(prog1)
    print(repr(prog1))
    print(f"\nTableau initial:")
    for ligne in prog1.construire_tableau():
        print(ligne)
        
    print(f"\nColonne pivot: {prog1.colonne_pivot(prog1.construire_tableau())}")
    tableau = prog1.construire_tableau()
    col = prog1.colonne_pivot(tableau)
    print(f"Ligne pivot: {prog1.ligne_pivot(tableau, col)}")
    prog1.pivoter(tableau, prog1.ligne_pivot(tableau, col), col)
        
    print(f"\nTableau résolu:")
    for ligne in prog1.resoudre():
        print(ligne)
        
    sol, val = prog1.solution()
    print(f"\nSolution optimale : {sol}")
    print(f"Valeur optimale : {val}")