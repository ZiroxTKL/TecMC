# Backup Policy

This document defines how TecMC backups are created, stored and validated.

GitHub is used for versioning clean project files such as configs, documentation, scripts, quests and planning files. It is not a full server backup system.

Full server backups must be stored separately as ZIP files.

---

## Backup rule

Before any major change, especially worldgen, structure mods, dimensions, death systems, teleport systems or progression changes, a full backup must be created.

Main workflow:

backup -> small change -> test -> document -> commit -> push

---

## What a full backup should include

A full server backup should include:

- `world/`
- `config/`
- `defaultconfigs/`
- `server.properties`
- `user_jvm_args.txt`
- `run.bat`
- `run.sh`
- `whitelist.json`
- `ops.json`
- `banned-players.json`
- `banned-ips.json`
- `patchouli_books/`
- quest files
- NPC/lore files
- relevant documentation
- modpack export or reference to the current mod profile

---

## What a backup does not need to include

A backup does not need to include:

- old `logs/`
- old `crash-reports/`
- cache files
- duplicate backups
- temporary files
- unused test worlds

---

## Naming format

Recommended format:

`TecMC_PhaseX_description_YYYY-MM-DD.zip`

Examples:

- `TecMC_Phase4B_preYUNG_2026-06-07.zip`
- `TecMC_Phase5_testworld_before_TownsAndTowers_2026-06-07.zip`
- `TecMC_preOfficialWorld_2026-06-07.zip`

---

## Backup validation

A backup only counts as valid if it can be restored and the server starts correctly.

Minimum restoration test:

1. Extract the ZIP into a separate test folder.
2. Start the server.
3. Confirm that there is no crash.
4. Join the world.
5. Check that configs, quests, NPC/lore files and whitelist are present.
6. Stop the server using `stop`.

If the server cannot start from the restored backup, the backup is not valid.

---

## Official world rule

The official world must not be created until Phase 5 worldgen and structure testing is completed.

Before creating the official world:

- Phase 4B must be backed up.
- The backup must be tested.
- Phase 5 mods must be tested in a separate world.
- Performance must be checked with spark.
- Logs must be reviewed.
- The changelog must be updated.