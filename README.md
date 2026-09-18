# GM Stars

A command-line NBA roster-builder game. Pick a franchise, get a salary
cap, and draft a 5-player starting lineup. Manage your budget wisely and 
meet your roster requirements to get scored on your final team.

## Status: In active development (target: 09/20,2026)

## Working
- [x] Franchise selection with input validation (full name or nickname)
- [x] Player selection with input validation
- [x] Live salary cap tracking and affordability checks per pick
- [x] Duplicate player prevention
- [ ] Position requirement constraint
- [ ] Roster grading based on player stats

## Planned for v2
- Live stats pulled from a real API instead of a hardcoded player pool
- Additional constraints (e.g. shooting percentages, PPG averages, etc)
- Trade mechanics after initial draft

## Tech
Python, standard library only for now.

## Run it
python gm_stars.py
