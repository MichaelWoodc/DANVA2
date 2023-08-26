import pygame
import sys

# Initialize Pygame
pygame.init()
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
surface = pygame.display.set_mode((displayX-700, displayY-200),pygame.RESIZABLE,display=0)
x, y = surface.get_size()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font_size = int(y / 15)
font1 = pygame.font.Font(None, font_size)
font2 = pygame.font.Font(None, font_size + 20)  # Larger font for selected button

# Button information
button_labels = ["Happy", "Sad", "Angry", "Fearful", "Continue"]
button_count = len(button_labels)
button_padding = int(y / 20)
button_width = int((x - button_padding * (button_count + 1)) / button_count)
button_height = int(y / 10)

# Store button rects and fonts
button_rects = []
fontslist = [font1] * button_count

# Initialize button rects
def initialize_button_rects():
    button_rects.clear()
    for i in range(button_count):
        button_rects.append(pygame.Rect(button_padding * (i + 1) + button_width * i, y - button_height - button_padding, button_width, button_height))

initialize_button_rects()

def draw_buttons():
    surface.fill(white)
    for i, rect in enumerate(button_rects):
        pygame.draw.rect(surface, black, rect)
        text = fontslist[i].render(button_labels[i], True, white)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

def handleClickedButton(button):
    global fontslist
    if button == 4:
        # Handle continue button
        for i in range(button_count):
            fontslist[i] = font1
        pass
    else:
        for i in range(button_count):
            fontslist[i] = font1
        fontslist[button] = font2

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        print('Clicked number', i)
                        handleClickedButton(i)
                        break
        elif event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            displayX, displayY = surface.get_size()
            initialize_button_rects()

    draw_buttons()
    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()
