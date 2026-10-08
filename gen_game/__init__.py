"""gen_game: steps 2 to 4 of the game-generation pipeline.

Takes a game from the inventory (`gen_inventory`), writes its rules as a spec,
encodes the spec as a platform game file, and evaluates the result. Like
`gen_inventory`, it sits beside `xcolos/`: the platform never imports it.
"""
