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

#### 2026-06-08 - Phase 7G.1 Dungeons and Taverns

- Added Dungeons and Taverns to increase lootable exploration structures.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- New structure/worldgen exploration was tested.
- TPS remained stable: `19.95 / 19.98 / 20.0 / 19.76 / 19.51`.
- Tick durations stayed acceptable for structure generation: `17.9 ms` median, `25.2 ms` P95 and `115.3 ms` max in the 1-minute sample.
- Server process CPU stayed moderate, around `4-21%`.
- Decision: **Approved with minor worldgen/load observation**.

#### 2026-06-08 - Phase 7G.2 Structory

- Added Structory as a lightweight structure expansion for the Overworld.
- Client launched correctly.
- Server started correctly.
- Player joined successfully.
- New Overworld chunk exploration was tested.
- TPS remained stable: `19.97 / 20.0 / 20.0 / 19.83 / 19.94`.
- Tick durations stayed acceptable for structure/worldgen testing: `16.6 ms` median, `22.9 ms` P95 and `161.0 ms` max in the 1-minute sample.
- Server process CPU stayed low to moderate, around `5-11%`.
- Decision: **Approved**.

#### 2026-06-08 - Phase 7G.3 / 7G.4 Moog's Nether and End Structures

- Added Moog's Nether Structures and Moog's End Structures together.
- Server started correctly.
- Player joined successfully.
- Nether and End exploration/generation were tested.
- Initial testing caused worldgen spikes due to teleporting, dimension loading, End initialization, dragon fight setup and new chunk generation.
- Short-term TPS recovered to stable values after generation.
- Final stabilization sample showed TPS at `19.99 / 20.0 / 20.0 / 19.99 / 18.52`.
- The 5-minute TPS recovered to `19.99`, while the 15-minute value still reflected earlier generation spikes.
- Tick durations in the final sample were acceptable: `13.1 ms` median, `40.9 ms` P95 and `365.8 ms` max in the 1-minute sample.
- Server process CPU stayed moderate, around `5-17%`.
- Decision: **Approved with worldgen/initial generation observation**.

#### 2026-06-08 - Phase 7G.5 Stalwart Dungeons

- Added Stalwart Dungeons as the final major dungeon/adventure structure mod for the worldgen stage.
- Server started correctly.
- Player joined successfully.
- Dimension/worldgen testing was completed successfully.
- TPS remained stable: `19.97 / 20.0 / 20.0 / 20.0 / 19.82`.
- Tick durations stayed healthy: `10.9 ms` median, `15.5 ms` P95 and `169.4 ms` max in the 1-minute sample.
- Server process CPU stayed low to moderate, around `1-16%`.
- Decision: **Approved**.

## 2026-06-09 - Phase 8B: Fixes / Stability Batch

### Estado

**Aprobado preliminarmente.**

Se añadió el primer lote de mods enfocado en estabilidad, fixes de bugs, networking, chunks y optimización ligera.

No se añadieron mods de worldgen en esta fase, por lo que este cambio no debería afectar la generación de chunks nuevos ni requerir reinicio de mundo.

### Mods añadidos

#### Fixes / estabilidad

- Item Split Bug Fix
- NetherPortalFix
- PacketFixer
- Passengers Portal Fix
- SkeletonAIFix
- Neruina
- Twilight Cave Fix
- BetterCompatibilityChecker
- Connectivity
- Chunk Sending
- Fast Async World Save
- Fast Item Frames
- Recipe Essentials
- Structure Layout Optimizer

#### Dependencias añadidas al server

- Cupboard
- PuzzlesLib

### Ajustes / notas

- `Cupboard` era requerido por:
  - Recipe Essentials
  - Fast Async World Save
  - Chunk Sending
  - Connectivity

- `PuzzlesLib` era requerido por:
  - SkeletonAIFix
  - Fast Item Frames

- Estas dependencias ya existían en el cliente TecMC, pero faltaban en el servidor. Se copiaron al servidor para resolver el error de carga.

- `Recipe Essentials` fue añadido como reemplazo recomendado para optimización de recetas.

- Si `Not Enough Recipe Book` sigue instalado, debe eliminarse para evitar duplicación de funciones con `Recipe Essentials`.

### Resultado de prueba

Primera carga:

- El servidor falló al iniciar por dependencias faltantes:
  - `cupboard`
  - `puzzleslib`

Después de añadir dependencias:

- El servidor inició correctamente.
- El TPS se estabilizó después de un spike inicial.

Resultado final de `spark tps`:

- TPS 5s / 10s / 1m / 5m / 15m:
  - 19.97 / 20.0 / 20.0 / 19.01 / 19.33

- Tick durations last 10s:
  - min: 8.4 ms
  - median: 9.9 ms
  - 95%ile: 17.0 ms
  - max: 37.3 ms

- Tick durations last 1m:
  - min: 8.2 ms
  - median: 9.9 ms
  - 95%ile: 16.9 ms
  - max: 67.1 ms

- CPU process:
  - 4% / 5% / 13%

### Evaluación

El lote quedó estable después de resolver las dependencias faltantes.

Hubo un spike inicial de lag durante la estabilización, pero el TPS volvió a 20 y el MSPT quedó en valores sanos.

### Veredicto

**Phase 8B - Fixes / Stability Batch: aprobado preliminarmente.**

### Próximo paso recomendado

- Probar entrada con cliente.
- Revisar inventario, crafteos y JEI.
- Probar portal al Nether.
- Probar Twilight Forest si hay portal disponible.
- Ejecutar `spark tps` después de 2–3 minutos de movimiento.
- Si se mantiene estable, marcar este lote como aprobado oficialmente y pasar al lote Client-only / UX.

## 2026-06-09 - Phase 8B: Client-only / UX Batch

### Estado

**Aprobado.**

Se añadió un lote de mods client-only enfocado en mejorar la interfaz, la información visual, JEI/Jade, animaciones y tooltips.

Este lote fue instalado únicamente en el cliente TecMC. No se añadieron estos mods al servidor, por lo que no deberían afectar directamente el TPS ni la generación del mundo.

### Mods añadidos

#### Client-only / UX

- Jade Addons
- JustEnoughResources
- JustEnoughBreeding
- JustEnoughProfessions
- NotEnoughAnimations
- OverflowingBars
- MiningSpeedTooltips

#### Dependencias añadidas

- TxniLib

### Mods no añadidos

- StylishEffects

### Ajustes / notas

- `Jade Addons` amplía la información mostrada por Jade.
- `JustEnoughResources` permite consultar recursos, drops y generación desde JEI.
- `JustEnoughBreeding` ayuda a revisar información de crianza de animales.
- `JustEnoughProfessions` ayuda a revisar profesiones y trades de aldeanos.
- `NotEnoughAnimations` mejora animaciones del jugador en cliente.
- `OverflowingBars` mejora la visualización de barras cuando hay valores altos.
- `MiningSpeedTooltips` añade información útil sobre velocidad de minado.
- `TxniLib` fue añadida como dependencia necesaria para este lote.

### Resultado de prueba

Después de añadir el lote client-only, el servidor se mantuvo estable.

Resultado de `spark tps`:

- TPS 5s / 10s / 1m / 5m / 15m:
  - 20.0 / 20.0 / 20.0 / 20.0 / 20.0

- Tick durations last 10s:
  - min: 7.7 ms
  - median: 9.8 ms
  - 95%ile: 16.6 ms
  - max: 34.3 ms

- Tick durations last 1m:
  - min: 7.7 ms
  - median: 10.8 ms
  - 95%ile: 20.2 ms
  - max: 200.5 ms

- CPU process:
  - 5% / 6% / 1%

### Evaluación

El lote client-only no generó impacto negativo en el servidor.

El TPS se mantuvo en 20.0 de forma consistente. Se observó un spike puntual de 200.5 ms en el último minuto, pero el 95%ile se mantuvo sano en 20.2 ms, por lo que no representa lag sostenido.

### Veredicto

**Phase 8B - Client-only / UX Batch: aprobado.**

### Próximo paso recomendado

Pasar al siguiente lote antes del mundo final:

- Aether Villages
- Deep Aether
- Lost Aether Content

Luego testear:

- Inicio del server
- Entrada con cliente
- Exploración ligera en Overworld y Aether
- `spark tps` después de 2–3 minutos

```markdown
## 2026-06-09 - Phase 8C: Aether Expansion Batch

### Estado

**Aprobado preliminarmente.**

Se añadió un lote de expansión para la dimensión del Aether, enfocado en mejorar exploración, estructuras y contenido adicional relacionado con esta dimensión.

Este lote sí afecta contenido/worldgen del Aether, por lo que debe quedar definido antes de crear el mundo final y antes de ejecutar Chunky.

### Mods añadidos

#### Aether Expansion

- Aether Villages
- Deep Aether
- Lost Aether Content

### Tipo de cambio

- Añade nuevas estructuras y contenido para el Aether.
- Añade más variedad de exploración en la dimensión.
- Puede afectar chunks nuevos del Aether.
- Requiere instalación tanto en cliente como en servidor.

### Resultado de prueba

Después de añadir el lote, el servidor inició correctamente y se realizó prueba de rendimiento.

Resultado de `spark tps`:

- TPS 5s / 10s / 1m / 5m / 15m:
  - 20.0 / 20.0 / 20.0 / 19.34 / 19.14

- Tick durations last 10s:
  - min: 12.4 ms
  - median: 15.6 ms
  - 95%ile: 27.4 ms
  - max: 55.6 ms

- Tick durations last 1m:
  - min: 7.9 ms
  - median: 11.1 ms
  - 95%ile: 22.9 ms
  - max: 172.7 ms

- CPU process:
  - 7% / 7% / 8%

### Evaluación

El lote se mantuvo estable durante la prueba inicial.

Los TPS de 5s, 10s y 1m se mantuvieron en 20.0. Los valores de 5m y 15m todavía arrastran carga previa o generación de chunks, pero el rendimiento actual se mantiene sano.

Se observó un spike puntual de 172.7 ms en el último minuto, probablemente asociado a carga de dimensión/chunks nuevos. El 95%ile se mantuvo bajo en 22.9 ms, por lo que no representa lag sostenido.

### Veredicto

**Phase 8C - Aether Expansion Batch: aprobado preliminarmente.**

### Próximo paso recomendado

Antes de marcarlo como aprobado oficial:

- Explorar el Aether durante 2–3 minutos.
- Cargar algunos chunks nuevos.
- Revisar consola por errores.
- Ejecutar nuevamente `spark tps`.

Si el TPS se mantiene en 20.0 y el 95%ile sigue por debajo de 40–50 ms, marcar este lote como aprobado oficialmente.

Siguiente lote sugerido:

- Farmer Structures
- Structory Towers
- Moog’s Missing Villages
```
## 2026-06-09 - Phase 8C: Worldgen Heavy Batch

### Estado

**Aprobado oficialmente.**

Se añadió un lote grande de worldgen, estructuras, expansión de Nether, contenido Deep Dark y ajustes de distribución de estructuras.

Este lote afecta generación de chunks nuevos, por lo que debe quedar definido antes de crear el mundo final y antes de ejecutar Chunky.

### Mods añadidos

#### Worldgen / estructuras / contenido

- Improved Village Placement
- Illager Invasion
- Deeper and Darker
- Jaden's Nether Expansion
- Sparse Structures
- Vanilla Backport
- Structory Towers
- Philip's Ruins
- Moog's Missing Villages

#### Dependencias añadidas

- Platform
- VB Compat

### Ajustes de configuración

#### Sparse Structures

Se detectó que el valor por defecto de Sparse Structures era demasiado agresivo para TecMC.

Valor original:

- `spreadFactor: 2.0`

Ese valor hacía que las estructuras aparecieran demasiado separadas, dejando el mundo más vacío de lo esperado para un server estilo BetterMC / RPG exploration.

Valor ajustado:

- `spreadFactor: 1.3`
- `idBasedSalt: true`

También se ajustó la mansión:

- `minecraft:mansion`
- `factor: 1.2`

### Config final relevante

```json
{
  "spreadFactor": 1.3,
  "idBasedSalt": true,
  "customSpreadFactors": [
    {
      "structure": "minecraft:mansion",
      "factor": 1.2
    }
  ]
}

## 2026-06-11 - Fase 8W: última ronda de worldgen y compatibilidad previa al mundo final

### Añadido

Se añadió una primera tanda de mods candidatos para la fase de **Worldgen Freeze**, enfocada en probar contenido que debe decidirse antes de crear el mundo definitivo.

#### Worldgen / estructuras / mobs

- Royal Variations
- Myths and Legends
- Enderman Overhaul
- Medieval Buildings [Nether Edition]
- Medieval Buildings [End Edition]
- Create Ore Excavation
- Dungeons and Taverns Ancient City Overhaul
- Explorations
- Snow Under Trees
- The Conjurer
- Pufferfish's Biome Dither
- Blended Compat

#### Compatibilidad / progresión

- Mowzie Cataclysm
- Cataclysm x YUNG's Better Nether Fortresses Compat
- Deeper and Darker to Cataclysm Progression
- Ender Dragon Loot

#### QoL / gameplay

- Easy Magic
- Client Sort
- Bartering Station
- Cut Through
- Elytra Slot
- Caelus API

### Pruebas realizadas

Se realizó prueba de estabilidad con el servidor activo y el jugador cargando chunks nuevos en vuelo.

Resultado de `spark tps` durante exploración/carga de chunks:

- TPS: `20.0 / 20.0 / 20.0 / 20.0 / 19.9`
- Tick durations 1m: `10.2 / 16.4 / 34.2 / 114.9 ms`
- CPU del proceso: `41% / 24% / 19%`

### Resultado

La tanda queda **aprobada provisionalmente**.

El servidor mantuvo 20 TPS incluso durante carga de chunks nuevos. Se observaron picos pequeños normales de worldgen, pero no hubo lag crítico ni spikes graves.

### Observaciones

- Esta tanda debe seguir probándose en Overworld, Nether y End antes del freeze definitivo.
- No añadir todavía la siguiente tanda hasta completar pruebas de exploración más largas.
- Al tratarse de mods que pueden afectar generación del mundo, deben decidirse antes de crear el mundo final.
- Una vez cerrado el Worldgen Freeze, no se deben añadir más mods que modifiquen Overworld worldgen, estructuras, biomas, cuevas, ores o aldeas.

## 2026-06-11 - Fase 8W: Tanda 2A de Loot Integrations y ajustes de progresión

### Añadido

Se añadió una segunda tanda enfocada en **compatibilidad de loot**, integración entre estructuras/mods y ajustes menores de progresión.

#### Loot Integrations

- Loot Integrations
- Loot Integrations: Vanilla
- Loot Integrations: YUNG's
- Loot Integrations: The Graveyard
- Loot Integrations: Moog's Structures
- Loot Integrations: Ice and Fire
- Loot Integrations: Dungeons and Taverns
- Loot Integrations: Philip's Ruins
- Loot Integrations: Born in Chaos

#### Progresión / balance

- Netherite Tweaks & Fixes

### Pruebas realizadas

Se realizó prueba de arranque, entrada al mundo, exploración y entrada al Nether.

Resultado de `spark tps` posterior a la prueba:

- TPS: `20.0 / 20.0 / 20.0 / 19.29 / 19.74`
- Tick durations 1m: `9.3 / 11.5 / 18.6 / 44.4 ms`
- CPU del proceso: `15% / 15% / 13%`

### Resultado

La tanda queda **aprobada provisionalmente**.

El servidor arrancó correctamente, el jugador pudo entrar al mundo y acceder al Nether sin crash. El rendimiento final fue estable, manteniendo 20 TPS y tick times bajos.

### Observaciones

- Se observaron spikes puntuales de `Can't keep up!` durante carga de chunks, entrada al Nether o movimiento rápido.
- Se registraron warnings de Lithostitched por referencias a template pools inexistentes.
- Se registró un warning menor relacionado con loot: `Couldn't set damage of loot item golden_horse_armor`.
- No se detectó crash ni caída permanente de TPS.
- Pendiente probar más cofres de estructuras para validar que las loot tables integradas funcionen correctamente.

### Estado

- Estado de la tanda: **aprobada provisionalmente**
- Riesgo actual: **bajo-medio**
- Próxima acción recomendada: probar apertura de cofres en estructuras YUNG, Graveyard, Dungeons and Taverns, Philip's Ruins y estructuras del Nether.

## 2026-06-11 - Fase 8W: Tanda 2B de Nether/End y rollback de compatibilidad visual

### Añadido / probado

Se inició una nueva tanda enfocada en contenido de **Nether, End, estructuras dimensionales y compatibilidad visual**.

Mods probados durante la tanda:

- End's Phantasm
- Formations
- Formations Nether
- Loot Integrations: Formations
- Better End Cities
- Sodium Dynamic Lights
- Sodium Options API
- Immersive Lanterns
- TxniLib

### Problemas detectados

Durante la prueba inicial se detectaron problemas de compatibilidad en cliente y dependencias faltantes en servidor.

#### Immersive Lanterns

El servidor no pudo arrancar inicialmente porque **Immersive Lanterns requería TxniLib** y esta dependencia no estaba instalada en el servidor.

Estado:

- Immersive Lanterns queda pausado.
- TxniLib solo será necesario si se vuelve a probar Immersive Lanterns.
- Se recomienda reintentar Immersive Lanterns más adelante como mini tanda aislada.

#### Sodium Dynamic Lights / Sodium Options API

El cliente crasheó por conflicto relacionado con **Embeddium** y `sodiumoptionsapi`.

Estado:

- Sodium Dynamic Lights queda descartado/pausado.
- Sodium Options API queda descartado/pausado.
- Se recomienda buscar una alternativa de dynamic lights compatible con Forge 1.20.1 + Embeddium, sin dependencia de Sodium.

### Rollback aplicado

Se eliminaron los siguientes mods para recuperar estabilidad del cliente:

- Sodium Options API
- Sodium Dynamic Lights
- Immersive Lanterns

Tras eliminar estos mods, el cliente volvió a abrir correctamente.

### Prueba de rendimiento posterior

Se realizó prueba con `spark tps` después del rollback.

Resultado:

- TPS: `19.95 / 19.98 / 20.0 / 19.8 / 19.93`
- Tick durations 10s: `9.7 / 13.5 / 27.2 / 46.4 ms`
- Tick durations 1m: `9.7 / 14.1 / 25.1 / 104.2 ms`
- CPU sistema: `41% / 48% / 47%`
- CPU proceso: `8% / 8% / 10%`

### Resultado

La tanda queda **aprobada provisionalmente en rendimiento** después del rollback.

El servidor mantiene TPS estable, bajo uso de CPU del proceso y tick times saludables. El spike máximo de `104.2 ms` no se considera grave mientras el TPS se mantenga cerca de 20 y el P95 esté controlado.

### Estado actual

- Cliente: **abre limpio**
- Servidor: **carga correctamente**
- Tanda 2B: **aprobada provisionalmente**
- Dynamic Lights: **descartado/pausado**
- Immersive Lanterns: **pausado para prueba aislada**
- Pendiente: validar logs finales y probar Nether/End con más exploración

### Próxima acción recomendada

Antes de añadir más mods, realizar una última prueba de exploración:

1. Entrar al Overworld.
2. Probar Nether cargando chunks.
3. Probar End cargando chunks.
4. Ejecutar `spark tps`.
5. Revisar `latest.log`.

Si no aparecen errores graves, la Tanda 2B queda lista para cerrar y pasar a la siguiente tanda de QoL/balance.



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