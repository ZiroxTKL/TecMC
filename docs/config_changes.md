# Config Changes

## Base server properties

Initial server configuration for TecMC.

### Gameplay

- `difficulty=hard`
- `gamemode=survival`
- `pvp=true`
- `hardcore=false`
- `enable-command-block=true`

### Progression

- `allow-nether=false`

The Nether is intentionally disabled during the first days of progression and will be enabled later as part of the server lore/quest progression.

### Access and security

- `online-mode=false`
- `white-list=true`
- `enforce-whitelist=true`

The server runs in offline mode for compatibility, but whitelist enforcement is enabled to prevent unauthorized access.

### Performance

- `view-distance=8`
- `simulation-distance=6`
- `sync-chunk-writes=true`
- `max-tick-time=60000`

Simulation distance may be reduced to 5 or 4 if TPS drops with multiple players.

### Server identity

- `max-players=10`
- `motd=§b§l§k|§b§l TecMC 1.0 §k|`