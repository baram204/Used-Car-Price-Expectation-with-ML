from flask import render_template,jsonify, flash, redirect, url_for

from .modelhandler import ModelHandler
from .crawlhandler import CrawlHandler

md = ModelHandler()
cr = CrawlHandler()

class SxjHelper():

    def alert(self, obj_rsp, level, title, message):
        messages = {'level':level, 'title':title, 'message':message}
        alert = render_template('alert_piece.html',messages=messages)
        obj_rsp.html_prepend('#alert',alert)

hp = SxjHelper()

class SijaxHandler(object):

    @staticmethod
    def say_hi(obj_response):
        obj_response.alert('Hi there!')

    @staticmethod
    def search_signle(obj_response, keyword, columns):
        print(columns)
        obj_response.script("$('.alert').hide();")
        aptinfo_list_df = md.get_apt_info_df(keyword, columns)
        # if not aptinfo_list_df.to_dict():
        #     hp.alert(obj_response,'alert-danger','법정동이','없습니다.')
        #     return

        print(aptinfo_list_df)

        # http://www.datasciencemadesimple.com/get-list-column-headers-column-name-python-pandas/
        header = list(aptinfo_list_df)
        print(header)
        rows = aptinfo_list_df.values.tolist()
        print(rows)
        table = render_template('table_piece.html',header= header, rows=rows)
        obj_response.html('#dataTable',table)
        datatable = """
        // Call the dataTables jQuery plugin
        
$('.table-responsive').responsiveTable();
        (function ($, window) {

        new TableExport($('table'), {formats: ['xlsx'], fileName: "contact-list", bootstrap: true})

    }).call(this, jQuery, window);
        
        """
        obj_response.script(datatable)




