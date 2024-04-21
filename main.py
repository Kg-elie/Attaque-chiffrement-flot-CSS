import time

class LFSR(object):

    def __init__(self, taille_n:int, initialisation_s:list[bool], retroaction_c:tuple[int]) -> None:
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

    initialisation = [1 for _ in range(17)] # initialisation à {1}**17
    lfsr_17 = LFSR(17, initialisation_s = initialisation, retroaction_c = (14,0)) # le 1er LFSR
    print(test(n = (2**17)-1)) 
    print(test(n = 2**17))

def question_2_3_2():
    """Programmer le 2nd LFSR de 25 bits"""
    initialisation = [1 for _ in range(25)] # initialisation à {1}**25
    lfsr_25 = LFSR(25, initialisation_s = initialisation, retroaction_c = (12,4,3,0)) # le 2nd LFSR

def question_2_3_3():
    
    def get_octet_from_lfsr(lfsr:LFSR) -> int:
        """Génère un octet à partir du LFSR fournit et renvoi son équivalent en base 10."""
        output_int = 0
        for i in range(8):
            b = lfsr.cycle()
            output_int += int(b)*(2**i)
        return output_int
    
    def to_bin(z:int) -> list[bool]:
        i = 0
        output = []
        while z > 0:
            output.append(z % 2)
            z = z // 2
        output.reverse()
        return output
    
    def xor(l1:list[bool],l2:list[bool]) -> list[bool]:
        output = []
        for i in range(len(l1)):
            output.append((l1[i] + l2[i]) % 2)
        return output

    class CSS(object):

        def __init__(self, key:list[bool]) -> None:
            key_17 = [1] + key[:16]
            key_25 = [1] + key[16:]
            self.c = 0
            self.lfsr17 = LFSR(taille_n=17, initialisation_s=key_17, retroaction_c=(14,0))
            self.lfsr25 = LFSR(taille_n=25, initialisation_s=key_25, retroaction_c=(12,4,3,0))
        
        def cycle(self) -> list[bool]:
            x = get_octet_from_lfsr(lfsr=self.lfsr17)
            y = get_octet_from_lfsr(lfsr=self.lfsr25)
            output = (x + y + self.c) % 256
            self.c += (x+y)//256
            return to_bin(output)


    def encrypter(key:list[bool], m:list[bool]):
        css = CSS(key)
        output = []
        while m:
            octet = m[:8]
            m = m[8:]
            output += xor(css.cycle(),octet)
        return output

    key = [0] * 40
    m = [1] * 40
    c = encrypter(key=key, m=m)
    print(c)


if __name__ == "__main__":
    question_2_3_3()