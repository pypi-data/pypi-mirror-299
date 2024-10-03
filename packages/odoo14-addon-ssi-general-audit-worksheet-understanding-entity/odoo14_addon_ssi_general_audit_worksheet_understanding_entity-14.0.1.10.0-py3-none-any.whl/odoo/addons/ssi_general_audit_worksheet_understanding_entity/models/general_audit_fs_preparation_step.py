# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class GeneralAuditFSPreparationStep(models.Model):
    _name = "general_audit_fs_preparation_step"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "General Audit FS Preparation Step"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
