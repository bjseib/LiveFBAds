# Meta Ad Library Context

## Front-End UI Notes
- Provide a drop-down to select from Real Money Gaming categories.
- Display the number of publishers available within each category.
- Show active ads with the ability to filter by open slots.
- Include search within the selected space.
- Consume the FastAPI endpoints (`/api/categories`, `/api/categories/{id}/ads`) to populate the UI.

## Real Money Gaming Categories
- Online Casino
- Online Sportsbook
- Sweepstakes/Social Casino
- DFS (Daily Fantasy Sports)

## Publishers by Category

### Online Casino
- Caesars Palace Online Casino
- DraftKings Casino
- BetMGM Casino
- FanDuel Casino
- Betrivers Casino
- Betway Casino
- Hard Rock Casino
- Golden Nugget Casino
- Jackpot City
- Bet365
- Betfred
- Tipico Casino
- PlayLive Casino
- Resorts World Casino & Spa
- Bally Casino

### Online Sportsbook
- Caesars Sportsbook
- BetMGM Sportsbook
- FanDuel Sportsbook

### Sweepstakes/Social Casino
- Chumba Casino
- Wow Vegas Casino
- McLuck Casino

### DFS
- DraftKings
- FanDuel
- Betr (Social Sportsbook)
- Sleeper
- Underdog Fantasy
- PrizePicks
- Boom
- Parlay Play
- No House Advantage
- Thrive Fantasy
- Monkey Knife Fight
- Betcha

> **Note:** All publishers must be based in the United States.

## Administration
- Administrators manage publisher records through the admin panel described in [Publisher Administration Guide](admin-publisher-management.md).
- Updates to publisher/category assignments should be reflected immediately in the ingestion service, ensuring new publishers are included in scheduled Meta API syncs.
- Archive inactive publishers instead of deleting to preserve historic ad creative data.
- The admin API (`/api/admin/publishers`) powers the interface and enforces auditing for modifications.
