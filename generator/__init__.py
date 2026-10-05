"""The game generator: the pipeline that builds games for the platform.

It sits beside the platform, not inside it. It may read the platform's design
documents and, in later steps, call its loader; the platform never imports it.
"""
