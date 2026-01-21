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
sunet_mancare = pygame.mixer.Sound("media/audio/bite-sound.wav")
latime, inaltime = 600, 400
ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)
pygame.display.set_caption('Examen SDA')

# 2. Culori și constante
NEGRU = (0, 0, 0)
ALB = (255, 255, 255)
ROSU = (213, 50, 80)
VERDE = (0, 255, 0)
ALBASTRU = (50, 153, 213)

dimensiune_bloc = 10
viteza = 15
ceas = pygame.time.Clock()

pygame.font.init() 
font_stil = pygame.font.SysFont("bahnschrift", 25)

def deseneaza_sarpe(bloc, lista_sarpe):
    for x in lista_sarpe:
        pygame.draw.rect(ecran, VERDE, [x[0], x[1], bloc, bloc])

def joc():
    global latime, inaltime, ecran, viteza
    game_over = False
    game_close = False
    high_score = citeste_highscore()
    viteza = 15

    # Încarcă muzica de fundal
    pygame.mixer.music.load("media/audio/main-theme.mp3")
# Redă muzica la infinit (parametrul -1)
    pygame.mixer.music.play(-1)

    # Poziția inițială aliniată la grilă (folosim // 10 * 10)
    x1 = (latime // 2 // 10) * 10
    y1 = (inaltime // 2 // 10) * 10
    x1_schimbare, y1_schimbare = 0, 0

    lista_sarpe = []
    lungime_sarpe = 1

    # Generare mâncare aliniată perfect la grilă
    mancare_x = random.randint(0, (latime - dimensiune_bloc) // 10) * 10
    mancare_y = random.randint(0, (inaltime - dimensiune_bloc) // 10) * 10

    while not game_over:

        while game_close == True:
            ecran.fill(ALBASTRU)
            scor_final = lungime_sarpe - 1
            if scor_final > high_score:
                high_score = scor_final
                salveaza_highscore(high_score)

            mesaj_pierdut = font_stil.render("AI PIERDUT!", True, ROSU)
            mesaj_scor = font_stil.render(f"Scor curent: {scor_final}", True, ALB)
            mesaj_high = font_stil.render(f"High Score: {high_score}", True, VERDE)
            mesaj_info = font_stil.render("Q - Iesire, C - Reincearca", True, ALB)

            ecran.blit(mesaj_pierdut, [latime // 3, inaltime // 4])
            ecran.blit(mesaj_scor, [latime // 4, inaltime // 2.5])
            ecran.blit(mesaj_high, [latime // 4, inaltime // 2])
            ecran.blit(mesaj_info, [latime // 4, inaltime - 50])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        joc()
                if event.type == pygame.VIDEORESIZE:
                    latime, inaltime = event.w, event.h
                    ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)

        # Gestionare evenimente (Resize + Taste)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.VIDEORESIZE:
                latime, inaltime = event.w, event.h
                ecran = pygame.display.set_mode((latime, inaltime), pygame.RESIZABLE)
                # Repoziționăm mâncarea dacă resize-ul a scos-o în afara ecranului
                if mancare_x >= latime or mancare_y >= inaltime:
                    mancare_x = random.randint(0, (latime - dimensiune_bloc) // 10) * 10
                    mancare_y = random.randint(0, (inaltime - dimensiune_bloc) // 10) * 10

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_schimbare == 0:
                    x1_schimbare = -dimensiune_bloc
                    y1_schimbare = 0
                elif event.key == pygame.K_RIGHT and x1_schimbare == 0:
                    x1_schimbare = dimensiune_bloc
                    y1_schimbare = 0
                elif event.key == pygame.K_UP and y1_schimbare == 0:
                    y1_schimbare = -dimensiune_bloc
                    x1_schimbare = 0
                elif event.key == pygame.K_DOWN and y1_schimbare == 0:
                    y1_schimbare = dimensiune_bloc
                    x1_schimbare = 0

        # Verificare coliziune pereti
        if x1 >= latime or x1 < 0 or y1 >= inaltime or y1 < 0:
            game_close = True

        x1 += x1_schimbare
        y1 += y1_schimbare
        ecran.fill(NEGRU)
        
        # Desenare mâncare
        pygame.draw.rect(ecran, ROSU, [mancare_x, mancare_y, dimensiune_bloc, dimensiune_bloc])
        
        cap_sarpe = [x1, y1]
        lista_sarpe.append(cap_sarpe)
        if len(lista_sarpe) > lungime_sarpe:
            del lista_sarpe[0]

        for x in lista_sarpe[:-1]:
            if x == cap_sarpe:
                game_close = True

        deseneaza_sarpe(dimensiune_bloc, lista_sarpe)
        
        # Scor în timp real
        scor_text = font_stil.render(f"{lungime_sarpe - 1}", True, ALB)
        ecran.blit(scor_text, [10, 10])
        
        pygame.display.update()

        # Verificare coliziune cu mâncarea (aliniere perfectă)
        if x1 == mancare_x and y1 == mancare_y:
            sunet_mancare.play()  # REDĂ SUNETUL AICI
            mancare_x = random.randint(0, (latime - dimensiune_bloc) // 10) * 10
            mancare_y = random.randint(0, (inaltime - dimensiune_bloc) // 10) * 10
            lungime_sarpe += 1
            viteza += 1

        ceas.tick(viteza)

    pygame.quit()
    quit()

if __name__ == "__main__":
    joc()