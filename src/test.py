from image_slicer import slice

tiles = slice(r"C:\Users\Superuser\Documents\Lightshot\chess\board.png", 64, 8, 8)

for tile in tiles:
    print(f"row: {tile.row}")
    print(f"col: {tile.column}")
    print()
    filepath = r"C:\Users\Superuser\Documents\Lightshot\chess\tiles" + f"\somethnig"
    filename = f"{tile.row}_{tile.column}.png"
    tile.save(filepath + filename)
#!/usr/bin/python
# -*- coding: utf-8 -*-
{
    'h1': ('white', 'R'),
    'g1': None,
    'f1': ('white', 'B'),
    'e1': ('white', 'K'),
    'd1': ('white', 'Q'),
    'c1': ('white', 'R'),
    'b1': None,
    'a1': ('white', 'R'),
    'h2': ('white', 'P'),
    'g2': ('white', 'P'),
    'f2': ('white', 'P'),
    'e2': ('white', 'P'),
    'd2': None,
    'c2': ('white', 'P'),
    'b2': ('white', 'P'),
    'a2': ('white', 'P'),
    'h3': None,
    'g3': None,
    'f3': ('white', 'N'),
    'e3': None,
    'd3': None,
    'c3': ('white', 'N'),
    'b3': ('white', 'P'),
    'a3': None,
    'h4': None,
    'g4': None,
    'f4': None,
    'e4': None,
    'd4': ('white', 'P'),
    'c4': None,
    'b4': None,
    'a4': None,
    'h5': None,
    'g5': None,
    'f5': None,
    'e5': None,
    'd5': ('black', 'P'),
    'c5': None,
    'b5': None,
    'a5': None,
    'h6': None,
    'g6': None,
    'f6': ('black', 'N'),
    'e6': None,
    'd6': None,
    'c6': None,
    'b6': None,
    'a6': None,
    'h7': ('black', 'P'),
    'g7': ('black', 'P'),
    'f7': ('black', 'P'),
    'e7': ('black', 'P'),
    'd7': None,
    'c7': ('black', 'P'),
    'b7': ('black', 'P'),
    'a7': ('black', 'P'),
    'h8': ('black', 'R'),
    'g8': None,
    'f8': ('black', 'B'),
    'e8': ('black', 'K'),
    'd8': ('black', 'Q'),
    'c8': ('black', 'R'),
    'b8': ('black', 'N'),
    'a8': ('black', 'N'),
    }
