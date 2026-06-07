# Performance Tests

This document tracks TecMC performance evidence using TPS, MSPT and basic server observations.

The goal is to confirm that each phase is stable before moving forward, especially before creating the official world.

---

## Current target

TecMC should stay close to:

- 20 TPS during normal gameplay.
- Low MSPT during idle and light gameplay.
- Stable performance with 3-4 normal players.
- Acceptable performance with up to 6-7 players in real use.
- No sustained lag during exploration, structures or light Create usage.

Short MSPT spikes are acceptable during login, config generation, chunk loading or world generation, as long as TPS returns to 20.

---

## Useful commands

Basic TPS/MSPT check:

- `/spark tps`

Health report:

- `/spark health --upload`

Profiler for deeper analysis:

- `/spark profiler start`
- `/spark profiler stop`

Use the profiler only when there is a real performance issue or when testing heavy worldgen, structures or Create setups.

---

## Test table

| Date | Phase | Mods tested | Players | Situation | TPS | Avg MSPT | Peak MSPT | RAM usage | Result | Notes |
|---|---|---|---:|---|---:|---:|---:|---|---|---|
| Pending | Phase 4B | Current stable stack | 0-1 | Idle after startup | Pending | Pending | Pending | Pending | Pending | Baseline test |
| Pending | Phase 4B | Current stable stack | 1 | Player login and initial loading | Pending | Pending | Pending | Pending | Pending | Check login spike |
| Pending | Phase 4B | Current stable stack | 1 | Basic exploration | Pending | Pending | Pending | Pending | Pending | Walking and loading nearby chunks |
| Pending | Phase 4B | Create + Create Deco | 1 | Light Create mechanisms | Pending | Pending | Pending | Pending | Pending | Simple machines only |
| Pending | Phase 4B | Current stable stack | 3-4 | Normal multiplayer gameplay | Pending | Pending | Pending | Pending | Pending | Real group usage |
| Pending | Phase 5 test | YUNG first block | 1-2 | Test world structure exploration | Pending | Pending | Pending | Pending | Pending | Before official world |

---

## Result criteria

### Approved

A test is approved if:

- TPS stays close to 20.
- MSPT does not stay near or above 50 ms.
- No repeated lag appears during normal gameplay.
- No crash occurs.
- Logs do not show serious errors.
- Players can join and play normally.

### Warning

A test enters warning state if:

- TPS drops temporarily but recovers.
- MSPT spikes during chunk generation.
- Logs show repeated warnings but no crash.
- Gameplay feels slightly unstable but playable.

### Rejected

A test is rejected if:

- TPS drops repeatedly or stays below normal.
- MSPT stays close to or above 50 ms.
- The server crashes.
- Players cannot join.
- A mod causes clear incompatibility.
- Worldgen causes severe lag or broken structures.

---

## Phase 5 testing protocol

Phase 5 must be tested in a separate test world before creating the official world.

Recommended order:

1. Backup Phase 4B.
2. Validate the backup.
3. Create a separate test world.
4. Add only the first worldgen/structure block.
5. Start the server.
6. Review logs.
7. Join the world.
8. Run `/spark tps`.
9. Explore structures and generate chunks.
10. Register results in this document.
11. Approve, reject or keep the block pending.
12. Commit and push only after stable tests.

---

## First Phase 5 block

Initial recommended block:

| Mod | Purpose | Status |
|---|---|---|
| YUNG's API | Required dependency for YUNG structure mods | Pending |
| YUNG's Better Dungeons | Better dungeon exploration | Pending |
| YUNG's Better Mineshafts | Better underground exploration | Pending |
| YUNG's Better Strongholds | Better stronghold progression | Pending |

Do not add many worldgen mods at the same time.

---

## Notes

Performance tests should be updated after each important mod change.

For every new test, record:

- Date.
- Phase.
- Mods tested.
- Number of players.
- Situation.
- TPS.
- Average MSPT.
- Peak MSPT.
- RAM usage if available.
- Result.
- Notes.

This document is part of the decision process before creating the official TecMC world.