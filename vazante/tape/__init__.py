"""Reading a seller tape and turning it into a decision in hours rather than weeks.

The whole desk is downstream of one file. This package ingests whatever the seller actually sends, maps it
without asking them to reformat anything, reconciles it against the fund's own CVM filing, sweeps it for
structural defects at no cost, and routes every position to the buyer who wants that piece.
"""
