"""Classe représentant un système linéaire de la forme Ax = b."""

from vecteur import Vecteur
from matrice import Matrice
from application_lineaire import ApplicationLineaire

class SystemeLineaire:
    
    def __init__(self, matrice, vecteur):
        """Constructeur qui crée un système linéaire à partir de <matrice> et <vecteur>."""
        if not isinstance(matrice, Matrice):
            raise ValueError("L'argument doit être une instance de Matrice")
        if not isinstance(vecteur, Vecteur):
            raise ValueError("L'argument doit être une instance de Vecteur")
        if len(vecteur) != matrice.nb_lignes():
            raise ValueError("La taille du vecteur doit être égale au nombre de lignes de la matrice")
        self.matrice = Matrice(matrice.data)
        self.vecteur = Vecteur(vecteur.coordonnees)
        
    def __str__(self):
        """Convertit <self> en une chaîne de caractères pour l'affichage."""
        chaine = ""
        for i in range(self.matrice.nb_lignes()):
            chaine += str(self.matrice.data[i]) + " | " + str(self.vecteur[i])
            if i < self.matrice.nb_lignes() - 1:
                chaine += "\n"
        return chaine    
    
    def __repr__(self):
        """Représentation formelle de <self> permettant de recréer l'objet."""
        return "Systeme linéaire(" + repr(self.matrice) + ", \n" + repr(self.vecteur) + ")"
    
    def construire_tableau(self):
        """Retourne la matrice augmentée [A|b] obtenue en accolant <vecteur>
        comme dernière colonne à <matrice>."""
        tableau = []
        for valeur in self.vecteur:
            tableau.append([valeur])
        return self.matrice.concat_horizontale(Matrice(tableau))
    
    def est_compatible(self):
        """Retourne True si le système admet au moins une solution, False sinon."""
        app_matrice = ApplicationLineaire(self.matrice)
        rang_matrice = app_matrice.rang()
        tableau = self.construire_tableau()
        app_augmentee = ApplicationLineaire(tableau)
        rang_augmentee = app_augmentee.rang()
        return rang_matrice == rang_augmentee
    
    def resoudre(self):
        """Retourne la solution unique du système si elle existe."""
        if not self.est_compatible():
            raise ValueError("Le système n'admet pas de solution")
        app = ApplicationLineaire(self.construire_tableau())
        tableau, colonnes_pivot = app.gauss()
        if len(colonnes_pivot) < self.matrice.nb_colonnes():
            raise ValueError("Le système admet une infinité de solutions")
        solution = []
        for i in range(self.matrice.nb_colonnes()):
            solution.append(tableau[i][-1])
        return Vecteur(solution)

    
if __name__ == "__main__":
    m1 = Matrice([[1,2], [3,4], [0,1]])
    v1 = Vecteur([5,6,2])
    sys1 = SystemeLineaire(m1, v1)
    m2 = Matrice([[1, 2], [3, 4]])
    v2 = Vecteur([5, 6])
    sys2 = SystemeLineaire(m2, v2)
    m3 = Matrice([[1, 2], [2, 4]])
    v3 = Vecteur([3, 7])
    sys3 = SystemeLineaire(m3, v3)
    m4 = Matrice([[1, 2, 3], [2, 4, 6]])
    v4 = Vecteur([5, 10])
    sys4 = SystemeLineaire(m4, v4)
    print(sys1)
    print(repr(sys1))
    print(sys1.construire_tableau())
    print(f"sys2 compatible : {sys2.est_compatible()}")
    print(f"sys3 compatible : {sys3.est_compatible()}")
    print(f"Solution sys2 : {sys2.resoudre()}")
    try:
        print(sys3.resoudre())
    except ValueError as e:
        print(f"Erreur sys3 : {e}")
    try:
        print(sys4.resoudre())
    except ValueError as e:
        print(f"Erreur sys4 : {e}")