"""Deprecated. The Milestone 1 implementation, kept for reference only.

Nothing in this package is on the path a match takes any more. A game is a
JSON file in `xcolos/games/library`, and `xcolos.flow` runs it by asking a
model to fill in the parts a file cannot state. This package holds what that
replaced:

    mafia.py    the hardcoded Python Mafia. Every rule of the game written as
                control flow, which is the thing the flow engine exists to
                stop needing.
    render.py   its per-fact wording. Thirteen Mafia message types that used
                to live in the kernel's renderer and made a game-agnostic
                module know one game.
    models.py   an unused adapter for linking a seat to a local model. Never
                imported; superseded by `xcolos.flow.backends`, which links a
                judge rather than a player.
    static/     an unused browser client for playing a seat by hand.

Why keep it at all. The hardcoded Mafia is the only independent implementation
of the same game, so it is the one thing that can say whether a definition is
right: run both on a seed and compare. Delete it and "the game file behaves
correctly" becomes an opinion.

It is not offered in the console and no new work should import it.
"""
