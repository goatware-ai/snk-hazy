"""Import every check module so the registry is populated.

Module order here is registration order, which is the run order inside each group
(core.GROUP_ORDER fixes the group order). Add a new check module to this list and it is
picked up by both entry points.
"""
from .prompt_inputs import prompt_frame, occupation, input_quality, uniqueness  # noqa: F401
from .golden_rubric import (lint, rubric_form, negatives, landing, liveness,  # noqa: F401
                            fidelity, leakage, sourcing, conformance)
from .authorship import prose, package, workbook_shape  # noqa: F401
from .packaging import hygiene  # noqa: F401
