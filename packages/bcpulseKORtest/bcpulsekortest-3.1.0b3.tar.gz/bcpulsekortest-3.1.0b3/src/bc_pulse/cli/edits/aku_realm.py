from __future__ import annotations
from bc_pulse import core
from bc_pulse.cli import color


def unlock_aku_realm(save_file: core.SaveFile):
    stage_ids = [255, 256, 257, 258, 265, 266, 268]
    for stage_id in stage_ids:
        save_file.event_stages.clear_map(1, stage_id, 0, False)

    color.ColoredText.localize("aku_realm_unlocked")
