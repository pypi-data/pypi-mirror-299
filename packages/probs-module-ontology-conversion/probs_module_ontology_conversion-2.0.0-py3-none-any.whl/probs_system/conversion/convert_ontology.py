"""Run the ontology conversion module.

Usage: python convert_ontology.py [PATH TO ontology.nt]

Writes to the `data` subdirectory in the same directory as this script.
"""

import sys
from probs_runner import probs_convert_ontology
from pathlib import Path
import shutil
import logging

logging.basicConfig(level=logging.DEBUG)


def main(ontology_path):
    here = Path(__file__).parent

    output_dir = here / "data"
    output_dir.mkdir(exist_ok=True, parents=True)

    # Convert the ontology to Datalog rules
    probs_convert_ontology(
        ontology_path,
        output_dir / "probs_ontology_rules.dlog",
    )

    # Duplicate the probs.ttl file so it can be built into the Python package
    shutil.copy(ontology_path, output_dir / "ontology.nt")


if __name__ == "__main__":
    main(sys.argv[1])
    sys.exit(0)
