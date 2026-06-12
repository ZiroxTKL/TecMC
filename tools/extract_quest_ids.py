from __future__ import annotations

import csv
import json
import re
import time
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MODS_DIR = ROOT / "mods"
DOCS_DIR = ROOT / "docs"

OUT_CSV = DOCS_DIR / "quest_ids_reference.csv"
OUT_REFERENCE_MD = DOCS_DIR / "quest_ids_reference.md"
OUT_SUMMARY_MD = DOCS_DIR / "quest_ids_summary.md"
OUT_ERAS_MD = DOCS_DIR / "quest_ids_by_era_candidates.md"
OUT_WARNINGS_MD = DOCS_DIR / "quest_ids_warnings.md"

CSV_COLUMNS = [
    "modid",
    "type",
    "id",
    "source_file",
    "jar_file",
    "confidence",
    "notes",
]

ALLOWED_TYPES = {
    "item",
    "tag_item",
    "entity_loot_table",
    "chest_loot_table",
    "structure",
    "structure_set",
    "biome",
    "dimension",
    "dimension_type",
    "recipe",
    "advancement",
    "unknown_useful",
}

KEY_MODS = {
    "minecraft",
    "create",
    "irons_spellbooks",
    "iceandfire",
    "alexsmobs",
    "alexscaves",
    "cataclysm",
    "mowziesmobs",
    "aether",
    "aether_redux",
    "twilightforest",
    "betterend",
    "betternether",
    "bclib",
    "graveyard",
    "born_in_chaos",
    "born_in_chaos_v1",
    "aquamirae",
    "fossil",
    "artifacts",
    "relics",
    "simplyswords",
    "bosses_of_mass_destruction",
    "dungeons_arise",
    "dungeons_and_taverns",
    "ctov",
    "galosphere",
    "endrem",
    "waystones",
    "sophisticatedbackpacks",
    "farmersdelight",
    "nethersdelight",
    "ends_delight",
    "spelunkers_charm",
    "advancednetherite",
}

KEY_FILE_HINTS = {
    "create",
    "irons_spellbooks",
    "iceandfire",
    "alexsmobs",
    "alexscaves",
    "cataclysm",
    "mowziesmobs",
    "aether",
    "twilightforest",
    "betterend",
    "betternether",
    "bclib",
    "graveyard",
    "born_in_chaos",
    "aquamirae",
    "fossil",
    "artifacts",
    "relics",
    "simplyswords",
    "bomd",
    "dungeonsarise",
    "dungeons-and-taverns",
    "dungeons_and_taverns",
    "ctov",
    "galosphere",
    "endrem",
    "waystones",
    "sophisticatedbackpacks",
    "farmersdelight",
    "nethersdelight",
    "ends_delight",
    "spelunkers_charm",
    "advancednetherite",
}

BOSS_TERMS = [
    "boss",
    "dragon",
    "worm",
    "golem",
    "leviathan",
    "ignis",
    "netherite",
    "monstrosity",
    "void",
    "lich",
    "champion",
    "hydra",
    "naga",
    "queen",
    "king",
    "emperor",
    "guardian",
    "wither",
    "serpent",
    "sunbird",
    "troll",
    "cyclops",
    "dread",
    "myrmex",
    "ghost",
    "reaper",
    "lord",
    "warden",
    "ancient",
    "cataclysm",
    "hastur",
    "abyss",
    "ender",
]

ERA_RULES = {
    "Era 0 - Supervivencia Primitiva": [
        "wood",
        "log",
        "plank",
        "stone",
        "cobble",
        "coal",
        "charcoal",
        "leather",
        "food",
        "bread",
        "meat",
        "wheat",
        "bed",
        "campfire",
    ],
    "Era 1 - Era del Hierro": [
        "iron",
        "copper",
        "emerald",
        "village",
        "villager",
        "backpack",
        "chest",
        "shield",
    ],
    "Era 2 - Era Mecanica": [
        "create",
        "zinc",
        "brass",
        "andesite",
        "cogwheel",
        "shaft",
        "press",
        "depot",
        "belt",
        "mechanical",
        "contraption",
    ],
    "Era 3 - Era Arcana": [
        "spell",
        "scroll",
        "arcane",
        "magic",
        "rune",
        "lapis",
        "amethyst",
        "ender_pearl",
        "artifact",
        "relic",
    ],
    "Era 4 - Era del Nether": [
        "nether",
        "quartz",
        "blaze",
        "obsidian",
        "netherite",
        "soul",
        "spectral",
        "fortress",
        "bastion",
    ],
    "Era 5 - Era Draconica / Bestial": [
        "dragon",
        "scale",
        "bone",
        "silver",
        "cyclops",
        "troll",
        "serpent",
        "myrmex",
        "mowzie",
        "alex",
        "aquamirae",
        "leviathan",
        "beast",
    ],
    "Era 6 - Era Dimensional": [
        "aether",
        "twilight",
        "betterend",
        "end",
        "dimension",
        "portal",
        "naga",
        "lich",
        "hydra",
        "ur_ghast",
        "queen",
    ],
    "Era 7 - Era del Cataclismo": [
        "cataclysm",
        "ignis",
        "monstrosity",
        "void",
        "abyss",
        "ender",
        "leviathan",
        "netherite",
        "ancient",
        "boss",
    ],
}


@dataclass(frozen=True)
class Row:
    modid: str
    type: str
    id: str
    source_file: str
    jar_file: str
    confidence: str
    notes: str


def ensure_safe_output(path: Path) -> None:
    resolved = path.resolve()
    docs = DOCS_DIR.resolve()
    tools = (ROOT / "tools").resolve()
    if docs not in resolved.parents and tools not in resolved.parents and resolved not in {docs, tools}:
        raise RuntimeError(f"Refusing to write outside docs/tools: {resolved}")


def normalize_mod_key(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")


def normalize_path_no_ext(path: str, prefix: str) -> str:
    rel = path[len(prefix) :]
    if rel.endswith(".json"):
        rel = rel[:-5]
    return rel.strip("/")


def add_row(rows: set[Row], row: Row) -> None:
    if row.type not in ALLOWED_TYPES:
        raise ValueError(f"Unsupported type: {row.type}")
    rows.add(row)


def parse_mods_toml_modids(text: str) -> list[str]:
    modids: list[str] = []
    blocks = re.findall(r"(?ms)^\s*\[\[mods\]\]\s*(.*?)(?=^\s*\[\[|\Z)", text)
    for block in blocks:
        match = re.search(r'(?m)^\s*modId\s*=\s*"([^"]+)"', block)
        if match:
            modids.append(match.group(1).lower())
    return sorted(set(modids))


def read_zip_text(zf: zipfile.ZipFile, name: str) -> str | None:
    try:
        with zf.open(name) as fh:
            return fh.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def collect_json_refs(obj: object) -> set[str]:
    refs: set[str] = set()
    pattern = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")

    def walk(value: object) -> None:
        if isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, str) and pattern.match(value):
            refs.add(value)

    walk(obj)
    return refs


def is_key_jar(jar_name: str, modids: Iterable[str]) -> bool:
    keys = {normalize_mod_key(m).replace("_", "") for m in modids}
    for key in KEY_MODS:
        if normalize_mod_key(key).replace("_", "") in keys:
            return True
    filename_key = normalize_mod_key(jar_name).replace("_", "")
    for hint in KEY_FILE_HINTS:
        if normalize_mod_key(hint).replace("_", "") in filename_key:
            return True
    return False


def classify_entry(name: str, jar_file: str) -> Row | None:
    clean = name.replace("\\", "/")
    parts = clean.split("/")
    if len(parts) < 4 or not clean.endswith(".json"):
        return None

    if len(parts) >= 5 and parts[0] == "assets" and parts[2] == "models" and parts[3] == "item":
        modid = parts[1]
        item = "/".join(parts[4:])[:-5]
        return Row(modid, "item", f"{modid}:{item}", clean, jar_file, "high", "item model")

    if parts[0] == "data":
        namespace = parts[1]
        if len(parts) >= 5 and parts[2] == "loot_tables" and parts[3] == "entities":
            entity = "/".join(parts[4:])[:-5]
            return Row(
                namespace,
                "entity_loot_table",
                f"{namespace}:{entity}",
                clean,
                jar_file,
                "high",
                "entity inferred from loot table",
            )
        if len(parts) >= 5 and parts[2] == "loot_tables" and parts[3] == "chests":
            chest = "/".join(parts[4:])[:-5]
            return Row(
                namespace,
                "chest_loot_table",
                f"{namespace}:{chest}",
                clean,
                jar_file,
                "high",
                "chest loot table",
            )
        if len(parts) >= 5 and parts[2] == "worldgen" and parts[3] == "structure":
            structure = "/".join(parts[4:])[:-5]
            return Row(namespace, "structure", f"{namespace}:{structure}", clean, jar_file, "high", "worldgen structure")
        if len(parts) >= 5 and parts[2] == "worldgen" and parts[3] == "structure_set":
            structure_set = "/".join(parts[4:])[:-5]
            return Row(
                namespace,
                "structure_set",
                f"{namespace}:{structure_set}",
                clean,
                jar_file,
                "high",
                "worldgen structure set",
            )
        if len(parts) >= 5 and parts[2] == "worldgen" and parts[3] == "biome":
            biome = "/".join(parts[4:])[:-5]
            return Row(namespace, "biome", f"{namespace}:{biome}", clean, jar_file, "high", "biome")
        if len(parts) >= 4 and parts[2] == "dimension":
            dimension = "/".join(parts[3:])[:-5]
            return Row(namespace, "dimension", f"{namespace}:{dimension}", clean, jar_file, "high", "dimension")
        if len(parts) >= 4 and parts[2] == "dimension_type":
            dimension_type = "/".join(parts[3:])[:-5]
            return Row(namespace, "dimension_type", f"{namespace}:{dimension_type}", clean, jar_file, "high", "dimension type")
        if len(parts) >= 5 and parts[2] == "tags" and parts[3] == "items":
            tag = "/".join(parts[4:])[:-5]
            return Row(namespace, "tag_item", f"{namespace}:{tag}", clean, jar_file, "high", "item tag")
        if len(parts) >= 4 and parts[2] == "recipes":
            recipe = "/".join(parts[3:])[:-5]
            return Row(namespace, "recipe", f"{namespace}:{recipe}", clean, jar_file, "medium", "recipe id")
        if len(parts) >= 4 and parts[2] == "advancements":
            advancement = "/".join(parts[3:])[:-5]
            return Row(namespace, "advancement", f"{namespace}:{advancement}", clean, jar_file, "medium", "advancement")

    return None


def looks_suspicious_id(identifier: str) -> bool:
    return not re.match(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$", identifier)


def term_matches(identifier: str, terms: Iterable[str]) -> bool:
    low = identifier.lower()
    return any(term in low for term in terms)


def top_rows(rows: Iterable[Row], row_type: str | None = None, limit: int = 30) -> list[Row]:
    selected = [r for r in rows if row_type is None or r.type == row_type]
    return sorted(selected, key=lambda r: (r.modid, r.type, r.id))[:limit]


def markdown_table(headers: list[str], rows: list[list[str]], limit: int | None = None) -> str:
    if limit is not None:
        rows = rows[:limit]
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |")
    if not rows:
        out.append("| _none_ |" + " |".join([""] * (len(headers) - 1)) + " |")
    return "\n".join(out)


def main() -> int:
    started = time.perf_counter()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for path in [OUT_CSV, OUT_REFERENCE_MD, OUT_SUMMARY_MD, OUT_ERAS_MD, OUT_WARNINGS_MD]:
        ensure_safe_output(path)

    rows: set[Row] = set()
    opened_jars = 0
    failed_jars: list[tuple[str, str]] = []
    jars_no_useful: list[str] = []
    jars_no_mods_toml: list[str] = []
    detected_modids_by_jar: dict[str, list[str]] = {}
    json_parse_failures: list[tuple[str, str, str]] = []
    key_json_refs: dict[str, set[str]] = defaultdict(set)
    key_jars: set[str] = set()

    jar_paths = sorted(MODS_DIR.glob("*.jar"), key=lambda p: p.name.lower())
    for jar_path in jar_paths:
        useful_before = len(rows)
        try:
            with zipfile.ZipFile(jar_path) as zf:
                opened_jars += 1
                names = zf.namelist()

                mods_toml = None
                for candidate in ("META-INF/mods.toml", "META-INF/neoforge.mods.toml"):
                    if candidate in names:
                        mods_toml = read_zip_text(zf, candidate)
                        break
                if mods_toml:
                    detected_modids_by_jar[jar_path.name] = parse_mods_toml_modids(mods_toml)
                else:
                    jars_no_mods_toml.append(jar_path.name)
                    detected_modids_by_jar[jar_path.name] = []

                jar_is_key = is_key_jar(jar_path.name, detected_modids_by_jar[jar_path.name])
                if jar_is_key:
                    key_jars.add(jar_path.name)

                for name in names:
                    row = classify_entry(name, jar_path.name)
                    if row:
                        add_row(rows, row)
                        if jar_is_key and row.type in {
                            "entity_loot_table",
                            "chest_loot_table",
                            "recipe",
                            "advancement",
                            "tag_item",
                            "structure",
                            "structure_set",
                            "biome",
                            "dimension",
                            "dimension_type",
                        }:
                            text = read_zip_text(zf, name)
                            if text is not None:
                                try:
                                    data = json.loads(text)
                                    key_json_refs[row.modid].update(collect_json_refs(data))
                                except Exception as exc:
                                    json_parse_failures.append((jar_path.name, name, str(exc)))

                if len(rows) == useful_before:
                    jars_no_useful.append(jar_path.name)
        except Exception as exc:
            failed_jars.append((jar_path.name, str(exc)))

    sorted_rows = sorted(rows, key=lambda r: (r.modid, r.type, r.id, r.jar_file, r.source_file))

    suspicious = [r for r in sorted_rows if looks_suspicious_id(r.id)]
    duplicates_by_id_type: dict[tuple[str, str, str], list[Row]] = defaultdict(list)
    for row in sorted_rows:
        duplicates_by_id_type[(row.modid, row.type, row.id)].append(row)
    duplicate_weird = {
        key: value
        for key, value in duplicates_by_id_type.items()
        if len({(r.jar_file, r.source_file) for r in value}) > 1
    }

    possible_bosses = [
        r
        for r in sorted_rows
        if r.type == "entity_loot_table" and term_matches(r.id, BOSS_TERMS)
    ]
    possible_bosses = sorted(possible_bosses, key=lambda r: (r.modid, r.id))

    structures = [r for r in sorted_rows if r.type in {"structure", "structure_set", "chest_loot_table"}]
    important_structures = [
        r
        for r in structures
        if term_matches(
            r.id,
            [
                "tower",
                "dungeon",
                "village",
                "castle",
                "fortress",
                "temple",
                "grave",
                "catacomb",
                "labyrinth",
                "lair",
                "den",
                "city",
                "crypt",
                "arena",
                "stronghold",
                "palace",
                "ruin",
            ],
        )
    ]

    forge_tags = [
        r
        for r in sorted_rows
        if r.type == "tag_item"
        and r.modid == "forge"
        and term_matches(r.id, ["ores", "ingots", "raw_materials", "gems", "storage_blocks", "nuggets", "dusts"])
    ]

    material_terms = [
        "ore",
        "ingot",
        "nugget",
        "gem",
        "dust",
        "raw",
        "scrap",
        "scale",
        "bone",
        "silver",
        "copper",
        "zinc",
        "brass",
        "netherite",
        "dragon",
        "ender",
        "amethyst",
        "sapphire",
        "ruby",
        "steel",
        "alloy",
    ]
    materials = [r for r in sorted_rows if r.type in {"item", "tag_item", "recipe"} and term_matches(r.id, material_terms)]
    dimensions_biomes = [r for r in sorted_rows if r.type in {"dimension", "dimension_type", "biome"}]

    needs_manual = []
    for row in possible_bosses:
        needs_manual.append(
            Row(row.modid, "unknown_useful", row.id, row.source_file, row.jar_file, "needs_manual_check", "possible boss by name heuristic")
        )
    for ref_modid, refs in key_json_refs.items():
        for ref in sorted(refs):
            if term_matches(ref, material_terms + BOSS_TERMS) and ref.split(":", 1)[0] in KEY_MODS:
                needs_manual.append(
                    Row(ref.split(":", 1)[0], "unknown_useful", ref, "json reference in key mod", "multiple", "needs_manual_check", "referenced by key mod JSON")
                )
    needs_manual = sorted(set(needs_manual), key=lambda r: (r.modid, r.id, r.notes))

    # CSV includes the required direct index plus conservative manual-check references.
    csv_rows = sorted(set(sorted_rows).union(needs_manual), key=lambda r: (r.modid, r.type, r.id, r.jar_file, r.source_file))
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(
                {
                    "modid": row.modid,
                    "type": row.type,
                    "id": row.id,
                    "source_file": row.source_file,
                    "jar_file": row.jar_file,
                    "confidence": row.confidence,
                    "notes": row.notes,
                }
            )

    type_counts = Counter(r.type for r in csv_rows)
    modid_counts = Counter(r.modid for r in csv_rows)
    direct_modid_counts = Counter(r.modid for r in sorted_rows)

    # Reference markdown.
    reference_lines = [
        "# Quest IDs Reference",
        "",
        "This file is a compact index. The complete machine-readable source is `quest_ids_reference.csv`.",
        "",
        f"- Jars analyzed: {opened_jars}",
        f"- Direct IDs extracted: {len(sorted_rows)}",
        f"- CSV rows including manual-check references: {len(csv_rows)}",
        "",
        "## Counts By Type",
        "",
        markdown_table(["type", "count"], [[k, str(v)] for k, v in sorted(type_counts.items())]),
        "",
        "## Top 20 Modids",
        "",
        markdown_table(["modid", "count"], [[k, str(v)] for k, v in modid_counts.most_common(20)]),
        "",
        "## Sample High Confidence Items",
        "",
        markdown_table(["id", "jar", "source"], [[r.id, r.jar_file, r.source_file] for r in top_rows(sorted_rows, "item", 40)]),
        "",
        "## Sample Structures",
        "",
        markdown_table(["id", "type", "jar"], [[r.id, r.type, r.jar_file] for r in top_rows(important_structures, None, 40)]),
        "",
        "## Sample Forge Tags",
        "",
        markdown_table(["id", "jar"], [[r.id, r.jar_file] for r in forge_tags[:60]]),
    ]
    OUT_REFERENCE_MD.write_text("\n".join(reference_lines) + "\n", encoding="utf-8")

    # Era candidates.
    era_lines = [
        "# Quest IDs By Era Candidates",
        "",
        "These are candidates, not final quests. Anything marked `needs_manual_check` should be verified in-game or with JEI/FTB Quests before becoming a hard objective.",
    ]
    for era, terms in ERA_RULES.items():
        era_lines.extend(["", f"## {era}", ""])
        matches = [r for r in csv_rows if term_matches(r.id, terms)]
        categories = {
            "Items": [r for r in matches if r.type == "item"],
            "Tags": [r for r in matches if r.type == "tag_item"],
            "Mobs / Entity Loot Tables": [r for r in matches if r.type == "entity_loot_table"],
            "Bosses / Possible Bosses": [r for r in matches if r.type == "entity_loot_table" and term_matches(r.id, BOSS_TERMS)],
            "Structures": [r for r in matches if r.type in {"structure", "structure_set", "chest_loot_table"}],
            "Dimensions / Biomes": [r for r in matches if r.type in {"dimension", "dimension_type", "biome"}],
            "Needs Manual Check": [r for r in matches if r.confidence == "needs_manual_check"],
        }
        for title, values in categories.items():
            era_lines.extend([f"### {title}", ""])
            era_lines.append(markdown_table(["id", "type", "confidence", "jar"], [[r.id, r.type, r.confidence, r.jar_file] for r in values[:25]]))
            era_lines.append("")
        objective_suggestions = {
            "Era 0 - Supervivencia Primitiva": [
                "Collect basic survival materials.",
                "Craft first food and storage goals.",
                "Use tags for wood, stone, leather, coal and simple food where available.",
            ],
            "Era 1 - Era del Hierro": [
                "Gate backpacks, shields, village trading and iron tools.",
                "Use forge tags for iron/copper/emerald objectives.",
            ],
            "Era 2 - Era Mecanica": [
                "Gate Create by zinc/copper/brass/andesite alloy progression.",
                "Use recipes and item IDs to form machine-building quest chains.",
            ],
            "Era 3 - Era Arcana": [
                "Introduce spells, scrolls, artifacts and relics after basic resources.",
                "Use advancements where present as safer triggers.",
            ],
            "Era 4 - Era del Nether": [
                "Gate Nether materials, blaze/quartz/obsidian and early nether bosses.",
                "Use structures for fortress/bastion style exploration tasks.",
            ],
            "Era 5 - Era Draconica / Bestial": [
                "Use entity loot tables for dragons and strong beasts as manual-check boss candidates.",
                "Gate silver, dragon materials and creature drops.",
            ],
            "Era 6 - Era Dimensional": [
                "Split Aether, Twilight Forest, BetterEnd and End Remastered objectives.",
                "Use dimensions and biomes as exploration candidates.",
            ],
            "Era 7 - Era del Cataclismo": [
                "Reserve Cataclysm and void/end boss IDs for endgame quest lines.",
                "Use boss drops and structures as final progression checks.",
            ],
        }
        era_lines.extend(["### Possible Quest Objectives", ""])
        for suggestion in objective_suggestions.get(era, []):
            era_lines.append(f"- {suggestion}")
    OUT_ERAS_MD.write_text("\n".join(era_lines) + "\n", encoding="utf-8")

    # Summary markdown.
    summary_lines = [
        "# Quest IDs Summary",
        "",
        "## Global Counts",
        "",
        f"- Jars analyzed: {opened_jars}",
        f"- Jars failed to open: {len(failed_jars)}",
        f"- Direct IDs extracted: {len(sorted_rows)}",
        f"- CSV rows including manual-check references: {len(csv_rows)}",
        "",
        "## Count By Type",
        "",
        markdown_table(["type", "count"], [[k, str(v)] for k, v in sorted(type_counts.items())]),
        "",
        "## Count By Modid",
        "",
        markdown_table(["modid", "count"], [[k, str(v)] for k, v in sorted(modid_counts.items())], limit=80),
        "",
        "## Top 20 Modids By Useful IDs",
        "",
        markdown_table(["modid", "count"], [[k, str(v)] for k, v in modid_counts.most_common(20)]),
        "",
        "## Top Relevant Mods For Quests",
        "",
        markdown_table(["modid", "direct id count"], [[m, str(direct_modid_counts[m])] for m in KEY_MODS if direct_modid_counts[m] > 0], limit=60),
        "",
        "## Bosses Or Important Mobs Detected",
        "",
        markdown_table(["id", "confidence", "jar", "source"], [[r.id, "needs_manual_check", r.jar_file, r.source_file] for r in possible_bosses[:80]]),
        "",
        "## Useful Progression Materials",
        "",
        markdown_table(["id", "type", "confidence", "jar"], [[r.id, r.type, r.confidence, r.jar_file] for r in materials[:100]]),
        "",
        "## Important Structures",
        "",
        markdown_table(["id", "type", "jar"], [[r.id, r.type, r.jar_file] for r in important_structures[:100]]),
        "",
        "## Dimensions And Biomes",
        "",
        markdown_table(["id", "type", "jar"], [[r.id, r.type, r.jar_file] for r in dimensions_biomes[:100]]),
        "",
        "## Useful Forge Ore/Material Tags",
        "",
        markdown_table(["id", "jar"], [[r.id, r.jar_file] for r in forge_tags[:100]]),
        "",
        "## IDs With needs_manual_check",
        "",
        markdown_table(["id", "notes"], [[r.id, r.notes] for r in needs_manual[:100]]),
        "",
        "## Warnings",
        "",
        f"- Jars with no useful data/assets entries: {len(jars_no_useful)}",
        f"- Jars without mods.toml/neoforge.mods.toml: {len(jars_no_mods_toml)}",
        f"- JSON parse failures while checking key mods: {len(json_parse_failures)}",
        f"- Suspicious ID/path rows: {len(suspicious)}",
        f"- Duplicate IDs across different source files/jars: {len(duplicate_weird)}",
        "",
        "## Suggested Next Steps",
        "",
        "- Review `quest_ids_by_era_candidates.md` and mark which candidates should become actual FTB Quests.",
        "- Verify possible bosses in-game or with JEI before using them as required objectives.",
        "- Prefer tag objectives for common materials, and direct item IDs for boss drops or unique artifacts.",
        "- Use advancements only where they match the intended progression cleanly.",
    ]
    OUT_SUMMARY_MD.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    # Warnings markdown.
    warnings_lines = [
        "# Quest IDs Warnings",
        "",
        "## Jars That Could Not Be Opened",
        "",
        markdown_table(["jar", "error"], [[jar, err] for jar, err in failed_jars]),
        "",
        "## Jars With No Useful data/assets Entries",
        "",
        "\n".join(f"- `{jar}`" for jar in jars_no_useful) if jars_no_useful else "_none_",
        "",
        "## JSON Parse Failures In Key Mods",
        "",
        markdown_table(["jar", "source", "error"], [[jar, src, err[:160]] for jar, src, err in json_parse_failures[:200]]),
        "",
        "## Duplicate IDs Across Different Sources",
        "",
        markdown_table(
            ["id", "type", "sources"],
            [
                [
                    key[2],
                    key[1],
                    "; ".join(sorted({f"{r.jar_file}:{r.source_file}" for r in values})[:5]),
                ]
                for key, values in list(duplicate_weird.items())[:200]
            ],
        ),
        "",
        "## Suspicious IDs Or Paths",
        "",
        markdown_table(["id", "type", "jar", "source"], [[r.id, r.type, r.jar_file, r.source_file] for r in suspicious[:200]]),
        "",
        "## Modids Not Detected From mods.toml",
        "",
        "\n".join(f"- `{jar}`" for jar in jars_no_mods_toml[:300]) if jars_no_mods_toml else "_none_",
        "",
        "## Manual Review Queue",
        "",
        markdown_table(["id", "notes"], [[r.id, r.notes] for r in needs_manual[:200]]),
    ]
    OUT_WARNINGS_MD.write_text("\n".join(warnings_lines) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - started
    print("Quest ID extraction complete")
    print(f"Jars analyzed: {opened_jars}")
    print(f"IDs found: {len(csv_rows)}")
    print("Files generated:")
    for path in [OUT_CSV, OUT_REFERENCE_MD, OUT_SUMMARY_MD, OUT_ERAS_MD, OUT_WARNINGS_MD]:
        print(f"- {path}")
    print("Top 10 modids:")
    for modid, count in modid_counts.most_common(10):
        print(f"- {modid}: {count}")
    print(f"Possible bosses: {len(possible_bosses)}")
    print(f"Structures: {sum(1 for r in csv_rows if r.type in {'structure', 'structure_set'})}")
    print(f"Useful Forge tags: {len(forge_tags)}")
    print("Warnings:")
    print(f"- failed jars: {len(failed_jars)}")
    print(f"- no useful entries: {len(jars_no_useful)}")
    print(f"- json parse failures: {len(json_parse_failures)}")
    print(f"- suspicious ids: {len(suspicious)}")
    print(f"Elapsed seconds: {elapsed:.2f}")
    print("Confirmed: no mods, datapacks, configs or world files were modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
