# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools,_
from datetime import datetime
import xlwt
import cStringIO
import base64
import xlsxwriter
import contextlib
from odoo.tools import html2plaintext
import lxml
from lxml import etree

class zh_mrp_wizard(models.TransientModel):
    _name = "zh.mrp.wizard"
    _description = "Lanceur Fiches"


    #===============================================================================
    # COLUMNS
    #===============================================================================
    mrp_wz_order_id = fields.Many2one('mrp.production', 'Ordre de fabrication', required = True)
    mrp_wz_worksheet = fields.Binary('Fiche', readonly=True)
    mrp_wz_worksheetname = fields.Char('Fiche', readonly=True)
    mrp_wz_state = fields.Selection([
        ('new', 'New'),
        ('done', 'Done'),], string='State',default='new') 
#     mrp_wz_fiche_fabrication = fields.Boolean('Fiche de FABRICATION',default = True)
#     mrp_wz_fiche_tracabilite = fields.Boolean('Fiche de TRACABILITÉ COMPOSANT',default = True) 
#     mrp_wz_fiche_controle = fields.Boolean('Fiche de CONTROLE',default = True) 
#     mrp_wz_mode = fields.Selection([
#         ('concat', 'Feuille par fiche'),
#         ('eclate', 'Classeur par fiche'),], string='Mode',default='concat')        
    
    @api.multi
    def mrp_wizard_generer_fiches_xslx(self):
        this = self[0]
        output = cStringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)
        order = self.mrp_wz_order_id
        with contextlib.closing(cStringIO.StringIO()) as buf:
            workbook = xlsxwriter.Workbook(buf)
            #===================================================================
            # FICHE DE FABRICATION
            #===================================================================
            worksheet = workbook.add_worksheet("FABRICATION")
            libelle_format = workbook.add_format({'font_size':'8','font_name':'Arial Narrow'})
            titre_format = workbook.add_format({'align': 'center','font_size':'13','bold': True,'font_name':'Arial Narrow'})
            entete_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#A9A9A9','border':1})
            ligne_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','border':1})
            highlight_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#FFFF00','border':0})
            worksheet.set_column('A:A', 9)
            worksheet.set_column('C:C', 12)
            worksheet.set_column('D:D', 12)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 12)
            worksheet.set_column('H:H', 9)
            #------------------------------------------------------------------------------ 
            worksheet.write(0, 0,'Date de lancement :',libelle_format )
            worksheet.write(1, 0,u'N° Commande :' ,libelle_format)
            worksheet.write(2, 0,'Date de livraison :',libelle_format ) 
            worksheet.write(1, 3,'FICHE OF : ',titre_format )
            worksheet.write(1, 4,'',highlight_format )  
            worksheet.write(3, 3,u'N° OF CLIENT :' ,libelle_format) 
            worksheet.write(3, 4,'',highlight_format ) 
            worksheet.write(4, 0,'Code :',libelle_format )
            worksheet.merge_range('C6:E6',order.name, titre_format)
            worksheet.write(5, 5,u'Qté lancée :',libelle_format )  
            worksheet.merge_range('G6:H6',order.product_qty,highlight_format ) 
            worksheet.write(5, 0,'NOTA :',libelle_format ) 
            worksheet.merge_range('B1:C1',order.date_planned_start, highlight_format)
            worksheet.merge_range('B2:C2', order.sale_name, highlight_format)
            worksheet.merge_range('B3:C3', order.date_planned_finished, highlight_format)
            #------------------------------------------------------------------------------
            merge_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#A9A9A9','border':0})
            worksheet.merge_range('A8:C8', u'OPÉRATIONS', merge_format)
            worksheet.merge_range('D8:H8', u'A REMPLIR PAR L’OPÉRATEUR', merge_format)                
            #------------------------------------------------------------------------------ 
            worksheet.write(8, 0,u'N° OP',entete_format)
            worksheet.merge_range('B9:C9',u'Libellés',entete_format) 
            worksheet.write(8, 3,'DATE',entete_format) 
            worksheet.write(8, 4,'MATIN',entete_format) 
            worksheet.write(8, 5,u'APRÈS-MIDI',entete_format) 
            worksheet.write(8, 6,u'Qté',entete_format) 
            worksheet.write(8, 7,'MATR.',entete_format) 
            #------------------------------------------------------------------------------ 
            row = 9
            workorder_ids = order.workorder_ids
            if workorder_ids :
                for workorder in workorder_ids:
#                     worksheet.write(row, 0,workorder.name.decode('utf-8'),ligne_format)
#                     worksheet.merge_range(row,1,row,2,workorder.workcenter_id.name.decode('utf-8'),ligne_format) 
#                     worksheet.write(row, 3,u'………..….',ligne_format) 
#                     worksheet.write(row, 4,u'…..H….. / …..H…..',ligne_format) 
#                     worksheet.write(row, 5,u'…..H….. / …..H…..',ligne_format) 
#                     worksheet.write(row, 6,u'……….',ligne_format) 
#                     worksheet.write(row, 7,u'………..….',ligne_format) 
                    merge = 'A'+str(row+1)+':A'+str(row+6)
                    worksheet.merge_range(merge,workorder.workcenter_id.sequence,ligne_format)
                    merge = 'B'+str(row+1)+':C'+str(row+6)
                    worksheet.merge_range(merge,workorder.name.decode('utf-8'),ligne_format)
                    merge = 'D'+str(row+1)+':D'+str(row+6)
                    worksheet.merge_range(merge,u'………..….\n\n\n………..….\n\n\n',ligne_format)
                    merge = 'E'+str(row+1)+':E'+str(row+6)
                    worksheet.merge_range(merge,u'…..H….. / …..H…..\n\n\n…..H….. / …..H…..\n\n\n…..H….. / …..H…..',ligne_format)
                    merge = 'F'+str(row+1)+':F'+str(row+6)
                    worksheet.merge_range(merge,u'…..H….. / …..H…..\n\n\n…..H….. / …..H…..\n\n\n…..H….. / …..H…..',ligne_format)
                    merge = 'G'+str(row+1)+':G'+str(row+6)
                    worksheet.merge_range(merge,u'………..….\n\n\n………..….\n\n\n',ligne_format)
                    merge = 'H'+str(row+1)+':H'+str(row+6)
                    worksheet.merge_range(merge,u'………..….\n\n\n………..….\n\n\n',ligne_format)                                                                                                                        
                    row+=6                
            #------------------------------------------------------------------------------ 
            row+=1
            merge = 'A'+str(row+1)+':H'+str(row+1)
            worksheet.merge_range(merge,'',ligne_format) 
            row+=1           
            merge = 'A'+str(row+1)+':B'+str(row+1)
            worksheet.merge_range(merge,u'QTÉ EN STOCK',entete_format)
            worksheet.write(row, 2,u'DATE ENTRÉE',entete_format)
            worksheet.write(row, 3,u'TEMPS PRÉVU',entete_format)
            worksheet.write(row, 4,u'TEMPS PASSÉ',entete_format)
            worksheet.write(row, 5,u'ÉCART DE TEMPS',entete_format)
            merge = 'G'+str(row+1)+':H'+str(row+1)
            worksheet.merge_range(merge,u'VISA',entete_format)
            row+=1
            merge = 'A'+str(row+1)+':B'+str(row+2)
            worksheet.merge_range(merge,'',ligne_format)
            merge = 'C'+str(row+1)+':C'+str(row+2)
            worksheet.merge_range(merge,'',ligne_format)
            merge = 'D'+str(row+1)+':D'+str(row+2)
            worksheet.merge_range(merge,'',ligne_format)
            merge = 'E'+str(row+1)+':E'+str(row+2)
            worksheet.merge_range(merge,'',ligne_format)
            merge = 'F'+str(row+1)+':F'+str(row+2)
            worksheet.merge_range(merge,'',ligne_format)                                    
            merge = 'G'+str(row+1)+':H'+str(row+2)
            worksheet.merge_range(merge,'',ligne_format)
            row+=2         
            #------------------------------------------------------------------------------ 
            merge = 'A'+str(row+1)+':H'+str(row+1)
            worksheet.merge_range(merge,u'CONCLUSION ET VISA RESP PROD',entete_format)
            row+=1  
            merge = 'A'+str(row+1)+':H'+str(row+4)
            worksheet.merge_range(merge,'',ligne_format)
            #===================================================================
            # FICHE DE TRACABILITE COMPOSANT
            #===================================================================
            worksheet = workbook.add_worksheet("TRACABILITE COMPOSANT")
            libelle_format = workbook.add_format({'font_size':'8','font_name':'Arial Narrow'})
            titre_format = workbook.add_format({'align': 'center','font_size':'13','bold': True,'font_name':'Arial Narrow'})
            entete_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#A9A9A9','border':1})
            ligne_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','border':1})
            highlight_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#FFFF00','border':0})
            worksheet.set_column('A:A', 9)
            worksheet.set_column('C:C', 12)
            worksheet.set_column('D:D', 12)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 12)
            worksheet.set_column('H:H', 9)
            #------------------------------------------------------------------------------ 
            worksheet.write(0, 0,'Date de lancement :',libelle_format )
            worksheet.write(1, 0,u'N° Commande :' ,libelle_format)
            worksheet.write(2, 0,'Date de livraison :',libelle_format ) 
            worksheet.write(1, 3,'FICHE OF : ',titre_format )
            worksheet.write(1, 4,'',highlight_format )  
            worksheet.write(3, 3,u'N° OF CLIENT :' ,libelle_format) 
            worksheet.write(3, 4,'',highlight_format ) 
            worksheet.write(4, 0,'Code :',libelle_format )
            worksheet.merge_range('C6:E6',order.name, titre_format)
            worksheet.write(5, 5,u'Qté lancée :',libelle_format )  
            worksheet.merge_range('G6:H6',order.product_qty,highlight_format ) 
            worksheet.write(5, 0,'NOTA :',libelle_format ) 
            worksheet.merge_range('B1:C1',order.date_planned_start, highlight_format)
            worksheet.merge_range('B2:C2', order.sale_name, highlight_format)
            worksheet.merge_range('B3:C3', order.date_planned_finished, highlight_format)
            #------------------------------------------------------------------------------
            merge_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#A9A9A9','border':0})
            worksheet.merge_range('A8:A9',u'N° OP',entete_format)
            worksheet.merge_range('B8:D8', u'OPÉRATIONS', merge_format)
            worksheet.merge_range('E8:I8', u'A REMPLIR PAR L’OPÉRATEUR', merge_format)                
            #------------------------------------------------------------------------------ 
            worksheet.write('B9','CODE',entete_format) 
            worksheet.merge_range('C9:D9',u'DÉSIGNATION',entete_format) 
            worksheet.write(8, 4,'TRACE',entete_format) 
            worksheet.write(8, 5,'NOM',entete_format) 
            worksheet.write(8, 6,u'REB. COMPOS.',entete_format) 
            worksheet.write(8, 7,u'REB. En COURS',entete_format) 
            worksheet.write(8, 8,u'RÉPARATION',entete_format) 
            #------------------------------------------------------------------------------ 
            row = 9
            bom = order.bom_id
            if bom :
                bom_line_ids = bom.bom_line_ids
                if  bom_line_ids:
                    for bl in bom_line_ids:
                        worksheet.write(row, 0,bl.operation_id.workcenter_id.sequence,entete_format)
                        worksheet.merge_range(row,1,row,3,bl.operation_id.name.decode('utf-8'),ligne_format) 
                        worksheet.write(row, 4,u'',ligne_format) 
                        worksheet.write(row, 5,u'',ligne_format) 
                        worksheet.write(row, 6,u'',ligne_format)  
                        worksheet.write(row, 7,u'',ligne_format)  
                        worksheet.write(row, 8,u'',ligne_format) 
                        row+=1 
                        worksheet.write(row, 0,bl.product_qty,ligne_format)    
                        worksheet.write(row, 1,bl.product_id.code,ligne_format) 
                        worksheet.merge_range(row,2,row,3,bl.product_id.name,ligne_format)
                        worksheet.write(row, 4,u'',ligne_format) 
                        worksheet.write(row, 5,u'',ligne_format) 
                        worksheet.write(row, 6,u'',ligne_format)  
                        worksheet.write(row, 7,u'',ligne_format)  
                        worksheet.write(row, 8,u'',ligne_format)                         
                        row+=1                
            #------------------------------------------------------------------------------ 
            row+=1
            merge = 'A'+str(row+1)+':I'+str(row+1)
            worksheet.merge_range(merge,u'ANALYSE DES REBUTS',entete_format)
            row+=1  
            merge = 'A'+str(row+1)+':I'+str(row+4)
            worksheet.merge_range(merge,'',ligne_format)            
            row+=4         
            #------------------------------------------------------------------------------ 
            merge = 'A'+str(row+1)+':I'+str(row+1)
            worksheet.merge_range(merge,u'CONCLUSION ET VISA RESP QUALITE',entete_format)
            row+=1  
            merge = 'A'+str(row+1)+':I'+str(row+4)
            worksheet.merge_range(merge,'',ligne_format)
            #===================================================================
            # FICHE DE CONTROLE 
            #===================================================================
            worksheet = workbook.add_worksheet("VERSION")
            libelle_format = workbook.add_format({'font_size':'8','font_name':'Arial Narrow'})
            titre_format = workbook.add_format({'align': 'center','font_size':'13','bold': True,'font_name':'Arial Narrow'})
            entete_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#A9A9A9','border':1})
            ligne_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','border':1})
            highlight_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#FFFF00','border':0})
            worksheet.set_column('A:A', 9)
            worksheet.set_column('C:C', 12)
            worksheet.set_column('D:D', 12)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 12)
            worksheet.set_column('H:H', 9)
            #------------------------------------------------------------------------------ 
            worksheet.write(0, 0,'Date de lancement :',libelle_format )
            worksheet.write(1, 0,u'N° Commande :' ,libelle_format)
            worksheet.write(2, 0,'Date de livraison :',libelle_format ) 
            worksheet.write(1, 3,'FICHE OF : ',titre_format )
            worksheet.write(1, 4,'',highlight_format )  
            worksheet.write(3, 3,u'N° OF CLIENT :' ,libelle_format) 
            worksheet.write(3, 4,'',highlight_format ) 
            worksheet.write(4, 0,'Code :',libelle_format )
            worksheet.merge_range('C6:E6',order.name, titre_format)
            worksheet.write(5, 5,u'Qté lancée :',libelle_format )  
            worksheet.merge_range('G6:H6',order.product_qty,highlight_format ) 
            worksheet.write(5, 0,'NOTA :',libelle_format ) 
            worksheet.merge_range('B1:C1',order.date_planned_start, highlight_format)
            worksheet.merge_range('B2:C2', order.sale_name, highlight_format)
            worksheet.merge_range('B3:C3', order.date_planned_finished, highlight_format)
            #------------------------------------------------------------------------------
            row = 8
            lignes = order.move_raw_ids
            if lignes :
            #------------------------------------------------------------------------------
                merge_format = workbook.add_format({'align': 'center','font_size':'8','bold': True,'font_name':'Arial Narrow','bg_color': '#A9A9A9','border':0})
                worksheet.merge_range('A8:F8', u'GAMME DE CONTRÔLE FINAL', merge_format)
                worksheet.merge_range('G8:H8', u'A REMPLIR PAR L’OPÉRATEUR', merge_format)                 
                bold   = workbook.add_format({'bold': True})
                cell_format = workbook.add_format({'align': 'center',
                                                   'valign': 'vcenter',
                                                   'border': 1})                
                for lg in lignes:
                    note = lg.product_id.zh_mrp_note
                    print'note',note
                    if note:
                        worksheet.merge_range(row, 0,row+4,5,"",cell_format)
                        worksheet.write_rich_string(row, 0,bold,lg.product_id.name,note,cell_format)
                        worksheet.merge_range(row,6,row+4,7,u'',ligne_format) 
                        row+=5
            workbook.close()           
            out = base64.encodestring(buf.getvalue())                    
        filename = 'Fiches'
        extension = 'xlsx'
        name = "%s.%s" % (filename, extension)
        this.write({'mrp_wz_state': 'done', 'mrp_wz_worksheet': out, 'mrp_wz_worksheetname': name})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'zh.mrp.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }            