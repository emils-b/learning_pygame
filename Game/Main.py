import pygame
pygame.init()

# izveido spēles ekrānu
win = pygame.display.set_mode((852, 480))
pygame.display.set_caption("First Game")

# attēli priekš bekgraunda un čara
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

# objekta dimensiju vertibas un atrums cik atri parvietojas un x un y ir vieta,
# kur parādās ielādējot
class player(object):
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))  # ar // dalot noapaļo, 1 // 3 = 0
                self.walkCount += 1
            elif man.right:
                win.blit(walkRight[man.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)




# bekgrounda funkcija
def redrawGameWindow():
    #global walkCount #šis, laikam, atļauj izmainot mainīgo te, izmainīt arī to ārpus funkcijas
    # lai objekts sglabātu formu un neveidotos š'vīka, kur bijis objekts ar fill aizpilda vietu,
    # kur tikko bija objekts
    win.blit(bg, (0, 0)) #nomaina bekgroundu uz attēlu, ne kā win.fill((0, 0, 0)) kas iedod tikai krāsu
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    # uzzīmē objektu
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    # atjauno attēlu, savādāk nekas nenotiktu/attēls nemainītos atbilstoši
    pygame.display.update()

# loops, kas nosaka visu spēli
#mainloop
man = player(300, 410, 64, 64)
bullets = []
run = True
while run:
    #pygame.time.delay(27) # ekrāna pārlādēšanās ātrums, ietekmē cik ātri objekti pārvietosies
    clock.tick(27) #attēla atjaunošana (fps)
    # uzspiežot krustiņu iziet no spēles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 852 and bullet.x >0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # pārvieto objektu atbilstoši nospiestajai pogai un ierobežo, lai neiziet ārpus ekrāna
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width//2), round(man. y + man.height//2), 6, (0, 0, 0), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 852 - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    # lai leciena laikā nevarētu pārvietoties uz augšu un leju
    if not(man.isJump):
        #if keys[pygame.K_UP] and y > vel:
        #    y -= vel
        #if keys[pygame.K_DOWN] and y < 500 - height - vel:
        #    y += vel
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    # veidots lai leciens būtu dinamiskāks - uz lecot uz augšu paātrinātos,
    # gaisā nopauzētu un tad krītot paātrinātos
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()