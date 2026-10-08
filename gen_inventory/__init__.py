"""gen_inventory: step 1 of the game-generation pipeline, the inventory of candidate games.

It sits beside the platform, not inside it. It may read the platform's design
documents and, in later steps, call its loader; the platform never imports it.
"""
