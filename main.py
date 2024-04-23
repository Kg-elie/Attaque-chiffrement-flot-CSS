###########
# CLASSES #
###########
import random

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
        return "IN -> "+self.s.__repr__()+" -> OUT"

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


################
# QUESTIONS DM #
################

def question_2_3_1():
    """Programmer le 1er LFSR de 17 bits et faire implémenter 
    une fonction de test qui vérifie que l'état prend bien les (2**17)-1 valeurs
    différentes pour une initialisation quelconque non-nulle du registre"""
    def test(n):
        initialisation = [1 for i in range(17)]
        g17 = lfsr17(initialisation)
        for i in range(1, n):
            g17.cycle()
            if initialisation == g17.bits():
                print(f"boucle détectée en {i}")
                return False
        return True
    
    print(test((2**17)-1)) # pas de boucle
    print(test((2**17))) # boucle
        


def question_2_3_2():
    """Programmer le 2nd LFSR de 25 bits"""
    initialisation = [1 for _ in range(25)] # initialisation à {1}**25
    g25 = lfsr25(initialisation)

def question_2_3_3():
    """Programmer chiffrement et déchiffrement"""
    key = [0] * 40
    m = [1] * 40
    print(f"key = \n{key}")
    print(f"m = \n{m}")
    c = chiffrer(key=key, m=m) # <=> Oxffffb66c39
    print(f"c = \n{c}")
    new_m = dechiffrer(key=key, c=c)
    print(f"new_m = \n{new_m}")


def question_4(lfsr17: LFSR, css : CSS):
    """ etat initial du lfsr25 a partir des 3 premiers octets de sortie du CSS et du lfsr17"""
    y =[]
    c = 0
    for i in range(3):
        s = lfsr17.octets[i]
        z = css.octets[i]
        y.append((z-(s+c))%256)
        if s+ y[i] + c > 255:
            c = 1
    print( f"les octets de y sont {y}")

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
    return True


def attaque_chiffrement(z: list):
    """ retrouver l'etat initial du css avec ses 6 premiers octets de sortie"""
    for i in range(2**16):
        key = bin_xbit(i,16)
        l = lfsr17([1]+key)
        lfsr17_octet = []
        for _ in range(3):
            lfsr17_octet.append(get_octet_from_lfsr(l))
        key.extend(etat_initial_lfsr25(lfsr17_octet, z[:3]))
        verif = verif_key(key,z)
        if verif:
            print(f"la clé est {key} pour l'essai {i}")
            return key
    


def random_key():
    key =  [ random.randint(0,1) for _ in range(40)]
    css = CSS(key)
    sortie = []
    s_sortie = []
    for i in range(6):
        css.cycle()
        sortie.append(css.octets[i])

    print(f"{key}, sortie = {sortie}")
    return sortie, key, css.lfsr17.octets, css.lfsr25.octets


def correspondance(liste1, liste2):

# Séparer chaque liste à partir du 17ème bit
    octets_liste1 = [liste1[i:i+8] for i in range(16, len(liste1), 8)]
    octets_liste2 = [liste2[i:i+8] for i in range(16, len(liste2), 8)]

    print("Octets de la première liste à partir du 17ème bit:", octets_liste1)
    print("Octets de la deuxième liste à partir du 17ème bit:", octets_liste2)



def question_2_3_4():
    pass

if __name__ == "__main__":
    
    test = random_key()
    key16 = [1] + test[1][:16]

    octets = []
    l = lfsr17(key16)
    for _ in range(3):
        octets.append(get_octet_from_lfsr(l))
    
    key = key16 + etat_initial_lfsr25(octets, test[0])
    print(test[2], test[3])
    print(key[1:])
    correspondance(test[1], key[1:])
    essai = verif_key(key[1:],test[0])
    print(essai)
    attaque_chiffrement(test[0])
    
    