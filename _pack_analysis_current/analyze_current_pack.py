from __future__ import annotations

import csv
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except Exception:  # pragma: no cover
    tomllib = None


SERVER_ROOT = Path(r"C:\Users\leoma\OneDrive\Documentos\VSCode\Server_Minecraft")
SERVER_MODS = SERVER_ROOT / "mods"
CLIENT_ROOT = Path(r"C:\Users\leoma\curseforge\minecraft\Instances\TecMC")
CLIENT_MODS = CLIENT_ROOT / "mods"
OUT = SERVER_ROOT / "_pack_analysis_current"

CONFIRMED = "Confirmado por archivos internos"
INFERRED = "Inferido por nombre del mod"
UNKNOWN = "No confirmado"

INTERNAL_ALLOWED_DIRS = [
    SERVER_ROOT / "config",
    SERVER_ROOT / "defaultconfigs",
    SERVER_ROOT / "serverconfig",
    SERVER_ROOT / "world" / "serverconfig",
    SERVER_ROOT / "world" / "datapacks",
    SERVER_ROOT / "_datapacks_master",
    SERVER_ROOT / "logs",
]

WORLDGEN_DIRS = {
    "structures_nbt": r"^data/[^/]+/structures/.+\.(nbt|json)$",
    "worldgen_structure": r"^data/[^/]+/worldgen/structure/.+\.json$",
    "structure_set": r"^data/[^/]+/worldgen/structure_set/.+\.json$",
    "template_pool": r"^data/[^/]+/worldgen/template_pool/.+\.json$",
    "biome": r"^data/[^/]+/worldgen/biome/.+\.json$",
    "configured_feature": r"^data/[^/]+/worldgen/configured_feature/.+\.json$",
    "placed_feature": r"^data/[^/]+/worldgen/placed_feature/.+\.json$",
    "dimension": r"^data/[^/]+/dimension/.+\.json$",
    "dimension_type": r"^data/[^/]+/dimension_type/.+\.json$",
    "biome_modifier": r"^data/[^/]+/(forge/)?biome_modifier/.+\.json$",
    "worldgen_modifier": r"^data/[^/]+/lithostitched/worldgen_modifier/.+\.json$",
}

COUNT_DIRS = {
    "loot_tables": r"^data/[^/]+/loot_tables/.+\.json$",
    "recipes": r"^data/[^/]+/recipes/.+\.json$",
    "advancements": r"^data/[^/]+/advancements/.+\.json$",
    "tags": r"^data/[^/]+/tags/.+\.json$",
    "lang": r"^assets/[^/]+/lang/.+\.(json|lang)$",
}

CLIENT_HINTS = {
    "embeddium",
    "oculus",
    "rubidium",
    "sodium",
    "chloride",
    "entityculling",
    "immediatelyfast",
    "flerovium",
    "jei",
    "jer",
    "justenough",
    "fancymenu",
    "konkrete",
    "melody",
    "appleskin",
    "mousetweaks",
    "clientsort",
    "controlling",
    "chat_heads",
    "chatheads",
    "skinlayers",
    "sound_physics",
    "soundphysics",
    "advancementplaques",
    "betterf3",
    "inventoryhud",
}

SERVER_HINTS = {
    "skinrestorer",
    "spark",
    "chunky",
    "servercore",
    "connectivity",
    "packetfixer",
}

PERF_HINTS = {
    "modernfix",
    "ferrite",
    "canary",
    "radium",
    "lithium",
    "fastsuite",
    "fastasyncworldsave",
    "chunksending",
    "connectivity",
    "packetfixer",
    "mobtimizations",
    "ai-improvements",
    "entityculling",
    "embeddium",
    "flerovium",
    "structureessentials",
    "structure_layout_optimizer",
    "chloride",
}

LIB_HINTS = {
    "architectury",
    "balm",
    "citadel",
    "geckolib",
    "cloth",
    "curios",
    "patchouli",
    "moonlight",
    "selene",
    "placebo",
    "terrablender",
    "bclib",
    "blueprint",
    "bookshelf",
    "framework",
    "puzzleslib",
    "kleiders",
    "konkrete",
    "melody",
    "cupboard",
    "cristel",
    "lithostitched",
    "athena",
    "resourceful",
    "irons_lib",
}

DIMENSION_HINTS = {
    "aether": "aether",
    "twilight": "twilight_forest",
    "betterend": "minecraft:the_end",
    "betternether": "minecraft:the_nether",
    "nether": "minecraft:the_nether",
    "end": "minecraft:the_end",
    "undergarden": "undergarden",
    "bumblezone": "the_bumblezone",
    "blue_skies": "blue_skies",
    "blueskies": "blue_skies",
    "alexscaves": "alexscaves",
    "deeperdarker": "deeperdarker",
}

HIGH_CHUNK_BORDER_HINTS = {
    "biomesoplenty",
    "biomes_o_plenty",
    "biomesop",
    "nullscape",
    "yungscavebiomes",
    "alexscaves",
    "terralith",
    "regions_unexplored",
    "regionsunexplored",
    "tectonic",
    "geophilic",
    "williamwythers",
    "byg",
    "oh_the_biomes",
}

STRUCTURE_VANILLA_KEYS = {
    "village": "Aldeas",
    "ancient_city": "Ancient Cities",
    "stronghold": "Strongholds",
    "fortress": "Nether Fortresses",
    "end_city": "End Cities",
    "mansion": "Woodland Mansions",
    "mineshaft": "Mineshafts",
    "pillager_outpost": "Pillager Outposts",
    "bastion": "Bastions",
    "ruined_portal": "Ruined Portals",
}

BOSS_WORDS = {
    "boss",
    "bossbar",
    "boss_bar",
    "bossfight",
    "summon_boss",
    "raid_boss",
}

BOSS_RE = re.compile(r"(?<![a-z])boss(?:es|bar|_bar|fight)?(?![a-z])")


def boss_signal(value: str) -> bool:
    return bool(BOSS_RE.search(value.lower()))

RELEVANT_ITEM_WORDS = [
    "sword",
    "blade",
    "axe",
    "bow",
    "crossbow",
    "staff",
    "wand",
    "spell",
    "scroll",
    "book",
    "tome",
    "helmet",
    "chestplate",
    "leggings",
    "boots",
    "armor",
    "shield",
    "relic",
    "artifact",
    "ring",
    "charm",
    "amulet",
    "trinket",
    "core",
    "key",
    "eye",
    "gem",
    "ingot",
    "essence",
    "shard",
    "fragment",
    "totem",
    "spawn_egg",
]


def norm_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def short_list(values, limit=12):
    values = [str(v) for v in values if v]
    if len(values) <= limit:
        return ", ".join(values)
    return ", ".join(values[:limit]) + f", ... (+{len(values) - limit})"


def md_escape(value) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def read_zip_text(zf: zipfile.ZipFile, name: str, max_bytes: int = 1_000_000) -> str:
    try:
        info = zf.getinfo(name)
        if info.file_size > max_bytes:
            return ""
        with zf.open(name) as fh:
            return fh.read(max_bytes).decode("utf-8", errors="replace")
    except Exception:
        return ""


def parse_toml(text: str):
    if not text.strip():
        return {}
    if tomllib:
        try:
            return tomllib.loads(text)
        except Exception:
            return {}
    return {}


def extract_mod_metadata(zf: zipfile.ZipFile, names: list[str]):
    toml_paths = [
        n
        for n in names
        if n.lower() in {"meta-inf/mods.toml", "meta-inf/neoforge.mods.toml"}
        or n.lower().endswith("/mods.toml")
        or n.lower().endswith("/neoforge.mods.toml")
    ]
    all_mods = []
    all_deps = []
    meta = {
        "modLoader": "",
        "loaderVersion": "",
        "license": "",
        "toml_paths": toml_paths,
        "toml_parse_ok": False,
    }
    for path in toml_paths:
        text = read_zip_text(zf, path)
        data = parse_toml(text)
        if not data:
            continue
        meta["toml_parse_ok"] = True
        meta["modLoader"] = meta["modLoader"] or str(data.get("modLoader", ""))
        meta["loaderVersion"] = meta["loaderVersion"] or str(data.get("loaderVersion", ""))
        meta["license"] = meta["license"] or str(data.get("license", ""))
        mods = data.get("mods", [])
        if isinstance(mods, dict):
            mods = [mods]
        for mod in mods:
            if isinstance(mod, dict):
                all_mods.append(
                    {
                        "modId": str(mod.get("modId", "")).strip(),
                        "displayName": str(mod.get("displayName", "")).strip(),
                        "version": str(mod.get("version", "")).strip(),
                        "description": str(mod.get("description", "")).strip(),
                    }
                )
        deps = data.get("dependencies", {})
        if isinstance(deps, dict):
            for owner, dep_items in deps.items():
                if isinstance(dep_items, dict):
                    dep_items = [dep_items]
                if not isinstance(dep_items, list):
                    continue
                for dep in dep_items:
                    if not isinstance(dep, dict):
                        continue
                    all_deps.append(
                        {
                            "owner": str(owner),
                            "modId": str(dep.get("modId", "")).strip(),
                            "mandatory": bool(dep.get("mandatory", False)),
                            "versionRange": str(dep.get("versionRange", "")).strip(),
                            "ordering": str(dep.get("ordering", "")).strip(),
                            "side": str(dep.get("side", "")).strip(),
                        }
                    )
    return meta, all_mods, all_deps


def iter_json_value_strings(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from iter_json_value_strings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_json_value_strings(value)
    elif isinstance(obj, str):
        yield obj


def lang_entries_from_text(path: str, text: str):
    out = {}
    if path.lower().endswith(".json"):
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, str):
                        out[str(k)] = v
        except Exception:
            return out
    else:
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            out[key.strip()] = val.strip()
    return out


def id_from_data_path(path: str, folder: str) -> str:
    parts = path.split("/")
    try:
        idx = parts.index(folder)
    except ValueError:
        return path
    namespace = parts[1] if len(parts) > 1 else "unknown"
    tail = "/".join(parts[idx + 1 :])
    tail = re.sub(r"\.(json|nbt|mcfunction)$", "", tail)
    return f"{namespace}:{tail}"


def id_from_worldgen_path(path: str, leaf: str) -> str:
    parts = path.split("/")
    namespace = parts[1] if len(parts) > 1 else "unknown"
    marker = f"/worldgen/{leaf}/"
    tail = path.split(marker, 1)[-1] if marker in path else path
    tail = re.sub(r"\.json$", "", tail)
    return f"{namespace}:{tail}"


def detect_dimensions_from_text(text: str, path: str):
    dims = set()
    hay = (text + "\n" + path).lower()
    checks = {
        "minecraft:overworld": [
            "minecraft:overworld",
            "#minecraft:is_overworld",
            "is_overworld",
            "overworld",
        ],
        "minecraft:the_nether": [
            "minecraft:the_nether",
            "#minecraft:is_nether",
            "is_nether",
            "nether",
        ],
        "minecraft:the_end": [
            "minecraft:the_end",
            "#minecraft:is_end",
            "is_end",
            "the_end",
            "end_city",
        ],
    }
    for dim, words in checks.items():
        if any(word in hay for word in words):
            dims.add(dim)
    return dims


@dataclass
class JarAnalysis:
    path: Path
    location: str
    jar_name: str
    file_size: int
    meta: dict = field(default_factory=dict)
    mods: list[dict] = field(default_factory=list)
    deps: list[dict] = field(default_factory=list)
    bundled_mod_ids: list[str] = field(default_factory=list)
    counts: Counter = field(default_factory=Counter)
    namespace_counts: Counter = field(default_factory=Counter)
    entries: dict = field(default_factory=lambda: defaultdict(list))
    text_hits: dict = field(default_factory=lambda: defaultdict(list))
    lang: dict = field(default_factory=dict)
    entities: dict = field(default_factory=dict)
    items: dict = field(default_factory=dict)
    blocks: dict = field(default_factory=dict)
    biomes: dict = field(default_factory=dict)
    structures: list[str] = field(default_factory=list)
    structure_sets: list[str] = field(default_factory=list)
    template_pools: list[str] = field(default_factory=list)
    dimensions: list[str] = field(default_factory=list)
    dimension_types: list[str] = field(default_factory=list)
    affected_dimensions: set[str] = field(default_factory=set)
    vanilla_structure_hits: set[str] = field(default_factory=set)
    boss_confirmed: list[str] = field(default_factory=list)
    boss_probable: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    side: str = UNKNOWN
    worldgen_risk: str = "Bajo"
    performance_risk: str = "Bajo"
    balance_risk: str = "Bajo"
    evidence: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def primary_mod_id(self) -> str:
        for mod in self.mods:
            if mod.get("modId"):
                return mod["modId"]
        return re.sub(r"[-_.]?(forge|mc)?1\.20\.1.*$", "", self.jar_name.lower()).replace(".jar", "")

    @property
    def primary_name(self) -> str:
        for mod in self.mods:
            if mod.get("displayName"):
                return mod["displayName"]
        return self.jar_name

    @property
    def version(self) -> str:
        for mod in self.mods:
            if mod.get("version"):
                return mod["version"]
        return UNKNOWN

    @property
    def mod_ids(self) -> list[str]:
        ids = [m.get("modId") for m in self.mods if m.get("modId")]
        return ids or [self.primary_mod_id]


def analyze_jar(path: Path, location: str) -> JarAnalysis:
    jar = JarAnalysis(path=path, location=location, jar_name=path.name, file_size=path.stat().st_size)
    try:
        with zipfile.ZipFile(path) as zf:
            names = [n.replace("\\", "/") for n in zf.namelist()]
            lower_names = [n.lower() for n in names]
            jar.meta, jar.mods, jar.deps = extract_mod_metadata(zf, names)
            nested_jars = [
                n
                for n in names
                if n.lower().endswith(".jar")
                and ("jarjar" in n.lower() or n.lower().startswith("meta-inf/jarjar/"))
            ]
            for nested in nested_jars[:80]:
                try:
                    info = zf.getinfo(nested)
                    if info.file_size > 30_000_000:
                        continue
                    with zf.open(nested) as fh:
                        data = fh.read()
                    with zipfile.ZipFile(io.BytesIO(data)) as nested_zf:
                        nested_names = [x.replace("\\", "/") for x in nested_zf.namelist()]
                        _, nested_mods, _ = extract_mod_metadata(nested_zf, nested_names)
                        for mod in nested_mods:
                            if mod.get("modId"):
                                jar.bundled_mod_ids.append(mod["modId"])
                except Exception:
                    continue
            if jar.bundled_mod_ids:
                jar.notes.append("Incluye jar-in-jar: " + short_list(sorted(set(jar.bundled_mod_ids)), 10))
            if not jar.mods:
                jar.notes.append("No se pudo confirmar META-INF/mods.toml parseable.")
            for name, lower in zip(names, lower_names):
                if lower.startswith("data/") and len(lower.split("/")) > 1:
                    jar.namespace_counts[lower.split("/")[1]] += 1
                for key, pattern in WORLDGEN_DIRS.items():
                    if re.match(pattern, lower):
                        jar.counts[key] += 1
                        if len(jar.entries[key]) < 500:
                            jar.entries[key].append(name)
                for key, pattern in COUNT_DIRS.items():
                    if re.match(pattern, lower):
                        jar.counts[key] += 1
                        if len(jar.entries[key]) < 500:
                            jar.entries[key].append(name)

                if boss_signal(lower):
                    jar.text_hits["boss_path"].append(name)
                for vanilla_key, label in STRUCTURE_VANILLA_KEYS.items():
                    if vanilla_key in lower:
                        jar.vanilla_structure_hits.add(label)

            # Read lang files first because they are compact and very useful.
            lang_paths = [p for p in jar.entries.get("lang", []) if re.search(r"/en_us\.(json|lang)$", p.lower())]
            if not lang_paths and jar.entries.get("lang"):
                lang_paths = jar.entries.get("lang", [])[:1]
            for lang_path in lang_paths[:8]:
                text = read_zip_text(zf, lang_path)
                for key, val in lang_entries_from_text(lang_path, text).items():
                    jar.lang[key] = val
                    low_key = key.lower()
                    low_pair = low_key + " " + val.lower()
                    if low_key.startswith("entity."):
                        jar.entities[key] = val
                    elif low_key.startswith("item."):
                        jar.items[key] = val
                    elif low_key.startswith("block."):
                        jar.blocks[key] = val
                    elif low_key.startswith("biome."):
                        jar.biomes[key] = val
                    entity_tail = ".".join(low_key.split(".")[2:]) if low_key.startswith("entity.") else ""
                    if low_key.startswith("entity.") and boss_signal(entity_tail + " " + val.lower()):
                        jar.boss_confirmed.append(f"{key} = {val}")
                    elif low_key.startswith("advancements.") and boss_signal(low_pair) and any(w in low_pair for w in ["defeat", "slay", "kill", "summon"]):
                        jar.boss_confirmed.append(f"{key} = {val}")

            # IDs from loot tables and worldgen paths.
            for ent_path in [n for n in names if re.match(r"^data/[^/]+/loot_tables/entities/.+\.json$", n.lower())]:
                ent_id = id_from_data_path(ent_path, "entities")
                jar.entities.setdefault(ent_id, ent_id)
                ent_leaf = ent_path.lower().split("/loot_tables/entities/", 1)[-1]
                if boss_signal(ent_leaf):
                    jar.boss_confirmed.append(ent_id)
            for struct_path in jar.entries.get("worldgen_structure", []):
                jar.structures.append(id_from_worldgen_path(struct_path, "structure"))
            for struct_path in jar.entries.get("structures_nbt", []):
                jar.structures.append(id_from_data_path(struct_path, "structures"))
            for path_set in jar.entries.get("structure_set", []):
                jar.structure_sets.append(id_from_worldgen_path(path_set, "structure_set"))
            for pool_path in jar.entries.get("template_pool", []):
                jar.template_pools.append(id_from_worldgen_path(pool_path, "template_pool"))
            for dim_path in jar.entries.get("dimension", []):
                jar.dimensions.append(id_from_data_path(dim_path, "dimension"))
            for dimt_path in jar.entries.get("dimension_type", []):
                jar.dimension_types.append(id_from_data_path(dimt_path, "dimension_type"))
            for biome_path in jar.entries.get("biome", []):
                biome_id = id_from_worldgen_path(biome_path, "biome")
                jar.biomes.setdefault(biome_id, biome_id)

            # Read relevant JSON resources to infer affected dimensions and boss signals.
            relevant_keys = [
                "worldgen_structure",
                "structure_set",
                "template_pool",
                "biome",
                "configured_feature",
                "placed_feature",
                "dimension",
                "dimension_type",
                "biome_modifier",
                "worldgen_modifier",
                "loot_tables",
                "advancements",
                "tags",
            ]
            for key in relevant_keys:
                for rel_path in jar.entries.get(key, [])[:300]:
                    text = read_zip_text(zf, rel_path, max_bytes=500_000)
                    if not text:
                        continue
                    jar.affected_dimensions.update(detect_dimensions_from_text(text, rel_path))
                    low = text.lower()
                    if (
                        (key == "advancements" and boss_signal(low))
                        or (key == "tags" and "/tags/entity_types/" in rel_path.lower() and boss_signal(low + " " + rel_path.lower()))
                        or ("loot_tables/entities/" in rel_path.lower() and boss_signal(rel_path.lower().split("/loot_tables/entities/", 1)[-1]))
                    ):
                        jar.text_hits["boss_text"].append(rel_path)
                    for vanilla_key, label in STRUCTURE_VANILLA_KEYS.items():
                        if vanilla_key in low:
                            jar.vanilla_structure_hits.add(label)
    except Exception as exc:
        jar.errors.append(f"{type(exc).__name__}: {exc}")
    finalize_jar(jar)
    return jar


def finalize_jar(jar: JarAnalysis):
    modid_norm = norm_name(" ".join(jar.mod_ids + [jar.jar_name, jar.primary_name]))
    raw_text = " ".join(jar.mod_ids + [jar.jar_name, jar.primary_name]).lower()
    client_hint_hit = (
        any(h in modid_norm for h in CLIENT_HINTS)
        or bool(re.search(r"(^|[^a-z0-9])jade([^a-z0-9]|$)", raw_text))
        or "jadeaddons" in modid_norm
    )

    # Infer dimensions from names when JSON does not say it directly.
    for hint, dim in DIMENSION_HINTS.items():
        if hint in modid_norm:
            jar.affected_dimensions.add(dim)

    cats = set()
    if any(h in modid_norm for h in PERF_HINTS):
        cats.add("Performance")
    if any(h in modid_norm for h in LIB_HINTS):
        cats.add("Librerias / dependencias")
    if client_hint_hit:
        cats.add("Cliente visual / HUD / UI")
    if "lootintegration" in modid_norm or "compat" in modid_norm:
        cats.add("Compatibilidad")
        cats.add("Loot / recompensas")
    if jar.counts["biome"] or jar.counts["configured_feature"] or jar.counts["placed_feature"] or jar.counts["biome_modifier"] or jar.counts["worldgen_modifier"]:
        cats.add("Worldgen / biomas / terreno")
    if jar.structures or jar.structure_sets or jar.template_pools:
        cats.add("Estructuras")
    if any("dungeon" in p.lower() for p in jar.structures + jar.structure_sets + jar.template_pools + [jar.jar_name]):
        cats.add("Dungeons")
    if jar.dimensions or jar.dimension_types:
        cats.add("Dimensiones")
    if jar.entities:
        cats.add("Mobs")
    is_cataclysm_core = any(mid == "cataclysm" for mid in jar.mod_ids) or jar.jar_name.lower().startswith("l_enders_cataclysm")
    if jar.boss_confirmed or jar.boss_probable or is_cataclysm_core or ("boss" in modid_norm and (jar.entities or jar.structures or jar.counts["loot_tables"])):
        cats.add("Bosses")
    if any(x in modid_norm for x in ["villager", "morevillagers", "easy_npc", "trader", "npc"]):
        cats.add("NPCs / traders / aldeanos")
    if any(x in modid_norm for x in ["spell", "magic", "irons", "ars", "mana", "occult", "goety", "botania", "relic", "artifact"]):
        cats.add("Magia")
    if any(x in modid_norm for x in ["combat", "weapon", "armor", "bettercombat", "simplyswords", "epicfight"]):
        cats.add("Combate")
    if jar.items and any(any(w in (k + v).lower() for w in ["sword", "armor", "helmet", "chestplate", "leggings", "boots", "tool", "axe"]) for k, v in list(jar.items.items())[:300]):
        cats.add("Armas / armaduras / herramientas")
    if jar.counts["loot_tables"]:
        cats.add("Loot / recompensas")
    if not cats and jar.counts["recipes"]:
        cats.add("QoL")
    if any(x in modid_norm for x in ["waystone", "backpack", "tombstone", "crafting", "polymorph", "carryon", "compass", "fallingtree", "ftbquests", "ftblibrary"]):
        cats.add("QoL")
    jar.categories = sorted(cats) if cats else [UNKNOWN]

    # Side inference.
    if jar.location == "shared":
        jar.side = "Both"
    elif jar.location == "client":
        if client_hint_hit:
            jar.side = "Client only"
        elif jar.counts["loot_tables"] or jar.counts["recipes"] or jar.entities or jar.structures or jar.dimensions:
            jar.side = "Both"
            jar.notes.append("Solo esta en cliente, pero contiene datos de gameplay; revisar si falta en servidor.")
        else:
            jar.side = "Client only"
    elif jar.location == "server":
        if any(h in modid_norm for h in SERVER_HINTS):
            jar.side = "Server only"
        elif client_hint_hit and not (jar.counts["loot_tables"] or jar.counts["recipes"] or jar.entities or jar.structures):
            jar.side = "Client only"
            jar.notes.append("Parece client-side y esta en servidor; revisar ubicacion.")
        else:
            jar.side = "Both" if (jar.counts["data"] or jar.counts["recipes"] or jar.entities or jar.structures or jar.dimensions or jar.deps) else UNKNOWN

    # Worldgen/chunk-border risk.
    existing_dims = {"minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"}
    touches_existing_dimension = bool(jar.affected_dimensions & existing_dims)
    has_custom_dimension = bool(jar.dimensions or jar.dimension_types or (jar.affected_dimensions - existing_dims))

    exact_high_worldgen_ids = {
        "betterend",
        "betternether",
        "biomesoplenty",
        "geophilic",
        "nullscape",
        "yungscavebiomes",
        "alexscaves",
    }
    exact_high_worldgen = any(mid.lower() in exact_high_worldgen_ids for mid in jar.mod_ids)
    custom_dimension_hint = any(x in modid_norm for x in ["aether", "twilightforest", "deeperdarker", "deepaether"])

    if custom_dimension_hint and jar.counts["biome"] > 0 and not exact_high_worldgen:
        jar.worldgen_risk = "Medio"
        jar.evidence.append(f"{CONFIRMED}: contiene biomas de dimension propia o no vanilla ({jar.counts['biome']}).")
    elif exact_high_worldgen or any(h in modid_norm for h in HIGH_CHUNK_BORDER_HINTS):
        jar.worldgen_risk = "Alto"
        jar.evidence.append("Inferido por nombre: mod de biomas/terreno conocido por tocar generacion base.")
    elif jar.counts["biome"] > 0 and touches_existing_dimension:
        jar.worldgen_risk = "Alto"
        jar.evidence.append(f"{CONFIRMED}: contiene biomas worldgen ({jar.counts['biome']}) en dimensiones existentes.")
    elif jar.counts["biome"] > 0 and not has_custom_dimension:
        jar.worldgen_risk = "Alto"
        jar.evidence.append(f"{CONFIRMED}: contiene biomas worldgen ({jar.counts['biome']}); dimension no confirmada.")
    elif jar.counts["biome"] > 0:
        jar.worldgen_risk = "Medio"
        jar.evidence.append(f"{CONFIRMED}: contiene biomas de dimension propia o no vanilla ({jar.counts['biome']}).")
    elif jar.counts["configured_feature"] or jar.counts["placed_feature"] or jar.counts["biome_modifier"] or jar.counts["worldgen_modifier"]:
        jar.worldgen_risk = "Medio"
        jar.evidence.append(f"{CONFIRMED}: contiene features/biome modifiers/worldgen modifiers.")
    elif jar.structures or jar.structure_sets or jar.template_pools:
        jar.worldgen_risk = "Bajo"
        jar.evidence.append(f"{CONFIRMED}: anade/modifica estructuras, sin evidencia de terreno base.")
    else:
        jar.worldgen_risk = "Bajo"

    # Performance risk.
    if any(x in modid_norm for x in ["cataclysm", "iceandfire", "alexscaves", "alexsmobs", "mowzie", "dungeonsarise", "blue_skies", "twilightforest"]):
        jar.performance_risk = "Medio"
    if len(jar.entities) > 60 or (jar.structures and len(jar.structures) > 80) or jar.file_size > 45_000_000:
        jar.performance_risk = "Medio"
    if any(x in modid_norm for x in ["performance", "modernfix", "ferrite", "canary", "fastsuite", "chunksending", "connectivity"]):
        jar.performance_risk = "Bajo"

    # Balance risk.
    balance_score = 0
    if "Bosses" in jar.categories:
        balance_score += 2
    if "Loot / recompensas" in jar.categories and jar.counts["loot_tables"] > 50:
        balance_score += 1
    if "Dungeons" in jar.categories or len(jar.structures) > 30:
        balance_score += 1
    if "Magia" in jar.categories or "Armas / armaduras / herramientas" in jar.categories:
        balance_score += 1
    if any(x in modid_norm for x in ["apotheosis", "cataclysm", "iceandfire", "bossesofmassdestruction", "borninchaos", "irons"]):
        balance_score += 1
    jar.balance_risk = "Alto" if balance_score >= 4 else "Medio" if balance_score >= 2 else "Bajo"

    # Boss confidence.
    if jar.text_hits.get("boss_text") and not jar.boss_confirmed:
        jar.boss_confirmed.append(f"Senales boss/bossbar en {short_list(jar.text_hits['boss_text'], 6)}")
    if not jar.boss_confirmed:
        bossy = [e for e in jar.entities.values() if any(word in str(e).lower() for word in ["boss", "king", "queen", "guardian", "lord", "monarch", "champion"])]
        if bossy:
            jar.boss_probable.extend(sorted(set(map(str, bossy)))[:25])
    if is_cataclysm_core and not jar.boss_confirmed:
        jar.boss_probable.append("Probable por nombre del mod Cataclysm; requiere revision manual de entidades.")


def collect_jars():
    server = {p.name: p for p in sorted(SERVER_MODS.glob("*.jar"))}
    client = {p.name: p for p in sorted(CLIENT_MODS.glob("*.jar"))}
    shared_names = set(server) & set(client)
    server_only = set(server) - set(client)
    client_only = set(client) - set(server)
    analyses = []
    for name in sorted(shared_names):
        analyses.append(analyze_jar(server[name], "shared"))
    for name in sorted(server_only):
        analyses.append(analyze_jar(server[name], "server"))
    for name in sorted(client_only):
        analyses.append(analyze_jar(client[name], "client"))
    return analyses, server, client, shared_names, server_only, client_only


def build_presence_by_modid(analyses):
    presence = defaultdict(set)
    jar_by_modid = defaultdict(list)
    for jar in analyses:
        locs = {"shared": {"server", "client"}, "server": {"server"}, "client": {"client"}}[jar.location]
        for mid in jar.mod_ids + jar.bundled_mod_ids:
            presence[mid].update(locs)
            jar_by_modid[mid].append(jar)
    return presence, jar_by_modid


def dependency_findings(analyses, presence):
    findings = []
    for jar in analyses:
        locs = {"shared": {"server", "client"}, "server": {"server"}, "client": {"client"}}[jar.location]
        for dep in jar.deps:
            dep_id = dep.get("modId", "")
            if not dep_id or dep_id in {"minecraft", "forge", "java", "neoforge"}:
                continue
            mandatory = dep.get("mandatory", False)
            dep_locs = presence.get(dep_id, set())
            dep_side = dep.get("side", "").upper()
            required_locs = set(locs)
            if dep_side == "CLIENT":
                required_locs &= {"client"}
            elif dep_side == "SERVER":
                required_locs &= {"server"}
            missing_on = sorted(required_locs - dep_locs)
            if mandatory and missing_on:
                findings.append((jar, dep, "Faltante en " + ", ".join(missing_on)))
    return findings


def version_flags(jar: JarAnalysis):
    text = " ".join([jar.jar_name, jar.primary_name, " ".join(jar.mod_ids), str(jar.meta.get("loaderVersion", ""))]).lower()
    flags = []
    if "neoforge" in text or any("neoforge" in p.lower() for p in jar.meta.get("toml_paths", [])):
        flags.append("Posible NeoForge")
    mc_tokens = sorted(set(re.findall(r"(?<!\d)1\.(?:19|20|21)(?:\.\d+)?(?!\d)", jar.jar_name.lower())))
    bad_tokens = [t for t in mc_tokens if t != "1.20.1"]
    if bad_tokens:
        flags.append("Version en nombre distinta a 1.20.1: " + ", ".join(bad_tokens))
    return flags


def scan_allowed_project_files():
    summary = {}
    for folder in INTERNAL_ALLOWED_DIRS:
        if not folder.exists():
            continue
        if "docs" in [p.name.lower() for p in folder.parents] or folder.name.lower() == "docs":
            continue
        files = [p for p in folder.rglob("*") if p.is_file() and "docs" not in [x.lower() for x in p.parts]]
        summary[str(folder)] = {
            "file_count": len(files),
            "json_count": sum(1 for p in files if p.suffix.lower() == ".json"),
            "toml_count": sum(1 for p in files if p.suffix.lower() == ".toml"),
            "datapacks": [p.name for p in folder.iterdir() if p.is_dir()] if "datapacks" in str(folder).lower() or folder.name.startswith("_datapacks") else [],
        }
    return summary


def scan_recent_logs(max_lines=200):
    logs_dir = SERVER_ROOT / "logs"
    out = []
    if not logs_dir.exists():
        return out
    logs = sorted(logs_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]
    patterns = ["error", "warn", "missing", "failed", "exception", "mixin"]
    for log in logs:
        try:
            lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        hits = [line.strip() for line in lines if any(p in line.lower() for p in patterns)]
        out.append({"file": str(log), "hits": hits[-max_lines:], "hit_count": len(hits)})
    return out


def category_summary(analyses):
    counts = Counter()
    for jar in analyses:
        for cat in jar.categories:
            counts[cat] += 1
    return counts


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(x) for x in row) + " |")
    return "\n".join(lines)


def mod_row(jar: JarAnalysis):
    adds_structures = bool(jar.structures or jar.structure_sets or jar.template_pools)
    adds_dimensions = bool(jar.dimensions or jar.dimension_types)
    adds_biomes = bool(jar.biomes)
    adds_mobs = bool(jar.entities)
    return [
        jar.jar_name,
        short_list(jar.mod_ids, 4),
        jar.primary_name,
        jar.version,
        jar.side,
        short_list(jar.categories, 4),
        "true" if jar.boss_confirmed or jar.boss_probable else "false",
        len(set(jar.boss_confirmed + jar.boss_probable)),
        "true" if adds_structures else "false",
        len(set(jar.structures)),
        "true" if adds_dimensions else "false",
        len(set(jar.dimensions)),
        "true" if adds_biomes else "false",
        len(set(jar.biomes)),
        "true" if adds_mobs else "false",
        len(set(jar.entities)),
        "true" if jar.counts["loot_tables"] else "false",
        jar.counts["loot_tables"],
        "true" if jar.counts["recipes"] else "false",
        jar.counts["recipes"],
        jar.worldgen_risk,
        jar.performance_risk,
        jar.balance_risk,
        "; ".join(jar.notes[:4]) or "; ".join(jar.evidence[:3]) or UNKNOWN,
    ]


def write_pack_analysis(analyses, server, client, shared_names, server_only, client_only, dep_findings, project_summary, log_summary):
    rows = []
    for jar in sorted(analyses, key=lambda j: (j.primary_name.lower(), j.jar_name.lower())):
        deps = [d for d in jar.deps if d.get("modId") not in {"minecraft", "forge", "java", "neoforge"}]
        rows.append(
            [
                jar.jar_name,
                short_list(jar.mod_ids, 3),
                jar.primary_name,
                jar.version,
                jar.side,
                short_list(jar.categories, 3),
                short_list([f"{d['modId']} ({'obligatoria' if d.get('mandatory') else 'opcional'})" for d in deps], 5) or UNKNOWN,
                short_list(jar.evidence, 2) or (CONFIRMED if jar.meta.get("toml_parse_ok") else UNKNOWN),
                jar.worldgen_risk,
                jar.performance_risk,
                jar.balance_risk,
                short_list(jar.notes + jar.errors + version_flags(jar), 3),
            ]
        )
    misplaced = []
    for jar in analyses:
        flags = version_flags(jar)
        if flags:
            misplaced.append((jar.jar_name, short_list(flags, 4)))
        if jar.location == "server" and jar.side == "Client only":
            misplaced.append((jar.jar_name, "Parece client-side en servidor"))
        if jar.location == "client" and jar.side == "Both":
            misplaced.append((jar.jar_name, "Parece gameplay/server-side solo en cliente"))
    lines = []
    lines.append("# Analisis tecnico actual del pack TecMC\n")
    lines.append("Generado desde los `.jar` y carpetas actuales del pack. No se leyo `docs/`.\n")
    lines.append("## Resumen general\n")
    lines.append(f"- Mods `.jar` en servidor: **{len(server)}**")
    lines.append(f"- Mods `.jar` en cliente: **{len(client)}**")
    lines.append(f"- `.jar` compartidos por nombre exacto: **{len(shared_names)}**")
    lines.append(f"- `.jar` solo servidor: **{len(server_only)}**")
    lines.append(f"- `.jar` solo cliente: **{len(client_only)}**")
    lines.append(f"- Mod IDs unicos analizados: **{len({m for j in analyses for m in j.mod_ids})}**\n")
    lines.append("## Mods solo servidor\n")
    lines.append(short_list(sorted(server_only), 80) or "Ninguno")
    lines.append("\n\n## Mods solo cliente\n")
    lines.append(short_list(sorted(client_only), 120) or "Ninguno")
    lines.append("\n\n## Posibles mods mal ubicados o a revisar\n")
    if misplaced:
        lines.append(table(["Jar", "Motivo"], misplaced))
    else:
        lines.append("No se detectaron candidatos claros.")
    lines.append("\n\n## Dependencias faltantes o desalineadas\n")
    if dep_findings:
        lines.append(table(["Jar", "Dependencia", "Tipo"], [(j.jar_name, f"{d.get('modId')} {d.get('versionRange')}", reason) for j, d, reason in dep_findings[:150]]))
    else:
        lines.append("No se detectaron dependencias obligatorias faltantes desde `mods.toml`.")
    lines.append("\n\n## Clasificacion por categoria\n")
    lines.append(table(["Categoria", "Mods"], [(k, v) for k, v in category_summary(analyses).most_common()]))
    lines.append("\n\n## Fuentes internas revisadas\n")
    lines.append(table(["Ruta", "Archivos", "JSON", "TOML", "Datapacks/carpetas"], [(k, v["file_count"], v["json_count"], v["toml_count"], short_list(v.get("datapacks", []), 12)) for k, v in project_summary.items()]))
    if log_summary:
        lines.append("\n\n## Logs recientes revisados\n")
        lines.append(table(["Log", "Lineas WARN/ERROR/missing/failed", "Ultimos hallazgos"], [(Path(l["file"]).name, l["hit_count"], short_list(l["hits"], 3)) for l in log_summary]))
    lines.append("\n\n## Fichas por mod\n")
    lines.append(table(
        [
            "Jar",
            "Mod ID",
            "Nombre",
            "Version",
            "Lado probable",
            "Categoria",
            "Dependencias declaradas",
            "Evidencia",
            "Riesgo mundo final",
            "Riesgo rendimiento",
            "Riesgo balance",
            "Comentarios",
        ],
        rows,
    ))
    (OUT / "pack_analysis.md").write_text("\n".join(lines), encoding="utf-8")


def write_content_summary(analyses):
    boss_confirmed = []
    boss_probable = []
    structures = []
    dimensions = []
    biomes = []
    mobs = []
    items = []
    for jar in analyses:
        for b in sorted(set(jar.boss_confirmed)):
            boss_confirmed.append((b, jar.primary_name, CONFIRMED))
        for b in sorted(set(jar.boss_probable)):
            boss_probable.append((b, jar.primary_name, INFERRED))
        if jar.structures or jar.structure_sets or jar.template_pools:
            structures.append((jar.primary_name, len(set(jar.structures)), len(set(jar.structure_sets)), len(set(jar.template_pools)), short_list(sorted(jar.affected_dimensions), 8) or UNKNOWN))
        for dim in sorted(set(jar.dimensions + jar.dimension_types)):
            dimensions.append((dim, jar.primary_name, CONFIRMED))
        for biome_id, label in sorted(jar.biomes.items())[:250]:
            biomes.append((biome_id, label, jar.primary_name, short_list(sorted(jar.affected_dimensions), 4) or UNKNOWN))
        if jar.entities:
            hostiles = []
            passive = []
            neutral = []
            bosses = []
            unclass = []
            for key, label in sorted(jar.entities.items())[:350]:
                low = (key + " " + str(label)).lower()
                if any(w in low for w in ["boss", "guardian", "lord", "queen", "king", "monarch"]):
                    bosses.append(label)
                elif any(w in low for w in ["zombie", "skeleton", "wraith", "knight", "warrior", "beast", "golem", "serpent", "dragon", "monster", "illager"]):
                    hostiles.append(label)
                elif any(w in low for w in ["cow", "sheep", "bird", "fish", "frog", "bee", "butterfly", "snail", "deer"]):
                    passive.append(label)
                elif any(w in low for w in ["trader", "villager", "npc"]):
                    neutral.append(label)
                else:
                    unclass.append(label)
            mobs.append((jar.primary_name, len(jar.entities), short_list(hostiles, 10), short_list(passive, 8), short_list(neutral, 8), short_list(bosses, 8), short_list(unclass, 8)))
        relevant = []
        for key, label in jar.items.items():
            low = (key + " " + str(label)).lower()
            if any(w in low for w in RELEVANT_ITEM_WORDS):
                relevant.append(f"{label} ({key})")
        if relevant:
            items.append((jar.primary_name, len(relevant), short_list(sorted(set(relevant)), 35), INFERRED))
    lines = []
    lines.append("# Resumen de contenido importante\n")
    lines.append("Este documento usa nombres, rutas, lang files, loot tables, advancements y worldgen internos. Si un dato no aparece en archivos, queda como `No confirmado`.\n")
    lines.append("## Bosses\n")
    lines.append(f"- Bosses confirmados por senales internas: **{len(set(x[0] + x[1] for x in boss_confirmed))}**")
    lines.append(f"- Bosses probables por nombre/entidad: **{len(set(x[0] + x[1] for x in boss_probable))}**\n")
    lines.append("### Confirmados\n")
    lines.append(table(["Boss/senal", "Mod", "Evidencia"], boss_confirmed[:250]) if boss_confirmed else "No confirmado")
    lines.append("\n\n### Probables\n")
    lines.append(table(["Boss probable", "Mod", "Evidencia"], boss_probable[:250]) if boss_probable else "No confirmado")
    lines.append("\n\n## Estructuras\n")
    lines.append(table(["Mod", "Estructuras", "Structure sets", "Template pools", "Dimensiones detectadas"], structures) if structures else "No confirmado")
    lines.append("\n\n## Dimensiones\n")
    lines.append(table(["Dimension/dimension_type", "Mod", "Evidencia"], dimensions) if dimensions else "No confirmado")
    lines.append("\n\n## Biomas\n")
    lines.append(table(["Biome ID", "Nombre/ID", "Mod", "Dimension probable"], biomes[:500]) if biomes else "No confirmado")
    lines.append("\n\n## Mobs\n")
    lines.append(table(["Mod", "Total entidades detectadas", "Hostiles", "Pasivos", "Neutrales/NPC", "Bosses/probables", "No clasificables"], mobs) if mobs else "No confirmado")
    lines.append("\n\n## Items importantes\n")
    lines.append(table(["Mod", "Cantidad candidatos", "Items", "Evidencia"], items[:220]) if items else "No confirmado")
    (OUT / "content_summary.md").write_text("\n".join(lines), encoding="utf-8")


def write_worldgen_impact(analyses):
    wg = [j for j in analyses if j.worldgen_risk != "Bajo" or j.structures or j.dimensions or j.dimension_types or j.counts["biome"]]
    rows = []
    for jar in sorted(wg, key=lambda j: ({"Alto": 0, "Medio": 1, "Bajo": 2}.get(j.worldgen_risk, 3), j.primary_name.lower())):
        rows.append(
            [
                jar.jar_name,
                jar.primary_name,
                jar.worldgen_risk,
                short_list(sorted(jar.affected_dimensions), 8) or UNKNOWN,
                jar.counts["biome"],
                jar.counts["configured_feature"] + jar.counts["placed_feature"],
                len(set(jar.structures)),
                len(set(jar.structure_sets)),
                len(set(jar.template_pools)),
                short_list(sorted(jar.vanilla_structure_hits), 8) or UNKNOWN,
                short_list(jar.evidence, 3) or CONFIRMED,
            ]
        )
    affects_overworld = [j for j in wg if "minecraft:overworld" in j.affected_dimensions or (j.worldgen_risk == "Alto" and not j.affected_dimensions)]
    affects_nether = [j for j in wg if "minecraft:the_nether" in j.affected_dimensions]
    affects_end = [j for j in wg if "minecraft:the_end" in j.affected_dimensions]
    adds_biomes = [j for j in wg if j.counts["biome"]]
    adds_features = [j for j in wg if j.counts["configured_feature"] or j.counts["placed_feature"] or j.counts["biome_modifier"]]
    modifies_vanilla = [j for j in wg if j.vanilla_structure_hits]
    must_before_world = [j for j in wg if j.worldgen_risk in {"Alto", "Medio"} and (j.counts["biome"] or j.counts["configured_feature"] or j.counts["placed_feature"] or j.counts["biome_modifier"] or j.counts["worldgen_modifier"])]
    add_later_ok = [j for j in wg if j.worldgen_risk == "Bajo" and (j.structures or j.dimensions or j.dimension_types)]
    chunky_test = [j for j in wg if j.worldgen_risk in {"Alto", "Medio"} or len(j.structures) > 50 or len(j.structure_sets) > 20]
    lines = []
    lines.append("# Impacto de worldgen\n")
    lines.append("Criterio de chunk border: alto si hay evidencia de biomas/terreno/generacion base; medio si hay features/ores/biome modifiers; bajo si solo hay estructuras o dimensiones propias.\n")
    lines.append("## Tabla principal\n")
    lines.append(table(["Jar", "Mod", "Riesgo chunk border", "Dimension afectada", "Biomas", "Features/placed", "Estructuras", "Structure sets", "Template pools", "Estructuras vanilla tocadas", "Evidencia"], rows))
    sections = [
        ("Mods que afectan Overworld", affects_overworld),
        ("Mods que afectan Nether", affects_nether),
        ("Mods que afectan End", affects_end),
        ("Mods que anaden estructuras", [j for j in wg if j.structures or j.structure_sets or j.template_pools]),
        ("Mods que anaden ores/features", adds_features),
        ("Mods que anaden biomas", adds_biomes),
        ("Mods que modifican aldeas/dungeons/estructuras vanilla", modifies_vanilla),
        ("Mods que deben quedar definidos antes del mundo final", must_before_world),
        ("Mods que se pueden anadir despues sin riesgo fuerte de chunk borders", add_later_ok),
        ("Mods que podrian generar chunk borders si se anaden tarde", [j for j in wg if j.worldgen_risk == "Alto"]),
        ("Mods que conviene probar con Chunky antes del lanzamiento", chunky_test),
    ]
    for title, items in sections:
        lines.append(f"\n\n## {title}\n")
        if items:
            lines.append(table(["Mod", "Jar", "Riesgo", "Evidencia"], [(j.primary_name, j.jar_name, j.worldgen_risk, short_list(j.evidence, 2) or CONFIRMED) for j in items]))
        else:
            lines.append("No confirmado")
    (OUT / "worldgen_impact.md").write_text("\n".join(lines), encoding="utf-8")


def write_balance_risk(analyses):
    rows = []
    for jar in sorted(analyses, key=lambda j: ({"Alto": 0, "Medio": 1, "Bajo": 2}.get(j.balance_risk, 3), j.primary_name.lower())):
        if jar.balance_risk == "Bajo":
            continue
        reasons = []
        if "Bosses" in jar.categories:
            reasons.append("bosses/progresion")
        if jar.counts["loot_tables"] > 50:
            reasons.append(f"loot tables altas ({jar.counts['loot_tables']})")
        if "Dungeons" in jar.categories or len(jar.structures) > 30:
            reasons.append("dungeons/estructuras con recompensas")
        if "Magia" in jar.categories:
            reasons.append("magia/progresion")
        if "Armas / armaduras / herramientas" in jar.categories:
            reasons.append("gear")
        recommendation = "Probar mas"
        if jar.balance_risk == "Alto" and (jar.counts["loot_tables"] > 50 or len(jar.structures) > 30):
            recommendation = "Ajustar datapack/config si el loot sale alto"
        if jar.worldgen_risk == "Alto":
            recommendation = "Probar mas antes de mundo final"
        rows.append([jar.primary_name, jar.jar_name, jar.balance_risk, short_list(reasons, 8), recommendation])
    general = [
        ("Progresion", "Medio", "Pack con bosses, dimensiones, End Remastered/Iron's Spells/gear; requiere test de ruta de progresion.", "Probar mas"),
        ("Loot excesivo", "Alto" if any(j.counts["loot_tables"] > 150 for j in analyses) else "Medio", "Muchas estructuras y Loot Integrations pueden llenar cofres con recompensas cruzadas.", "Ajustar datapack"),
        ("Spawners", "Medio", "Dungeons y estructuras pueden concentrar spawners/mobs.", "Probar mas"),
        ("Enchantments", "Medio", "Mods de loot/gear pueden combinarse con encantamientos fuertes.", "Ajustar config"),
        ("Netherite", "Medio", "Boss drops, dungeons y loot pueden adelantar materiales.", "Probar mas"),
        ("Armas demasiado fuertes", "Medio", "Varios mods de bosses/magia/loot anaden gear.", "Probar mas"),
        ("Armaduras demasiado fuertes", "Medio", "Gear de dimensiones y bosses puede saltar tiers.", "Probar mas"),
        ("Boss drops", "Alto", "Cataclysm/Ice and Fire/BOMD/Mowzie y similares pueden dar drops endgame.", "Ajustar datapack/config"),
        ("Traders/aldeanos", "Medio", "More Villagers, Easy NPC y estructuras con aldeanos pueden crear rutas de farmeo.", "Ajustar config"),
        ("Mobs fuertes early game", "Alto", "Born in Chaos, Ice and Fire, Alex's Mobs/Caves, Graveyard y dungeons pueden castigar spawn temprano.", "Probar mas"),
    ]
    lines = []
    lines.append("# Reporte de riesgos de balance\n")
    lines.append("Riesgo calculado por evidencia interna: loot tables, estructuras, entidades, categorias inferidas por nombre y recursos dentro de los jars.\n")
    lines.append("## Riesgos generales\n")
    lines.append(table(["Area", "Riesgo", "Motivo", "Recomendacion"], general))
    lines.append("\n\n## Mods con riesgo medio/alto\n")
    lines.append(table(["Mod", "Jar", "Riesgo", "Motivos", "Recomendacion"], rows) if rows else "No se detectaron riesgos altos/medios.")
    (OUT / "balance_risk_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_csv(analyses):
    headers = [
        "jar_name",
        "mod_id",
        "mod_name",
        "version",
        "side",
        "category",
        "adds_bosses",
        "boss_count",
        "adds_structures",
        "structure_count",
        "adds_dimensions",
        "dimension_count",
        "adds_biomes",
        "biome_count",
        "adds_mobs",
        "mob_count",
        "adds_loot_tables",
        "loot_table_count",
        "adds_recipes",
        "recipe_count",
        "worldgen_risk",
        "performance_risk",
        "balance_risk",
        "notes",
    ]
    with (OUT / "mod_feature_index.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        for jar in sorted(analyses, key=lambda j: j.jar_name.lower()):
            writer.writerow(mod_row(jar))


def write_dependency_report(analyses, dep_findings, presence):
    mandatory = []
    optional = []
    for jar in analyses:
        for dep in jar.deps:
            if dep.get("modId") in {"minecraft", "forge", "java", "neoforge"}:
                continue
            row = [jar.primary_name, jar.jar_name, dep.get("modId"), dep.get("versionRange"), dep.get("side"), "obligatoria" if dep.get("mandatory") else "opcional"]
            if dep.get("mandatory"):
                mandatory.append(row)
            else:
                optional.append(row)
    location_mismatch = []
    for mid, locs in sorted(presence.items()):
        if locs == {"client"}:
            location_mismatch.append((mid, "Solo cliente"))
        elif locs == {"server"}:
            location_mismatch.append((mid, "Solo servidor"))
    version_rows = []
    for jar in analyses:
        flags = version_flags(jar)
        if flags:
            version_rows.append((jar.jar_name, jar.primary_name, short_list(flags, 5)))
    client_in_server = [(j.jar_name, j.primary_name, j.side) for j in analyses if j.location == "server" and j.side == "Client only"]
    gameplay_client_only = [(j.jar_name, j.primary_name, short_list(j.categories, 4)) for j in analyses if j.location == "client" and j.side == "Both"]
    lines = []
    lines.append("# Reporte de dependencias\n")
    lines.append("Extraido desde `META-INF/mods.toml`/`neoforge.mods.toml` cuando existe. Dependencias de Minecraft/Forge/Java se omiten de las tablas largas.\n")
    lines.append("## Dependencias obligatorias\n")
    lines.append(table(["Mod", "Jar", "Dependencia", "Version range", "Side", "Tipo"], mandatory[:500]) if mandatory else "No confirmado")
    lines.append("\n\n## Dependencias opcionales\n")
    lines.append(table(["Mod", "Jar", "Dependencia", "Version range", "Side", "Tipo"], optional[:500]) if optional else "No confirmado")
    lines.append("\n\n## Dependencias faltantes/desalineadas\n")
    lines.append(table(["Jar", "Dependencia", "Hallazgo"], [(j.jar_name, f"{d.get('modId')} {d.get('versionRange')}", reason) for j, d, reason in dep_findings]) if dep_findings else "No se detectaron obligatorias faltantes por metadata.")
    lines.append("\n\n## Mod IDs presentes solo en un lado\n")
    lines.append(table(["Mod ID", "Presencia"], location_mismatch[:500]) if location_mismatch else "No confirmado")
    lines.append("\n\n## Posibles NeoForge o versiones distintas\n")
    lines.append(table(["Jar", "Mod", "Flag"], version_rows) if version_rows else "No se detectaron flags claros.")
    lines.append("\n\n## Posibles client-side en server\n")
    lines.append(table(["Jar", "Mod", "Lado inferido"], client_in_server) if client_in_server else "No se detectaron candidatos claros.")
    lines.append("\n\n## Posibles gameplay/server-side solo en cliente\n")
    lines.append(table(["Jar", "Mod", "Categorias"], gameplay_client_only) if gameplay_client_only else "No se detectaron candidatos claros.")
    (OUT / "mod_dependency_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_important_findings(analyses, dep_findings):
    def score_importance(j):
        score = 0
        score += 5 if j.worldgen_risk == "Alto" else 3 if j.worldgen_risk == "Medio" else 0
        score += 3 if "Bosses" in j.categories else 0
        score += 3 if "Dimensiones" in j.categories else 0
        score += 2 if "Estructuras" in j.categories else 0
        score += min(3, len(j.entities) // 30)
        score += min(3, len(j.structures) // 40)
        return score

    top_important = sorted(analyses, key=score_importance, reverse=True)[:10]
    top_wg = sorted([j for j in analyses if j.worldgen_risk != "Bajo" or j.structures], key=lambda j: ({"Alto": 0, "Medio": 1, "Bajo": 2}[j.worldgen_risk], -len(j.structures), j.primary_name))[:10]
    top_perf = sorted(analyses, key=lambda j: ({"Alto": 0, "Medio": 1, "Bajo": 2}.get(j.performance_risk, 2), -len(j.entities), -j.file_size))[:10]
    top_balance = sorted(analyses, key=lambda j: ({"Alto": 0, "Medio": 1, "Bajo": 2}.get(j.balance_risk, 2), -j.counts["loot_tables"], -len(j.entities)))[:10]
    before_final = [j for j in analyses if j.worldgen_risk in {"Alto", "Medio"} or j.balance_risk == "Alto" or j.performance_risk == "Medio"][:60]
    possible_pause = [j for j in analyses if j.errors or version_flags(j) or (j.location == "server" and j.side == "Client only") or (j.location == "client" and j.side == "Both")]
    redundant = [j for j in analyses if "Compatibilidad" in j.categories and "lootintegration" in norm_name(j.jar_name)]
    manual = []
    for j, d, reason in dep_findings:
        manual.append((j.jar_name, j.primary_name, f"Dependencia: {d.get('modId')} - {reason}"))
    for j in possible_pause:
        manual.append((j.jar_name, j.primary_name, short_list(j.errors + version_flags(j) + j.notes, 5)))

    def simple_rows(items):
        return [(j.primary_name, j.jar_name, short_list(j.categories, 4), j.worldgen_risk, j.performance_risk, j.balance_risk) for j in items]

    lines = []
    lines.append("# Hallazgos importantes\n")
    lines.append("Documento corto para decidir que revisar antes del mundo final.\n")
    lines.append("## Top 10 mods mas importantes del pack\n")
    lines.append(table(["Mod", "Jar", "Categorias", "Worldgen", "Rendimiento", "Balance"], simple_rows(top_important)))
    lines.append("\n\n## Top 10 mas riesgosos para worldgen\n")
    lines.append(table(["Mod", "Jar", "Categorias", "Worldgen", "Rendimiento", "Balance"], simple_rows(top_wg)))
    lines.append("\n\n## Top 10 mas riesgosos para rendimiento\n")
    lines.append(table(["Mod", "Jar", "Categorias", "Worldgen", "Rendimiento", "Balance"], simple_rows(top_perf)))
    lines.append("\n\n## Top 10 mas riesgosos para balance\n")
    lines.append(table(["Mod", "Jar", "Categorias", "Worldgen", "Rendimiento", "Balance"], simple_rows(top_balance)))
    lines.append("\n\n## Mods que si o si deben probarse antes del mundo final\n")
    lines.append(table(["Mod", "Jar", "Categorias", "Worldgen", "Rendimiento", "Balance"], simple_rows(before_final[:40])))
    lines.append("\n\n## Mods que podrian eliminarse o pausarse\n")
    lines.append(table(["Jar", "Mod", "Motivo"], [(j.jar_name, j.primary_name, short_list(j.errors + version_flags(j) + j.notes, 5) or "Requiere decision manual") for j in possible_pause[:80]]) if possible_pause else "No hay candidatos claros.")
    lines.append("\n\n## Mods redundantes\n")
    lines.append("Los Loot Integrations son complementarios, no necesariamente redundantes. Se listan para verificar que cada uno corresponda a un mod presente.\n")
    lines.append(table(["Jar", "Mod", "Notas"], [(j.jar_name, j.primary_name, short_list(j.notes, 3) or "Compatibilidad/loot") for j in redundant]) if redundant else "No confirmado")
    lines.append("\n\n## Mods que requieren revision manual\n")
    lines.append(table(["Jar", "Mod", "Motivo"], manual[:120]) if manual else "No se detectaron hallazgos criticos por metadata.")
    (OUT / "important_findings.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    analyses, server, client, shared_names, server_only, client_only = collect_jars()
    presence, _ = build_presence_by_modid(analyses)
    dep_find = dependency_findings(analyses, presence)
    project_summary = scan_allowed_project_files()
    log_summary = scan_recent_logs()

    write_pack_analysis(analyses, server, client, shared_names, server_only, client_only, dep_find, project_summary, log_summary)
    write_content_summary(analyses)
    write_worldgen_impact(analyses)
    write_balance_risk(analyses)
    write_csv(analyses)
    write_dependency_report(analyses, dep_find, presence)
    write_important_findings(analyses, dep_find)

    total_structures = sum(len(set(j.structures)) for j in analyses)
    total_bosses = sum(len(set(j.boss_confirmed + j.boss_probable)) for j in analyses)
    total_dims = sum(len(set(j.dimensions + j.dimension_types)) for j in analyses)
    total_biomes = sum(len(set(j.biomes)) for j in analyses)
    high_risks = [j for j in analyses if j.worldgen_risk == "Alto" or j.balance_risk == "Alto" or j.performance_risk == "Alto"]
    print("Analisis TecMC completado")
    print(f"Total jars analizados: {len(analyses)}")
    print(f"Server jars: {len(server)}")
    print(f"Client jars: {len(client)}")
    print(f"Total estructuras detectadas: {total_structures}")
    print(f"Total bosses confirmados/probables: {total_bosses}")
    print(f"Total dimensiones detectadas: {total_dims}")
    print(f"Total biomas detectados: {total_biomes}")
    print(f"Riesgos altos encontrados: {len(high_risks)}")
    print("Archivos generados:")
    for name in [
        "pack_analysis.md",
        "content_summary.md",
        "worldgen_impact.md",
        "balance_risk_report.md",
        "mod_feature_index.csv",
        "mod_dependency_report.md",
        "important_findings.md",
    ]:
        print(f"- {OUT / name}")


if __name__ == "__main__":
    main()
