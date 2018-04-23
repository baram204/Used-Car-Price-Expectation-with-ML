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
    def search_signle(obj_response, keyword):
        obj_response.script("$('.alert').hide();")
        bjd_list: list = md.get_bjd_list(keyword)
        # hp.alert(obj_response,'alert-info','법정동 목록',bjd_list)
        if not bjd_list:
            hp.alert(obj_response,'alert-danger','법정동이','없습니다.')
            return
        apt_list , bldCode_list = cr.crawl_apt_list(bjd_list)
        # hp.alert(obj_response,'alert-info','아파트 목록',apt_list)
        if not apt_list:
            hp.alert(obj_response,'alert-danger',bjd_list+'법정동에','아파트가 없습니다.')
            return
        # if apt was there, should be apt info.
        # apt_list = apt_list[:1]
        # bjdCode_list = bldCode_list[:1]
        aptinfo_list_df = cr.crawl_apt_info(apt_list, bldCode_list)
        # hp.alert(obj_response,'alert-info','아파트 정보',rows)

        md.insert_all_rows(aptinfo_list_df)

        # http://www.datasciencemadesimple.com/get-list-column-headers-column-name-python-pandas/
        header = list(aptinfo_list_df)
        print(header)
        rows = aptinfo_list_df.values.tolist()
        print(rows)
        table = render_template('table_piece.html',header= header, rows=rows)
        obj_response.html('#dataTable',table)
        datatable = """
        // Call the dataTables jQuery plugin
            $('head').append('<script src="/static/vendor/tablesaw/tablesaw.js"></script>');
            Tablesaw.init();
            $('#dataTable').tablesaw().data("tablesaw").refresh();
        
        """
        obj_response.script(datatable)




