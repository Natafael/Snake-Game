import pygame
import time
import random

def citeste_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def salveaza_highscore(scor):
    with open("highscore.txt", "w") as f:
        f.write(str(scor))

# 1. Inițializare Pygame și setări fereastră
pygame.init()
pygame.mixer.init()

try:
    sunet_mancare = pygame.mixer.Sound("media/audio/bite-sound.wav")
except:
    sunet_mancare = None # Fail-safe dacă lipsește fișierul

latime, inaltime = 600, 400
ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)
pygame.display.set_caption('Snake Game - Proiect Final')

# 2. Culori și constante
NEGRU = (0, 0, 0)
ALB = (255, 255, 255)
ROSU = (213, 50, 80)
VERDE = (0, 255, 0)
ALBASTRU = (50, 153, 213)

dimensiune_bloc = 10
viteza = 15
ceas = pygame.time.Clock()

img_mar = pygame.image.load("media/textures/apple.png")
img_corp = pygame.image.load("media/textures/head.png")
img_cap = pygame.image.load("media/textures/skin.png")

img_mar = pygame.transform.scale(img_mar, (20, 20))
img_corp = pygame.transform.scale(img_corp, (dimensiune_bloc, dimensiune_bloc))
img_cap = pygame.transform.scale(img_cap, (20, 20))

pygame.font.init() 
font_stil = pygame.font.SysFont("bahnschrift", 25)

def deseneaza_sarpe(bloc, lista_sarpe):
    for i in range(len(lista_sarpe)):
        if i == len(lista_sarpe) - 1:
            # Dacă este ultimul element, desenăm capul
            ecran.blit(img_cap, (lista_sarpe[i][0], lista_sarpe[i][1]))
        else:
            # Altfel, desenăm corpul
            ecran.blit(img_corp, (lista_sarpe[i][0], lista_sarpe[i][1]))

def ecran_pauza():
    global latime, inaltime, ecran # O singură declarare la început
    
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
                # Re-facem blur-ul pentru noua dimensiune
                small_img = pygame.transform.smoothscale(screenshot, (latime // 4, inaltime // 4))
                blurred_img = pygame.transform.smoothscale(small_img, (latime, inaltime))
                overlay = pygame.Surface((latime, inaltime))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))

def joc():
    global latime, inaltime, ecran, viteza
    game_over = False
    game_close = False
    high_score = citeste_highscore()
    viteza = 15

    try:
        pygame.mixer.music.load("media/audio/main-theme.mp3")
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

        deseneaza_sarpe(dimensiune_bloc, lista_sarpe)
        
        scor_text = font_stil.render(f"{lungime_sarpe - 1}", True, ALB)
        ecran.blit(scor_text, [10, 10])
        pygame.display.update()

        if x1 == mancare_x and y1 == mancare_y:
            if sunet_mancare: sunet_mancare.play()
            mancare_x = random.randint(0, (latime - dimensiune_bloc) // 10) * dimensiune_bloc
            mancare_y = random.randint(0, (inaltime - dimensiune_bloc) // 10) * dimensiune_bloc
            lungime_sarpe += 1
            viteza += 1

        ceas.tick(viteza)

    pygame.quit()
    quit()

if __name__ == "__main__":
    joc()