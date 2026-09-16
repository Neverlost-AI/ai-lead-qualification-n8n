import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = ROOT / "workflows" / "lead-qualification-demo.json"
data = json.loads(P.read_text(encoding="utf-8"))
raw = P.read_text(encoding="utf-8")

problems = []
nodes = data.get("nodes", [])
names = {n["name"] for n in nodes}

expected_nodes = {
    "When clicking ‘Execute workflow’",
    "Sample Lead",
    "Message a model1",
    "Append row in sheet1",
    "If High Priority",
    "Create a draft1",
}
if names != expected_nodes:
    problems.append(f"unexpected node set: {sorted(names)}")

for source, groups in data.get("connections", {}).items():
    if source not in names:
        problems.append(f"missing source node: {source}")
    for branch in groups.get("main", []):
        for edge in branch:
            if edge["node"] not in names:
                problems.append(f"missing target node: {edge['node']}")

refs = set(re.findall(r"\$\([\"']([^\"']+)[\"']\)", raw))
missing_refs = refs - names
if missing_refs:
    problems.append(f"expressions reference missing nodes: {sorted(missing_refs)}")

ai = next(n for n in nodes if n["name"] == "Message a model1")
opts = ai["parameters"]["options"]["textFormat"]["textOptions"]
if opts.get("type") != "json_schema":
    problems.append("model output is not json_schema")
schema = json.loads(opts.get("schema", "{}"))
if set(schema.get("required", [])) != {"priority", "reason", "recommended_action"}:
    problems.append("schema required fields are wrong")
if schema.get("additionalProperties") is not False:
    problems.append("schema should forbid additional properties")

sheet = next(n for n in nodes if n["name"] == "Append row in sheet1")
mapped = set(sheet["parameters"]["columns"]["value"].keys())
expected_cols = {"Name","Email","Company","Budget","Priority","Reason","Recommended Action"}
if mapped != expected_cols:
    problems.append(f"sheet mappings wrong: {sorted(mapped)}")

cond = next(n for n in nodes if n["name"] == "If High Priority")
left = cond["parameters"]["conditions"]["conditions"][0]["leftValue"]
if ".text.priority" not in left:
    problems.append("High-priority route does not read structured priority")

for forbidden in [
    '"credentials"',
    '"webhookId"',
    '"instanceId"',
    "docs.google.com/spreadsheets/d/",
    "TE5ixTqetsHYaZaX",
    "c9gzfEIn309sL12w",
]:
    if forbidden in raw:
        problems.append(f"public export contains forbidden identifier: {forbidden}")

if problems:
    print("FAIL")
    for p in problems:
        print(" -", p)
    sys.exit(1)

print("PASS lead-qualification-demo.json")
print("PASS connections")
print("PASS structured output schema")
print("PASS Google Sheets mappings")
print("PASS conditional routing")
print("PASS public-export sanitation")
