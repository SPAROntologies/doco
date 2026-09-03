import sys
import json
from pathlib import Path
import requests
from rdflib import Graph

ONTOLOGY_FILE = Path("docs/current/doco.ttl")
FOOPS_API_URL = "https://foops.linkeddata.es/assessOntologyFile"
MIN_FAIR_SCORE = 0.99


def validate_syntax():
    print(f"-> [1/2] Checking local RDF syntax ({ONTOLOGY_FILE})...")
    g = Graph()
    try:
        g.parse(ONTOLOGY_FILE, format="turtle")
        print("✓ RDF Turtle syntax is valid.")
    except Exception as e:
        print(f"✗ RDF parsing error: {e}")
        sys.exit(1)


def validate_fairness():
    print(f"-> [2/2] Running FAIR assessment via FOOPS! API...")

    if not ONTOLOGY_FILE.exists():
        print(f"✗ File not found: {ONTOLOGY_FILE}")
        sys.exit(1)

    headers = {
        "Accept": "application/json"
    }

    try:
        with open(ONTOLOGY_FILE, "rb") as f:
            files = {
                "file": (ONTOLOGY_FILE.name, f, "text/turtle")
            }
            response = requests.post(
                FOOPS_API_URL, 
                files=files, 
                headers=headers, 
                timeout=60
            )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"✗ FOOPS! API request failed: {e}")
        if 'response' in locals() and response is not None:
            print(f"Server response: {response.text}")
        sys.exit(1)

    overall_score = data.get("overall_score", 0.0)
    checks = data.get("checks", [])

    print("\n--- FOOPS! FAIR Assessment Report ---")
    print(f"Overall FAIR Score: {overall_score * 100:.1f}%\n")

    failed_checks = []
    for check in checks:
        title = check.get("title", check.get("id", "Check"))
        status = check.get("status", "unknown")
        category = check.get("principle_id", "FAIR")

        if status == "passed" or check.get("total_passed_tests", 0) > 0:
            print(f"  [✓ PASS] [{category}] {title}")
        else:
            print(f"  [✗ FAIL] [{category}] {title}")
            failed_checks.append(f"[{category}] {title}: {check.get('description', '')}")

    print("-------------------------------------")

    if overall_score < MIN_FAIR_SCORE:
        print(f"\n✗ Quality Gate Failed: FAIR score ({overall_score * 100:.1f}%) is below the minimum threshold ({MIN_FAIR_SCORE * 100:.1f}%).")
        print("\nFailed Checks:")
        for err in failed_checks:
            print(f"  - {err}")
        sys.exit(1)

    print(f"\n✓ FAIR assessment passed successfully ({overall_score * 100:.1f}%).")

if __name__ == "__main__":
    validate_syntax()
    validate_fairness()