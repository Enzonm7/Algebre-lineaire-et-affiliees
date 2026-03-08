class Matrice:
    
    def __init__(self, data):
        if data == []:
            raise ValueError("Matrice vide non autorisée !")
        for i in range(len(data)):
            if data[i] == []:
                raise ValueError("Matrice vide non autorisée !")
            elif len(data[i]) != len(data[0]):
                raise ValueError("Les lignes sont de longueurs différentes!")
        self.data = []
        for ligne in data:
            self.data.append(list(ligne))
            
    
    def __str__(self):
        m = ""
        for i in range(len(self.data)):
            if i == 0:
                m += str(self.data[i]) 
            else:
                m += "\n" + str(self.data[i])  
        return m
            
    def __repr__(self):
        return "Matrice(" + str(self.data) + ")"
    
    def nb_lignes(self):
        return len(self.data)
    
    def nb_colonnes(self):
        return len(self.data[0])
    
    def __add__(self, other):
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
        res = []
        for i in range(self.nb_lignes()):
            ligne = []
            for j in range(self.nb_colonnes()):
                ligne.append(self.data[i][j] * coefficient)
            res.append(ligne)
        return Matrice(res)
            
    
    def __matmul__(self, other):
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
        res = []
        for j in range(self.nb_colonnes()):
            ligne = []
            for i in range(self.nb_lignes()):
                ligne.append(self.data[i][j])
            res.append(ligne)
        return Matrice(res)
    
    
if __name__ == "__main__":
    m1 = Matrice([[1,2,3], [4,5,6], [7,8,9]])
    m2 = Matrice([[1,0], [0,1]])
    m3 = Matrice([[1,2], [4,5], [3,7]])   
    m4 = Matrice([[2,6], [5,3], [4,1]]) 
    m5 = Matrice([[5,6], [9,7], [8,3]]) 
    print(m1)
    print(repr(m2))
    print(repr(m3))
    print(f"Nombre de lignes: {m3.nb_lignes()}")
    print(f"Nombre de colonnes: {m2.nb_colonnes()}")
    print(f"Addition de deux matrices:\n{m3 + m4}")
    print(f"Soustraction de deux matrices:\n{m5 - m4}")
    print(f"Produit d'une matrice avec un scalaire:\n{m1 * 3}")
    print(f"Produit matricielle:\n{m1 @ m3}")
    print(f"La transposée de ma matrice:\n{m5.transposee()}")
    