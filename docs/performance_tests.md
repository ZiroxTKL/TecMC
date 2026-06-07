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

## Recorded tests

| Date | Phase | Test | Players | TPS | MSPT summary | Result |
|---|---|---|---:|---|---|---|
| 2026-06-07 | Phase 4B | Baseline after startup / player online | 1 | 19.98-20.0 | Median ~2.3 ms, P95 ~26.8 ms, peak 630.8 ms | Approved |

### Test notes

#### 2026-06-07 - Phase 4B baseline

- Mods tested: Current stable stack.
- Situation: Server after startup with one player online.
- TPS stayed stable between 19.98 and 20.0.
- Median MSPT was around 2.3 ms in the 1-minute window.
- P95 MSPT was around 26.8 ms in the 1-minute window.
- Peak MSPT reached 630.8 ms once.
- The peak is considered punctual, likely caused by startup, login or chunk loading.
- Last 10-second sample normalized to 6.4 ms median, 11.7 ms P95 and 33.3 ms max.
- Server process CPU was around 13% in the final reading.
- RAM usage was not measured.
- Decision: Approved as Phase 4B baseline before Phase 5 testing.

#### 2026-06-07 - Phase 5A YUNG base initial test

- Mods tested: YUNG's API, YUNG's Better Dungeons, YUNG's Better Mineshafts and YUNG's Better Strongholds.
- Situation: New Phase 5 test world after startup.
- TPS recovered to 20.0 in the last short-term readings.
- 1-minute TPS stayed around 19.24-19.25 due to recent startup/worldgen load.
- 5-minute TPS stayed around 19.71.
- Median MSPT was around 7.5 ms in the 1-minute window.
- P95 MSPT reached around 21.5 ms after stabilization.
- Peak MSPT reached 248.8 ms once.
- The peak is considered punctual, likely caused by startup, initial world generation or structure generation.
- Last 10-second sample normalized to 7.0 ms median, 8.2 ms P95 and 10.3 ms max.
- Server process CPU dropped to around 4% in the final reading.
- RAM usage was not measured.
- Decision: Approved as initial Phase 5A YUNG base test.

#### 2026-06-07 - Phase 5B YUNG extra structures

- Mods tested: YUNG's Better Desert Temples, YUNG's Better Jungle Temples and YUNG's Better Ocean Monuments.
- Situation: Phase 5 test world after adding extra vanilla structure improvements.
- TPS stayed at 20.0 in the short-term readings.
- 5-minute TPS stayed around 19.71.
- Last 10-second sample was very stable: 2.2 ms median, 3.0 ms P95 and 4.8 ms max.
- 1-minute P95 reached 55.1 ms and peak MSPT reached 269.5 ms.
- The spike is considered punctual, likely caused by chunk/structure generation.
- Server process CPU was around 3% in the final short-term reading.
- RAM usage was not measured.
- Decision: Approved as Phase 5B YUNG extra structures test.

#### 2026-06-07 - Phase 5C Towns and Towers

- Mods tested: Towns and Towers.
- Situation: Phase 5 test world with additional settlement/tower structures.
- Short-term TPS stayed stable around 20.0.
- 1-minute TPS dropped to around 19.14 during recent world/structure generation.
- 5-minute TPS stayed around 19.47.
- Last 10-second sample: 8.3 ms median, 17.5 ms P95 and 51.7 ms max.
- 1-minute sample: 15.0 ms median, 40.4 ms P95 and 144.8 ms max.
- The spike is considered acceptable during structure/world generation.
- Server process CPU was around 3% in the final short-term reading.
- RAM usage was not measured.
- Decision: Approved with observation. The mod is heavier than previous YUNG blocks but remains playable and stable.

#### 2026-06-07 - Phase 5D Nether and End structures

- Mods tested: YUNG's Better Nether Fortresses and YUNG's Better End Island.
- Situation: Phase 5 test world with temporary Nether access enabled.
- Tested Nether/End-related structure generation and End entry behavior.
- Final short-term TPS stayed stable around 19.98-20.0.
- 5-minute TPS stayed around 19.5.
- Final 10-second sample: 4.0 ms median, 15.9 ms P95 and 226.9 ms max.
- Final 1-minute sample: 3.9 ms median, 7.3 ms P95 and 226.9 ms max.
- Server showed two "Can't keep up" warnings around dimension/structure generation and End initialization.
- The warnings are considered acceptable because the test included locate commands, teleporting, dimension loading, End generation and initial dragon fight setup.
- Server process CPU stayed low in the final reading.
- RAM usage was not measured.
- Decision: Approved with observation. Stable after generation, but dimension entry can create temporary spikes.

#### 2026-06-07 - Phase 5E When Dungeons Arise

- Mods tested: When Dungeons Arise.
- Situation: Phase 5 test world with large dungeon/structure generation.
- Short-term TPS stayed stable at 20.0.
- 1-minute TPS stayed around 19.25 during recent world/structure generation.
- 5-minute TPS stayed around 19.41.
- Last 10-second sample: 9.5 ms median, 20.1 ms P95 and 55.8 ms max.
- 1-minute sample: 11.2 ms median, 43.2 ms P95 and 153.0 ms max.
- Server process CPU stayed around 11-21%.
- No crash was observed.
- The mod is heavier than previous structure blocks but remains stable in the initial test.
- RAM usage was not measured.
- Decision: Approved with observation. Keep an eye on loot balance and large structure density.

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