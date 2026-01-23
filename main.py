import pygame
import time
import random
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def citeste_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def salveaza_highscore(scor):
    with open("highscore.txt", "w") as f:
        f.write(str(scor))

pygame.init()
pygame.mixer.init()

try:
    sunet_mancare = pygame.mixer.Sound(resource_path("media/audio/bite-sound.wav"))

except:
    sunet_mancare = None 

latime, inaltime = 600, 400
ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)
pygame.display.set_caption('Snake Game - Proiect Final')

NEGRU = (0, 0, 0)
ALB = (255, 255, 255)
ROSU = (213, 50, 80)
VERDE = (0, 255, 0)
ALBASTRU = (50, 153, 213)

dimensiune_bloc = 10
viteza = 15
ceas = pygame.time.Clock()

img_mar = pygame.image.load(resource_path("media/textures/zero.png")).convert_alpha()
img_corp = pygame.image.load(resource_path("media/textures/two.png")).convert_alpha()
img_cap = pygame.image.load(resource_path("media/textures/one.png")).convert_alpha()
img_coada = pygame.image.load(resource_path("media/textures/three.png")).convert_alpha()
img_curba = pygame.image.load(resource_path("media/textures/turn.png")).convert_alpha()

img_mar = pygame.transform.scale(img_mar, (dimensiune_bloc, dimensiune_bloc))
img_corp = pygame.transform.scale(img_corp, (dimensiune_bloc, dimensiune_bloc))
img_cap = pygame.transform.scale(img_cap, (dimensiune_bloc, dimensiune_bloc))
img_coada = pygame.transform.scale(img_coada, (dimensiune_bloc, dimensiune_bloc))
img_curba = pygame.transform.scale(img_curba, (dimensiune_bloc, dimensiune_bloc))

pygame.font.init() 
font_stil = pygame.font.SysFont("bahnschrift", 25)

def calculeaza_unghi(segment_curent, segment_vecin):
    dx = segment_curent[0] - segment_vecin[0]
    dy = segment_curent[1] - segment_vecin[1]
    
    if dy < 0: return 0    
    if dy > 0: return 180  
    if dx > 0: return 270  
    if dx < 0: return 90   
    return 0

def deseneaza_sarpe(bloc, lista_sarpe, dx, dy):
    for i in range(len(lista_sarpe)):
        x, y = lista_sarpe[i][0], lista_sarpe[i][1]
        
        if i == len(lista_sarpe) - 1:
            if len(lista_sarpe) > 1:
                unghi = calculeaza_unghi(lista_sarpe[i], lista_sarpe[i-1])
            else:
                if dy < 0: unghi = 0
                elif dy > 0: unghi = 180
                elif dx > 0: unghi = 270
                elif dx < 0: unghi = 90
                else: unghi = 0
            img_rotita = pygame.transform.rotate(img_cap, unghi)
            ecran.blit(img_rotita, (x, y))

        elif i == 0 and len(lista_sarpe) > 1:
            unghi = calculeaza_unghi(lista_sarpe[i+1], lista_sarpe[i])
            img_rotita = pygame.transform.rotate(img_coada, unghi)
            ecran.blit(img_rotita, (x, y))

        else:
            prev_seg = lista_sarpe[i-1]
            next_seg = lista_sarpe[i+1]
            
            dx_p, dy_p = x - prev_seg[0], y - prev_seg[1]
            dx_n, dy_n = next_seg[0] - x, next_seg[1] - y

            if dx_p != dx_n or dy_p != dy_n:

                if (dx_p == bloc and dy_n == -bloc) or (dy_p == bloc and dx_n == -bloc):
                    unghi = 0    
                elif (dx_p == -bloc and dy_n == -bloc) or (dy_p == bloc and dx_n == bloc):
                    unghi = 270   
                elif (dx_p == -bloc and dy_n == bloc) or (dy_p == -bloc and dx_n == bloc):
                    unghi = 180  
                else:
                    unghi = 90  
                
                img_rotita = pygame.transform.rotate(img_curba, unghi)
                ecran.blit(img_rotita, (x, y))
            else:
                unghi = calculeaza_unghi(lista_sarpe[i], lista_sarpe[i-1])
                img_rotita = pygame.transform.rotate(img_corp, unghi)
                ecran.blit(img_rotita, (x, y))

def ecran_pauza():
    global latime, inaltime, ecran 
    
    screenshot = ecran.copy()
    small_img = pygame.transform.smoothscale(screenshot, (latime // 4, inaltime // 4))
    blurred_img = pygame.transform.smoothscale(small_img, (latime, inaltime))
    
    overlay = pygame.Surface((latime, inaltime))
    overlay.set_alpha(128) 
    overlay.fill((0, 0, 0)) 

    pausa = True
    while pausa:
        ecran.blit(blurred_img, (0, 0))
        ecran.blit(overlay, (0, 0))
        
        mesaj = font_stil.render("Pauza", True, VERDE)
        info = font_stil.render("Apasa P pentru a continua", True, ALB)
        ecran.blit(mesaj, [latime // 3, inaltime // 2.5])
        ecran.blit(info, [latime // 4, inaltime // 2])
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausa = False
            if event.type == pygame.VIDEORESIZE:
                latime, inaltime = event.w, event.h
                ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)

                small_img = pygame.transform.smoothscale(screenshot, (latime // 4, inaltime // 4))
                blurred_img = pygame.transform.smoothscale(small_img, (latime, inaltime))
                overlay = pygame.Surface((latime, inaltime))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                
class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.viata = 255  
        self.culoare = (255, 255, 255) 

    def miscare(self):
        self.x += self.vx
        self.y += self.vy
        self.viata -= 15 

    def desenare(self, ecran):
        if self.viata > 0:
       
            s = pygame.Surface((3, 3))
            s.set_alpha(self.viata)
            s.fill(self.culoare)
            ecran.blit(s, (self.x, self.y))

def joc():
    global latime, inaltime, ecran, viteza
    game_over = False
    game_close = False
    high_score = citeste_highscore()
    viteza = 15
    particule = []

    try:
        pygame.mixer.music.load(resource_path("media/audio/main-theme.mp3"))
        pygame.mixer.music.play(-1)
    except:
        pass

    x1 = (latime // 2 // 10) * dimensiune_bloc
    y1 = (inaltime // 2 // 10) * dimensiune_bloc
    x1_schimbare, y1_schimbare = 0, 0

    lista_sarpe = []
    lungime_sarpe = 1

    mancare_x = random.randint(0, (latime - dimensiune_bloc) // 10) * dimensiune_bloc
    mancare_y = random.randint(0, (inaltime - dimensiune_bloc) // 10) * dimensiune_bloc

    while not game_over:

        while game_close == True:
            ecran.fill(ALBASTRU)
            scor_final = lungime_sarpe - 1
            if scor_final > high_score:
                high_score = scor_final
                salveaza_highscore(high_score)

            mesaj_pierdut = font_stil.render("Wasted", True, ROSU)
            mesaj_scor = font_stil.render(f"Scor: {scor_final}", True, ALB)
            mesaj_highscore = font_stil.render(f"Highscore: {high_score}", True, NEGRU)
            mesaj_info = font_stil.render("Q-Iesire C-Reincearca", True, ALB)

            ecran.blit(mesaj_pierdut, [latime // 3, inaltime // 4])
            ecran.blit(mesaj_scor, [latime // 4, inaltime // 2.5])
            ecran.blit(mesaj_highscore, [latime // 4, inaltime// 3])
            ecran.blit(mesaj_info, [latime // 4, inaltime - 50])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        joc()
                if event.type == pygame.VIDEORESIZE:
                    latime, inaltime = event.w, event.h
                    ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.VIDEORESIZE:
                latime, inaltime = event.w, event.h
                ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    ecran_pauza()
                elif event.key == pygame.K_LEFT and x1_schimbare == 0:
                    x1_schimbare, y1_schimbare = -dimensiune_bloc, 0
                elif event.key == pygame.K_RIGHT and x1_schimbare == 0:
                    x1_schimbare, y1_schimbare = dimensiune_bloc, 0
                elif event.key == pygame.K_UP and y1_schimbare == 0:
                    y1_schimbare, x1_schimbare = -dimensiune_bloc, 0
                elif event.key == pygame.K_DOWN and y1_schimbare == 0:
                    y1_schimbare, x1_schimbare = dimensiune_bloc, 0

        if x1 >= latime or x1 < 0 or y1 >= inaltime or y1 < 0:
            game_close = True

        x1 += x1_schimbare
        y1 += y1_schimbare
        ecran.fill(NEGRU)
        
        ecran.blit(img_mar, (mancare_x, mancare_y))
        
        cap_sarpe = [x1, y1]
        lista_sarpe.append(cap_sarpe)
        if len(lista_sarpe) > lungime_sarpe:
            del lista_sarpe[0]

        for x in lista_sarpe[:-1]:
            if x == cap_sarpe:
                game_close = True

        deseneaza_sarpe(dimensiune_bloc, lista_sarpe, x1_schimbare, y1_schimbare)
        
        scor_text = font_stil.render(f"{lungime_sarpe - 1}", True, ALB)
        ecran.blit(scor_text, [10, 10])
       
        for p in particule[:]:
            p.miscare()
            p.desenare(ecran)
            if p.viata <= 0:
                particule.remove(p)
        pygame.display.update()

        if x1 == mancare_x and y1 == mancare_y:
            if sunet_mancare: sunet_mancare.play()
            if x1 == mancare_x and y1 == mancare_y:
         
                for _ in range(15):
                    particule.append(Particula(mancare_x + 5, mancare_y + 5))
            mancare_x = random.randint(0, (latime - dimensiune_bloc) // 10) * dimensiune_bloc
            mancare_y = random.randint(0, (inaltime - dimensiune_bloc) // 10) * dimensiune_bloc
            lungime_sarpe += 1
            viteza += 1

        ceas.tick(viteza)

    pygame.quit()
    quit()

if __name__ == "__main__":
    joc()