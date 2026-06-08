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

#### 2026-06-08 - Phase 6B Food, Vanilla+ and Survival

- Added Farmer's Delight, Nether's Delight, End's Delight, Aquaculture 2, Friends&Foes, More Villagers, Creeper Overhaul and Carry On.
- Required dependencies were added correctly.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Items, mobs, food features and Carry On were tested correctly.
- Short-term TPS recovered to 20.0.
- 5-minute TPS dropped to 18.85 during the test, likely due to loading, testing and new content initialization.
- Tick durations stayed acceptable: 7.1 ms median, 11.6 ms P95 and 303.4 ms max in the 1-minute sample.
- Server process CPU stayed low, around 4–9%.
- Decision: Approved with observation.

#### 2026-06-08 - Phase 6C Alex ecosystem

- Added Alex's Mobs, Alex's Caves, Alex's Delight and required dependencies.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Alex's Mobs and Alex's Caves content were tested correctly.
- TPS stayed stable: 19.99 / 19.99 / 20.0 / 19.82 / 19.63.
- Tick durations were excellent: 1.2 ms median, 2.4 ms P95 and 110.5 ms max in the 1-minute sample.
- Server process CPU stayed low in short-term readings.
- Decision: Approved.

#### 2026-06-08 - Phase 6D Ice and Fire

- Added Ice and Fire: Dragons.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Ice and Fire content was tested correctly.
- Short-term TPS recovered to 20.0.
- 5-minute and 15-minute TPS stayed around 19.59 during testing.
- Last 10-second sample was stable: 3.4 ms median, 5.2 ms P95 and 13.3 ms max.
- 1-minute sample showed 19.3 ms median, 37.6 ms P95 and 191.5 ms max.
- Server process CPU stayed low, around 4–11%.
- Decision: Approved with observation. Watch dragon spawn rate, terrain destruction and structure density.

#### 2026-06-08 - Phase 6E End Expansion and Xaero's World Map

- Added Nullscape, The Outer End and Xaero's World Map.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- End generation and map functionality were tested correctly.
- Short-term TPS recovered to 20.0.
- 5-minute TPS stayed around 19.63 and 15-minute TPS around 19.08 during testing.
- Last 10-second sample was excellent: 0.8 ms median, 1.2 ms P95 and 97.1 ms max.
- 1-minute sample showed 5.5 ms median, 35.9 ms P95 and 228.9 ms max.
- Server process CPU stayed moderate, around 1–17%.
- Decision: Approved with observation. End generation caused punctual spikes, but the server recovered correctly.

#### 2026-06-08 - Phase 6F RPG Combat, Magic and Loot

- Added Better Combat, Combat Roll, Simply Swords, Spartan Shields, Iron's Spells 'n Spellbooks, Relics, Artifacts, Curios and Curious Lanterns.
- Added Cloth Config to the server after dependency error.
- Client launched correctly.
- Server started correctly after dependency fix.
- Player joined successfully.
- Combat, roll, weapons, spells and accessory systems were tested correctly.
- TPS stayed stable: 20.0 / 20.0 / 20.0 / 20.0 / 19.86.
- Tick durations: 11.9 ms median, 33.8 ms P95 and 283.8 ms max in the 1-minute sample.
- Server process CPU stayed moderate, around 3–13%.
- Decision: Approved with observation. High tick spike was punctual and the server recovered to 20 TPS.

#### 2026-06-08 - Phase 6G Bosses, Dark Lore and Danger

- Added L_Ender's Cataclysm, Mowzie's Mobs, Bosses of Mass Destruction, The Graveyard, Wither Reincarnated, Born in Chaos and Aquamirae.
- Required APIs and dependencies were added correctly.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Boss and mob content loaded correctly.
- Short-term TPS recovered to 20.0.
- 5-minute TPS stayed around 19.4 and 15-minute TPS around 19.81 during testing.
- Last 10-second sample was stable: 3.3 ms median, 5.9 ms P95 and 13.7 ms max.
- 1-minute sample showed 12.0 ms median, 38.1 ms P95 and 288.2 ms max.
- Server process CPU stayed moderate, around 3-21%.
- Decision: Approved with observation. Boss/entity loading caused punctual spikes, but the server recovered correctly.

#### 2026-06-08 - Phase 7A End Remastered

- Added End Remastered.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- End progression content was tested correctly.
- Short-term TPS recovered to 20.0.
- 5-minute TPS dropped to around 18.49 during testing.
- 15-minute TPS stayed around 19.38.
- Last 10-second sample was stable: 1.1 ms median, 7.5 ms P95 and 48.1 ms max.
- 1-minute sample was healthy: 6.7 ms median, 9.2 ms P95 and 75.3 ms max.
- Server process CPU stayed moderate, around 4-21%.
- Decision: Approved with observation. The server recovered correctly after testing/load.

#### 2026-06-08 - Phase 7B Twilight Forest and Aether

- Added The Twilight Forest and The Aether.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Dimension loading was tested correctly.
- Short-term TPS recovered to 20.0.
- 5-minute TPS stayed around 19.47 and 15-minute TPS around 19.72.
- Last 10-second sample was excellent: 1.1 ms median, 1.6 ms P95 and 23.0 ms max.
- 1-minute sample stayed healthy: 7.8 ms median, 24.2 ms P95 and 83.6 ms max.
- Server process CPU stayed low, around 1-9%.
- Decision: Approved.

#### 2026-06-08 - Phase 7C Advanced Netherite

- Added Advanced Netherite.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Advanced Netherite gear/progression content was tested correctly.
- Short-term TPS recovered to 20.0.
- 5-minute TPS stayed around 19.43 and 15-minute TPS around 19.82.
- Last 10-second sample was stable: 1.4 ms median, 9.0 ms P95 and 23.0 ms max.
- 1-minute sample stayed healthy: 11.4 ms median, 14.5 ms P95 and 205.0 ms max.
- Server process CPU stayed low, around 3-11%.
- Decision: Approved.

#### 2026-06-08 - Phase 7D Villages, Spelunking and Fossils

- Added ChoiceTheorem's Overhauled Village, Lithostitched, Spelunker's Charm II, More Hitboxes and Fossils and Archeology Revival.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- CTOV village generation was tested and a village generated correctly.
- Lithostitched showed warnings for missing CTOV optional template pool references.
- No crash was observed.
- TPS recovered to around 20.0 in short-term readings.
- 5-minute TPS dropped to around 17.4 and 15-minute TPS to around 18.38 during a heavy test involving village loading and a dragon attack.
- 1-minute tick durations reached 27.5 ms median, 59.0 ms P95 and 401.6 ms max during the stress situation.
- Decision: Approved with observation. Village generation worked, but CTOV warnings and heavy entity/worldgen situations should be monitored.

#### 2026-06-08 - Phase 7F.1 YUNG's Cave Biomes

- Added YUNG's Cave Biomes.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- Cave biome generation was tested correctly.
- Short-term TPS stayed stable around 20.0.
- 5-minute TPS stayed around 19.5 and 15-minute TPS around 19.83.
- Last 10-second sample was excellent: 1.0 ms median, 4.1 ms P95 and 8.0 ms max.
- 1-minute sample showed 10.9 ms median, 16.3 ms P95 and 243.0 ms max.
- Server process CPU stayed low to moderate, around 0-17%.
- Decision: Approved.

#### 2026-06-08 - Phase 7F.3 Galosphere

- Added Galosphere to expand underground cave content.
- Server initially failed to start due to a broken Create compatibility recipe pointing to `galosphere:silver_ingot`, an item that does not exist in the installed Galosphere version.
- Created a datapack fix: `tecmc_galosphere_fix`.
- Redirected Create's broken Galosphere silver smelting/blasting recipes to `iceandfire:silver_ingot`, since Ice and Fire is the active silver source in the modpack.
- Patched broken `galosphere:block_comparator` references to prevent datapack loading errors.
- Server started successfully after applying the datapack fix.
- Tested in-game successfully.
- TPS remained stable: `20.0 / 20.0 / 20.0 / 20.0 / 19.84`.
- Tick durations stayed healthy: `5.0 ms` median, `20.1 ms` P95 and `74.9 ms` max in the 1-minute sample.
- Server process CPU stayed low to moderate, around `2-11%`.
- Decision: **Approved with patch**.


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