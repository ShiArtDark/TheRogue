# [ CONSTANTE ]
WIDTH, HEIGHT= 1400,750 # Taille écran
FPS = 120 # Taux de raffraichissement
TILESIZE= 64 # La taille des sprites ( 64x64x )

# [ UI ]

BAR_HEIGHT = 30
HP_BAR_WIDTH = 300
ITEM_BOX_SIZE = 80
MENU_FONT = 'assets/graphics/font/NormalFont.ttf'
MENU2_FONT = 'assets/graphics/font/PixelMiddle.ttf'
UI_FONT = 'assets/graphics/font/DungeonFont.ttf'
UI_FONT_SIZE = 65

WATERCOLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER = '#111111'
TEXT_COLOR = '#EEEEEE'

HP_COLOR = '#e64435'
BORDER_ACTIVE = 'gold'
DASH_BORDER = '#52cc89'

# [ Enemy ]

monster_data = {
    'spirit' : {'health': 50, 'speed': 1.75, 'damage': 15, 'resistance': 5, 'attack_radius':50, 'notice_radius': 350, 'attack_type':'slash', 'score': 125, 'animationSpeed': .05, 'attackSound': 'assets/sound/SFX/fireSpiritAttack.mp3'},
    'samourai' : {'health': 400, 'speed': 2, 'damage': 45, 'resistance': 0, 'attack_radius':80, 'notice_radius': 600, 'attack_type':'slash', 'score': 600, 'animationSpeed': .05, 'attackSound': 'assets/sound/SFX/samSlash.mp3'},
    'racoon' : {'health': 300, 'speed': 2.5, 'damage': 30, 'resistance': 0, 'attack_radius':100, 'notice_radius': 600, 'attack_type':'slash', 'score': 00, 'animationSpeed': .05, 'attackSound': 'assets/sound/SFX/onePUNCHRacoon.mp3'}
}