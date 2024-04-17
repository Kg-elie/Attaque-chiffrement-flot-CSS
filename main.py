import time

class LFSR(object):

    def __init__(self, taille_n:int, initialisation_s:tuple[bool], retroaction_c:tuple[int]) -> None:
        """initialisation -> s = [ s[0], ... , s[n-1] ]\n
        rétroaction -> c = [ c0, ... , cn-1 ]\n
        """
        self.n = taille_n # taille du LFSR
        self.s = [0 for _ in range(self.n)] # registre initialisé à 0 sur chaques bits
        self.c = [0 for _ in range(self.n)] # coefficiants de rétroaction initialisés à 0
        self.__set_initialisation(initialisation_s)
        self.__set_retroaction(retroaction_c)

    def __set_initialisation(self, booléens:list[bool]):
        """prend une liste de booléens de la taille du LFSR pour les charger dans le registre"""
        if self.n == len(booléens):
            self.s = booléens[:]
        else:
            raise ValueError

    def __set_retroaction(self, retroaction:tuple[int]):
        """"""
        for r in retroaction:
            self.c[r] = 1
    
    def __decalage(self, b:bool):
        """Enlève s[0] et décalle tout les bits du registre tandis que b est ajouté en fin de registre"""
        self.s = self.s[1:] + [b]
    
    def cycle(self) -> bool:
        """Un cycle de fonctionnement LFSR"""
        output = self.s[0]
        b = 0 # nouveau bit généré à partir des coefficiants de c et s
        for i in range(self.n):
            if self.c[i]:
                #print(b, self.s[i])
                b = (b + self.s[i]) % 2 # XOR
                #time.sleep(0.5)
        self.__decalage(b)
        return output


def question_2_3_1():
    """Programmer le 1er LFSR de 17 bits et faire implémenter 
    une fonction de test qui vérifie que l'état prend bien les (2**17)-1 valeurs
    différentes pour une initialisation quelconque non-nulle du registre"""

    def test(n):
        """Vérifie si pendant n cycles le registre courant du LFSR est égal à l'initialisation du LFSR.\n
        return [True | Tuple:(False, int)]\n
        int indiquant le i-ième cycle où le vecteur d'initialisation est égal à la configuration actuelle."""
        
        i = 1
        while i < n:
            lfsr_17.cycle()
            if lfsr_17.s == initialisation:
                return (False, i)
            i += 1
        return True

    initialisation = [1 for _ in range(17)]
    lfsr_17 = LFSR(17, initialisation_s = initialisation, retroaction_c = (14,0)) # le 1er LFSR
    print(test(n = (2**17)-1)) 
    print(test(n = 2**17))

def question_2_3_2():
    """Programmer le 2nd LFSR de 25 bits"""
    initialisation = [1 for _ in range(25)]
    lfsr_17 = LFSR(17, initialisation_s = initialisation, retroaction_c = (12,4,3,0)) # le 2nd LFSR

def question_2_3_3():
    pass

if __name__ == "__main__":
    question_2_3_1()