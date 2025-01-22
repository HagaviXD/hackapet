import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background = displayio.OnDiskBitmap("C:/Users/User/hackapet/pets/acons_example_pet/code/forestbackground.bmp")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

cat_sheet = displayio.OnDiskBitmap("C:/Users/User/hackapet/pets/acons_example_pet/code/cat-Sheet.bmp")

tile_width = 32
tile_height = 32

cat_sprite = displayio.TileGrid(
    cat_sheet,
    pixel_shader=cat_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)

splash.append(cat_sprite)

fireball_bitmap = displayio.OnDiskBitmap("C:/Users/User/hackapet/pets/acons_example_pet/code/fireball.bmp")

fireballs = []
lanes = [10, round((display.width - tile_width)/2), display.width - 10 - tile_width]

def spawn_fireball(clear_lanes = [0, 1, 2]):
    x_position = lanes[random.choice(clear_lanes)]
    fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fireball_bitmap.width,
        tile_height=fireball_bitmap.height,
        x=x_position,
        y= -tile_height -32
    )
    fireballs.append(fireball)
    splash.append(fireball)

def check_collision(sprite1, sprite2):
    return (
    sprite1.x < sprite2.x + 32 and
    sprite1.x + 32 > sprite2.x and
    sprite1.y < sprite2.y + 32 and
    sprite1.y + 32 > sprite2.y
    )

death = displayio.OnDiskBitmap("C:/Users/User/hackapet/pets/acons_example_pet/code/restart.bmp")


def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader=cat_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,  
        y=(display.height - 32) // 2  
    )
    splash.append(death_hi)
    for i in fireballs:
        splash.remove(i)
    fireballs.clear()

speed = 4 
current_position_IL = 1 #in lanes

range_min_y = -25
min_dist = 35
two_in_range = False
game_over = False


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True:
                for i in fireballs:
                    splash.remove(i)
                fireballs.clear()
                splash.remove(death_hi)
                game_over = False
       

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and current_position_IL > 0:
        current_position_IL -= 1
        cat_sprite.x = lanes[current_position_IL] 
    if keys[pygame.K_RIGHT] and current_position_IL < len(lanes) - 1: 
        current_position_IL += 1
        cat_sprite.x = lanes[current_position_IL] 

    if cat_sprite.x >= display.width - 32:
        cat_sprite.x = display.width - 32
    if cat_sprite.x <= 0 :
        cat_sprite.x = 0 

    clear_lanes = [0,1,2]
    in_range_counter = 0    
    for fireball in fireballs:
        if fireball.y <= min_dist:
            clear_lanes.remove(lanes.index(fireball.x))
        if fireball.y <= range_min_y:
            in_range_counter +=1
        fireball.y += 5 
        if fireball.y > display.height:
            splash.remove(fireball)
            fireballs.remove(fireball)
        if check_collision(cat_sprite, fireball):
            game_over = True
            display_game_over()
    if in_range_counter >= 2:
        two_in_range = True
    else: 
        two_in_range = False

    
    

    if random.random() < 0.05 and not two_in_range: # spawn rate
        spawn_fireball(clear_lanes)

    time.sleep(0.075)
        