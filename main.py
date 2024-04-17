
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
            self.content = booléens[:]
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
                b = (b + self.s[i]) % 2 # XOR
        self.__decalage(b)
        return output


def make_LFRS_17():
    pass

def make_LFRS_25():
    pass