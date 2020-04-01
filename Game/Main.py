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

#bulletSound = pygame.mixer.Sound("bullet.wav") #nebija pieejami šie skaņas efekti, tādēļ nav ievietoti mapē
#hitSound = pygame.mixer.Sound("Hit.wav")

music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

score = 0

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
        self.hitbox = (self.x + 17, self.y, 29, 62)

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
        self.hitbox = (self.x + 17, self.y, 29, 62)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #uzzīmē kasti ap čaru

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont("comicsans", 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, ((852/2)-(text.get_width()/2), ((480/2)-(text.get_height()/2))))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #ievietots, lai kamēr ir pauze var iziet no spēles
                    i = 301
                    pygame.QUIT


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

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.end = end
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.path = [self.x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10)) # katru reizi kā trāpa šis samazinās atklājot sarkano krāsu, kas ir apakšā
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) #uzzīmē kasti ap čaru

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health >0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")


# bekgrounda funkcija
def redrawGameWindow():
    #global walkCount #šis, laikam, atļauj izmainot mainīgo te, izmainīt arī to ārpus funkcijas
    # lai objekts sglabātu formu un neveidotos švīka, kur bijis objekts ar fill aizpilda vietu,
    # kur tikko bija objekts
    win.blit(bg, (0, 0)) #nomaina bekgroundu uz attēlu, ne kā win.fill((0, 0, 0)) kas iedod tikai krāsu
    text = font.render("Score: " + str(score), 1, (0,0,0)) #izveido tekstu
    win.blit(text, (740, 10)) # uzzīmē tekstu uz ekrāna
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    # uzzīmē objektu
    #pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    # atjauno attēlu, savādāk nekas nenotiktu/attēls nemainītos atbilstoši
    pygame.display.update()

# loops, kas nosaka visu spēli
#mainloop
font = pygame.font.SysFont("comicsans", 30, True, True)
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootloop = 0
bullets = []
run = True
while run:
    #pygame.time.delay(27) # ekrāna pārlādēšanās ātrums, ietekmē cik ātri objekti pārvietosies
    clock.tick(27) #attēla atjaunošana (fps)

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0

    # uzspiežot krustiņu iziet no spēles
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    #hitSound.play() # ja būtu ielādēta skaņa, tad te to liktu, kad trāpa goblinam
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
                    score +=1
        if bullet.x < 852 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # pārvieto objektu atbilstoši nospiestajai pogai un ierobežo, lai neiziet ārpus ekrāna
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and  shootloop == 0:
        #bullet.Sound.play() #ja būtu ielādēts skaņas fails, tad šādi šo palaistu uz lodes izšaušanu
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width//2), round(man. y + man.height//2), 6, (0, 0, 0), facing))

        shootloop = 1

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