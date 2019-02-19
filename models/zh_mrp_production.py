# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import float_compare

class MrpProduct(models.Model):
    _inherit = 'product.product'
    #===========================================================================
    # COLUMNS
    #===========================================================================
    zh_mrp_note = fields.Text('Note')

class MrpProduction(models.Model):
    _inherit = 'product.template'
    #===========================================================================
    # COLUMNS
    #===========================================================================
    zh_mrp_note = fields.Text('Note')
    zh_mrp_notes = fields.One2many('mrp.production.note','note_mrp_id',string="Notes")
    
class MrpProductionNote(models.Model):
    _name = 'mrp.production.note'
    #===========================================================================
    # COLUMNS
    #===========================================================================
    note_libelle = fields.Char('Libellé')    
    note_texte = fields.Text('Description') 
    note_mrp_id =  fields.Many2one('mrp.production',string="Ordre de fabrication")