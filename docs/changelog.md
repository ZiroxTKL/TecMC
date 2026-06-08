# Changelog

This file tracks the main development phases of TecMC.

## Current status

TecMC is currently in **Phase 4B completed**.

The server has a clean Forge base, performance optimization, QoL tools, multiplayer progression utilities, quests, NPC/lore systems, and lightweight Create support.

The official world should **not** be created yet. Phase 5 must be tested first using a separate test world.

---

## Phase history

| Version | Phase | Main change | Status |
|---|---|---|---|
| 0.1 | Phase 0 | Clean Forge 1.20.1 server base. Fixed occupied port 25565 issue. | Approved |
| 0.2 | Phase 1A | Added base performance tools: spark, Chunky, ModernFix, FerriteCore. | Approved |
| 0.3 | Phase 1B | Added entity and logic optimization: Canary, AI Improvements, Mobtimizations. | Approved |
| 0.4 | Phase 1C | Added extra server performance utilities: FastSuite, Clumps, dependencies. | Approved |
| 0.5 | Phase 1D | Added client FPS optimization: Embeddium, ImmediatelyFast, Entity Culling. | Approved |
| 0.6 | Phase 1E | Added Chloride as Embeddium addon. | Approved |
| 0.7 | Phase 2A | Added client QoL base: JEI, Jade, AppleSkin, Controlling, Mouse Tweaks, Inventory Profiles Next. | Approved |
| 0.8 | Phase 2B | Added multiplayer/progression QoL: Sophisticated Backpacks, Corail Tombstone, SecurityCraft. | Approved |
| 0.9 | Phase 3 | Added quests, NPCs and lore base: FTB Quests, Easy NPC, Patchouli. | Approved |
| 1.0 | Phase 4A | Added Create as lightweight engineering system. | Approved |
| 1.1 | Phase 4B | Added Create Deco for industrial/steampunk decoration. | Approved |
| 1.2 | Phase 5 | Worldgen and structures. | Pending |

---

## Decision log

### Approved decisions

- TecMC is a custom modpack/server, not a modified BetterMC install.
- The project focuses on RPG, adventure, quests, NPCs, lore, bosses, dimensions and a beautiful world.
- Create is allowed only as lightweight engineering, not as the main focus of the server.
- The Nether starts disabled and will be unlocked later through progression/lore.
- Lootr was rejected to keep classic competitive loot.
- The official world must wait until Phase 5 is tested.

### Pending decisions

- First YUNG structure block.
- Biome mod choice: Regions Unexplored or Biomes O' Plenty.
- Towns and Towers.
- When Dungeons Arise.
- Waystones.
- Blue Skies.
- Create Steam 'n' Rails.

---

## Rules for future changelog entries

Each new phase should document:

- Mods added.
- Mods removed.
- Config changes.
- Test result.
- Performance observations.
- Final decision: approved, rejected or pending.

## Version 1.1.1 - Phase 4B backup validation

### Validated

- Created a full Phase 4B backup before Phase 5 testing.
- Restored the backup in a separate test folder.
- Started the restored server successfully.
- Confirmed that the backup can be used as recovery point.

## Version 1.2 - Phase 5 worldgen expansion

### Added

- YUNG structure mods.
- Towns and Towers.
- When Dungeons Arise.
- Biomes O' Plenty and dependencies.
- BetterNether and BetterEnd.
- Soulful Nether.
- Quark and Supplementaries.

#### 2026-06-08 - Phase 6A.2 Server QoL

- Added Waystones, Nature's Compass, XP Tome, ElevatorID, Void Totem, Iron Chests, Goblin Traders, Polymorph and Crafting Tweaks.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- QoL features tested correctly.
- TPS stayed stable: 19.97 / 19.98 / 20.0 / 19.75 / 19.92.
- Tick durations: 6.8 ms median, 14.6 ms P95 and 56.4 ms max in the 1-minute sample.
- Server process CPU stayed low, around 3–9%.
- Decision: Approved.

### Fixed

- Downgraded Create from 6.0.8 to 6.0.7 due to creative inventory crash.

## Version 1.2.1 - Remove Create Deco

### Removed

- Create Deco.

### Reason

- Removed because it added limited value to TecMC progression and decoration.
- Reduces Create addon complexity after isolated client-side Create registry crashes.

### Decision

Approved.

### Tested

- Server starts correctly.
- Client enters correctly after mod/config synchronization.
- Spark TPS recovered to 20.0 during short-term readings.
- No reproducible crash after retry.

### Decision

Approved.

Phase 5 worldgen and vanilla plus expansion is stable enough to continue testing.

### Decision

Approved.

Phase 4B now has a valid backup and restoration test. The project can move safely into Phase 5 test-world preparation.

Recommended format:

```md
## Version X.X - Phase name

### Added
- Mod name: reason.

### Changed
- Config or design change.

### Removed
- Mod name: reason.

### Tested
- Test world result.
- Logs result.
- TPS/MSPT result.

### Decision
Approved / Rejected / Pending.