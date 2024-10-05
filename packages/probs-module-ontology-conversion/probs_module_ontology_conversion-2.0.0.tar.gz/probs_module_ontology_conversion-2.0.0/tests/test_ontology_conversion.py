# -*- coding: utf-8 -*-

import pytest
from pathlib import Path

from probs_runner import probs_convert_ontology


def test_converted_rule(working_dir):
    ontology_filename = working_dir / "ontology.nt"
    ontology_rules = working_dir / "ontology_rules.dlog"
    with open(ontology_filename, "wt") as f:
        f.write(
            """
<http://w3id.org/probs-lab/ontology#SoldProduction> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://w3id.org/probs-lab/ontology#Flow> .
            """
            )
    probs_convert_ontology(
        ontology_filename,
        ontology_rules,
        working_dir / "test_converted_rule",
    )
    assert ":Flow[?X] :- :SoldProduction[?X] ." in ontology_rules.read_text()


def test_no_rule(working_dir):
    ontology_filename = working_dir / "ontology.nt"
    ontology_rules = working_dir / "ontology_rules.dlog"
    with open(ontology_filename, "wt") as f:
        f.write(
            """
#No ontology defined in RDF file
            """
            )
    probs_convert_ontology(
        ontology_filename,
        ontology_rules,
        working_dir / "test_no_rule",
    )
    assert ":Flow[?X] :- :SoldProduction[?X] ."  not in ontology_rules.read_text()

        


