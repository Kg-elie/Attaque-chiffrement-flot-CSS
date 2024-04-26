##############
# LIBRAIRIES #
##############


import random, sys, time


###########
# CLASSES #
###########


class LFSR(object):

    def __init__(self, initialisation_s:list[bool], retroaction_c:list[bool]) -> None:
        self.s = initialisation_s[:] # registre initialisé à 0 sur chaques bits
        self.c = retroaction_c[:] # coefficiants de rétroaction initialisés à 0
        self.octets = [] # octet en sortie du LFSR
    
    def cycle(self) -> bool:
        output = self.s[-1]
        b = 0
        for i in range(len(self.s)):
            if self.c[i] == 1:
                b = (b + self.s[i]) % 2
        self.s = [b] + self.s[:-1]
        return output
    
    def bits(self) -> list[bool]:
        return self.s[:]
    
    def __repr__(self) -> str:
        output = "LFSR : \n"
        return "LFSR\n{\nTAILLE : "+len(self.s).__repr__()+"\nBITS :       IN -> "+self.s.__repr__()+" -> OUT\nRETROACTION :      "+self.c.__repr__()+"\n}"

class CSS(object):
    
    def __init__(self, key:list[bool]) -> None:
        key_17 = [1] + key[:16]
        key_25 = [1] + key[16:]
        self.c = 0
        self.lfsr17 = lfsr17(key_17)
        self.lfsr25 = lfsr25(key_25)
        self.octets = [] # octet en sortie du CSS
    
    def cycle(self) -> list[bool]:
        x = get_octet_from_lfsr(lfsr=self.lfsr17)
        y = get_octet_from_lfsr(lfsr=self.lfsr25)
        
        output = (x + y + self.c) % 256
        self.c = (x+y)//256
        z = to_bin(output)
        self.octets.append(output)
        while len(z) <= 7:
            z = [0] + z
        return z


#############
# FONCTIONS #
#############


def lfsr17(initialisation:list[bool])->LFSR:
    retro = [0 for i in range(17)]
    retro[14] = 1
    retro[0] = 1
    retro.reverse()
    return LFSR(initialisation, retro)


def lfsr25(initialisation:list[bool])->LFSR:
    retro = [0 for i in range(25)]
    retro[12] = 1
    retro[4] = 1
    retro[3] = 1
    retro[0] = 1
    retro.reverse()
    return LFSR(initialisation, retro)


def get_octet_from_lfsr(lfsr:LFSR) -> int:
    """Génère un octet à partir du LFSR fournit et renvoi son équivalent en base 10."""
    output_int = 0
    for i in range(8):
        b = lfsr.cycle()
        output_int += int(b)*(2**i)
    lfsr.octets.append(output_int)
    return output_int


def bin_to_int(octal:list) -> int:
    output = 0
    for i in range(7,-1,-1):
        val = octal[7-i]*(2**i)
        output += val
    return output


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


def chiffrer(key:list[bool], m:list[bool]):
    css = CSS(key)
    output = []
    while m:
        octet = m[:8]
        m = m[8:]
        octet_c = css.cycle()
        output += xor(octet_c, octet)
    return output


def dechiffrer(key:list[bool], c:list[bool]):
    css = CSS(key)
    output = []
    while c:
        octet = c[:8]
        c = c[8:]
        output += xor(css.cycle(),octet)
    return output


def bin_xbit(nb:int,x:int):
    """ retourne une liste de 16 bits"""
    return [int(i) for i in bin(nb)[2:].zfill(x)]


def verif_key(key: list, z: list):
    """ verifie si la clé est correcte"""
    css = CSS(key)
    for i in range(6):
        css.cycle()
        if css.octets[i] != z[i]:
            return False
    print
    return True


def attaque_chiffrement(z: list):
    """Retrouve l'etat initial du css avec ses 6 premiers octets de sortie"""
    print("# Lancement de l'attaque contre CSS")
    start = time.time()
    for i in range(2**16):
        key = bin_xbit(i,16)
        l = lfsr17([1]+key)
        lfsr17_octet = []
        for _ in range(3):
            lfsr17_octet.append(get_octet_from_lfsr(l))
        key.extend(etat_initial_lfsr25(lfsr17_octet, z[:3]))
        verif = verif_key(key,z)
        if verif:
            print(f" essai n°{i} : clé trouvée.\n {key}\n temps écoulé : {time.time()-start} sec.")
            return key


def random_key():
    key =  [ random.randint(0,1) for _ in range(40)]
    css = CSS(key)
    sortie = []
    for i in range(6):
        css.cycle()
        sortie.append(css.octets[i])

    print(f"""# Génération d'une clé aléatoire pour CSS\n {key}\n# Donnée dont on dispose pour l'attaque
 6 premiers Octets du CSS : {sortie}""")
    return sortie


def etat_initial_lfsr25(lfsr17_octet, css_octet)  :
    """ etat initial du lfsr25 a partir des 3 premiers octets de sortie du CSS et du lfsr17"""
    y = []
    c = 0
    for i in range(3):
        s = lfsr17_octet[i]
        z = css_octet[i]
        result = (z-(s+c))%256
        y = bin_xbit(result,8) + y
        if s+ result > 255:
            c = 1
        else:
            c = 0
    return y


###########################
# QUESTIONS DEVOIR MAISON #
###########################


def question_1():
    """Programmer le 1er LFSR de 17 bits et faire implémenter 
    une fonction de test qui vérifie que l'état prend bien les (2**17)-1 valeurs
    différentes pour une initialisation quelconque non-nulle du registre"""
    def test(n):
        print(f"Lancement d'un test de bouclage sur {n} cycles...")
        initialisation = [1 for i in range(17)]
        g17 = lfsr17(initialisation)
        for i in range(1, n):
            g17.cycle()
            if initialisation == g17.bits():
                print(f"True : boucle détectée au cycle n°{i} < {n}")
                return None
        print(f"False : pas de boucle détectée sur {n} cycles effectués.")
        return None
    print(lfsr17([1 for i in range(17)]))
    test((2**17)-1) # pas de boucle
    test((2**17)) # boucle
        


def question_2():
    """Programmer le 2nd LFSR de 25 bits"""
    initialisation = [1 for _ in range(25)] # initialisation à {1}**25
    print(lfsr25(initialisation))


def question_3():
    """Programmer chiffrement et déchiffrement"""
    clé = [0] * 40
    msg = [1] * 40
    print(f"clé                 = {clé}")
    print(f"message             = {msg}")
    c = chiffrer(key=clé, m=msg) # <=> Oxffffb66c39
    print(f"chiffrement...\nm_chiffré           = {c}")
    new_m = dechiffrer(key=clé, c=c)
    print(f"déchiffrement...\nm_chiffré_déchiffré = {new_m}")


def question_6():
    """Attaque du chiffrement CSS"""
    css_octets = random_key()
    attaque_chiffrement(css_octets)


########
# MAIN #
########


if __name__ == "__main__":
    match sys.argv[1]:
        case "1":
            print("\n## QUESTION 1 ##\nPour cette question les 17 bits d'initialisation sont à 1.")
            question_1()
        case "2":
            print("\n## QUESTION 2 ##\nPour cette question les 25 bits d'initialisation sont à 1.")
            question_2()
        case "3":
            print("\n## QUESTION 3 ##\n")
            question_3()
        case "4":
            print("\nRéponse à l'intérieur de dm2024.pdf\n")
        case "5":
            print("\nRéponse à l'intérieur de dm2024.pdf\n")
        case "6":
            print("\n## QUESTION 6 ##\n")
            question_6()
    print("")
