"""The operator console.

A local web UI for building a table, choosing a game, and watching a match run.

This is an operator's console, not a player's client. It holds the full view on
purpose, the way a spectator seat does. A player-facing client, where one person
occupies one seat and sees only what that seat is entitled to, is a different
surface and belongs to Milestone 2.
"""

from xcolos.web.server import MatchManager, serve

__all__ = ["MatchManager", "serve"]
