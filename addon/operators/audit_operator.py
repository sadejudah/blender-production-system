from ..checks.transform_check import run_transform_check

results = run_transform_check()

print("=" * 60)
print("Blender Production System")
print("Transform Inspection")
print("=" * 60)

passes = 0
fails = 0

for result in results:

    if result["status"] == "PASS":
        passes += 1
    else:
        fails += 1

    print(result["object"])
    print("Status:", result["status"])

    for issue in result["issues"]:
        print(" -", issue)

print("=" * 60)
print("PASS:", passes)
print("FAIL:", fails)
print("=" * 60)

self.report(
    {'INFO'},
    f"{passes} Passed | {fails} Failed"
)

return {'FINISHED'}
