import desprotetor
import unittest


class desprotetorSimpleTestCase(unittest.TestCase):
    def setUp(self):
        desprotetor.app.config['TESTING'] = True
        self.app = desprotetor.app.test_client()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1',
                             'HTTP_REFERER': 'http://desprotetor.com/',
                             'HTTP_USER_AGENT': "Chrome"}

    def tearDown(self):
        # se precisar de algum ajuste no final dos testes
        pass

    # casos simples
    def test_response_from_empty_list(self):
        data = {"data": ""}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert "[]" in result.data

    def test_response_from_simple_url_param(self):
        data = {"data": "http://www.test.com.br?url=http://www.correct.com"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.test.com.br?blag=xkcd&enourmousparametername=http://www.correct.com&url=test&test=1"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_reversed_url_param(self):
        data = {"data": "http://www.bolosetortas.info/bolodelimao/?url=lmth.bvmr.geL.DB.VdEO2FM/tz6iarpt/selif/moc.erahskaerf//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://freakshare.com/files/tprai6zt/MF2OEdV.BD.Leg.rmvb.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_reversed_no_url(self):
        data = {"data": "lmth.rar.RCSMMM0B0DAL/3719gyqu/selif/moc.erahstib//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://bitshare.com/files/uqyg9173/LAD0B0MMMSCR.rar.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_multiple_simple_url_param(self):
        data = {"data": "http://www.test.com.br?url=http://www.correct.com\nhttp://www.test.com.br?url=http://www.correct.com"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}, {"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_blocked_domain(self):
        # bug - filter for www.link-protegido.com not working
        #data = {"data": "http://www.test.com.br?url=http://www.link-protegido.com"}
        #expected_response = """[{"dep": 0, "url": "http://www.test.com.br?url=http://www.link-protegido.com"}]"""
        #result = self.app.post('/', data=data, environ_base=self.environ_base)
        #assert expected_response == result.data

        data = {"data": "http://www.test.com.br?url=http://desprotetordelink.com"}
        expected_response = """[{"dep": 0, "url": "http://www.test.com.br?url=http://desprotetordelink.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_unnanounced_decoy_base64(self):
        data = {"data": "http://www.buskaqui.in/protetoradsense2//pd/aHR0cDovL/687474703a2f2f747572626f6269742e6e65742f6b3472796b626f39347830692e68746d6c"}
        expected_response = """[{"dep": 1, "url": "http://turbobit.net/k4rykbo94x0i.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_direct_strings_no_url(self):
        data = {"data": "68747470733a2f2f646c2e64726f70626f782e636f6d2f752f36373333343230342f4754412532305341253230416476616e6365642532304d6f64732f417765736f6d652532302e49465025323056332e726172"}
        expected_response = """[{"dep": 1, "url": "https://dl.dropbox.com/u/67334204/GTA%20SA%20Advanced%20Mods/Awesome%20.IFP%20V3.rar"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "aHR0cDovL2Fkdi5saS83MzkwL2h0dHA6Ly95YWRpLnNrL2QvN19YbWJTSkEwQUprMQ=="}
        expected_response = """[{"dep": 1, "url": "http://adv.li/7390/http://yadi.sk/d/7_XmbSJA0AJk1"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "QmFpeGFyIEZpbG1lIERldG9uYSBSYWxwaCAgRHVibGFkb3xodHRwOi8vYml0c2hhcmUuY29tL2ZpbGVzL3Y0NjgzanB5L0RSYWxwLlI1LkQuQS5hdmkuaHRtbA="}
        expected_response = """[{"dep": 1, "url": "http://bitshare.com/files/v4683jpy/DRalp.R5.D.A.avi.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data


class desprotetorResponseTestCase(unittest.TestCase):
    def setUp(self):
        desprotetor.app.config['TESTING'] = True
        self.app = desprotetor.app.test_client()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1',
                             'HTTP_REFERER': 'http://desprotetor.com/',
                             'HTTP_USER_AGENT': "Chrome"}

    def tearDown(self):
        # se precisar de algum ajuste no final dos testes
        pass

    def test_predefined_response(self):
        data = {"data": "http://desprotetor.com/"}
        expected_response = """[{"dep": 2, "url": "http://desprotetor.com/", "mess": "Esta URL n&atilde;o &eacute; um protetor de links. Procure nao tentar desproteger o desprotetor. =)"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.example.com/"}
        expected_response = """[{"dep": 3, "url": "http://www.example.com/", "mess": "nao parece um protetor"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": ""}
        expected_response = """[]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data


class desprotetorSeparatorTestCase(unittest.TestCase):
    def setUp(self):
        desprotetor.app.config['TESTING'] = True
        self.app = desprotetor.app.test_client()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1',
                             'HTTP_REFERER': 'http://desprotetor.com/',
                             'HTTP_USER_AGENT': "Chrome"}

    def tearDown(self):
        # se precisar de algum ajuste no final dos testes
        pass

    # casos com separadores
    def test_response_separator(self):
        data = {"data": "http://filmeslegendados.info/?http://www.correct.com"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://dicasedicas.info/go/protetor/?8bfwxktq/ot.lu//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://ul.to/qtkxwfb8"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://gta.nafaixa.com.br/link-download/pd/aHR0cDovL/68747470733a2f2f646c2e64726f70626f782e636f6d2f752f36373333343230342f4754412532305341253230416476616e6365642532304d6f64732f417765736f6d652532302e49465025323056332e726172"}
        expected_response = """[{"dep": 1, "url": "https://dl.dropbox.com/u/67334204/GTA%20SA%20Advanced%20Mods/Awesome%20.IFP%20V3.rar"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_last_separator(self):
        data = {"data": "http://www.vamola.in/&test&test&http://www.correct.com"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_common_separators(self):
        data = {"data": "http://test.test/go!http://www.correct.com"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://test.test|http://www.correct.com"}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://test.test//download/?http://www.correct.com"}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://test.test?down!http://www.correct.com"}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://test.test?down!http://www.correct.com"}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.dicasgratisnanet.net/driversprotetor//p/protcaHR0cDovL/aHR0cDovL3d3dy5wb3NpdGl2b2luZm9ybWF0aWNhLmNvbS5ici9zdXBvcnRlcG9zaXRpdm8vZHJpdmVycy9kb3dubG9hZC5hc3A/cGFyYW09MjE3OTY5JmZpbGU9MTEwODc5MjRfQ1JEX1dJTjdfeDY0XzAwLmV4ZQ=="}
        expected_response = """[{"dep": 1, "url": "http://www.positivoinformatica.com.br/suportepositivo/drivers/download.asp?param=217969&file=11087924_CRD_WIN7_x64_00.exe"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_remove_string_then_get_after_separator(self):
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        data = {"data": "http://superdownsmega.paginadedownload.info/http://www.cor.urlrect.com"}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://superdownsmega.paginadedownload.info/http://www.cor.urlrect.com"}
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data


class desprotetorTransformationTestCase(unittest.TestCase):
    def setUp(self):
        desprotetor.app.config['TESTING'] = True
        self.app = desprotetor.app.test_client()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1',
                             'HTTP_REFERER': 'http://desprotetor.com/',
                             'HTTP_USER_AGENT': "Chrome"}

    def tearDown(self):
        # se precisar de algum ajuste no final dos testes
        pass

    # casos simples + transofmacao
    def test_response_from_hex_url_param(self):
        data = {"data": "http://www.baixeadrenalina.com/protetor/?id=687474703a2f2f62697473686172652e636f6d2f66696c65732f30367474776f6e6d2f5355502e5430352e4530312e2d2e4475616c2e417564696f2e7261722e68746d6c"}
        expected_response = """[{"dep": 1, "url": "http://bitshare.com/files/06ttwonm/SUP.T05.E01.-.Dual.Audio.rar.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_dirty_base64_url_param(self):
        data = {"data": "http://www.baixarfilmesdublados.info/baixar/?url=QmFpeGFyIEZpbG1lIEEgQ2FzYSBEb3MgU29uaG9zICBEdWJsYWRvfGh0dHA6Ly91bC50by94a2E4cjkybi9BQ2RTLkJELkR1Yi5ybXZi"}
        expected_response = """[{"dep": 1, "url": "http://ul.to/xka8r92n/ACdS.BD.Dub.rmvb"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.klumag.net/ids/id35/baixar?lnk=QmFpeGFyIEZpbG1lIFBvbGljaWFsIEVtIEFwdXJvcyAgRHVibGFkb3xodHRwOi8vdXBsb2FkZWQubmV0L2ZpbGUvZDZwdTdhNjE="}
        expected_response = """[{"dep": 1, "url": "http://uploaded.net/file/d6pu7a61"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_clean_base64_url_param(self):
        data = {"data": "http://gospel.ebaixar.com/?ID!aHR0cDovL3d3dy40c2hhcmVkLmNvbS9yYXIvS1hOYWQzdi0vR09TUEVMX01VU0lDQV9VTklURURfXzIwMTNfcGFyLmh0bWw="}
        expected_response = """[{"dep": 1, "url": "http://www.4shared.com/rar/KXNad3v-/GOSPEL_MUSICA_UNITED__2013_par.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://redirecionardownbt.com/index.php?url=aHR0cDovL2Fkdi5saS83MzkwL2h0dHA6Ly95YWRpLnNrL2QvN19YbWJTSkEwQUprMQ=="}
        expected_response = """[{"dep": 1, "url": "http://adv.li/7390/http://yadi.sk/d/7_XmbSJA0AJk1"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.agaleradodownload.com/download/?id=687474703a2f2f6465706f73697466696c65732e636f6d2f66696c65732f63376f616f39317375"}
        expected_response = """[{"dep": 1, "url": "http://depositfiles.com/files/c7oao91su"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_safety_reverse_params(self):
        data = {"data": "http://www.celularbr.com/seven/?NP129KKT=d?/moc.daolpuagem.www//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://www.megaupload.com/?d=TKK921PN"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.celularbr.com/seven/?url=NP129KKT=d?/moc.daolpuagem.www//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://www.megaupload.com/?d=TKK921PN"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        # BUG
        '''
        data = {"data": "http://www.celularbr.com/seven/?ah=NP129KKT=d?/moc.daolpuagem.www//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://www.megaupload.com/?d=TKK921PN"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data
        '''

    def test_dirty_param(self):
        data = {"data": "http://www.linkstw.com/sh/protetor.php?link=Z@E$5KGwNWa/elif/moc.evreselif.www//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://www.fileserve.com/file/aWNwGK5"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data
    
    def test_simple_replace(self):
        data = {"data": "http://www.hitsmp3.net/cds-download.php?id=8500"}
        expected_response = """[{"dep": 1, "url": "http://www.hitsmp3.net/cds-liberado.php?id=8500"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://filmeseserieshd.com/fs/protetor.php?link=Z@E$lmth.50x2seisiaDgnihsuP/8f64a7dc/42481127/elif/moc.derahs4.www//:ptth"}
        expected_response = """[{"dep": 1, "url": "http://www.4shared.com/file/72118424/cd7a46f8/PushingDaisies2x05.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_response_from_dirty_base64_no_url(self):
        data = {"data": "RG93bmxvYWQgRGUgUGVybmFzIFBybyBBciAyfGh0dHA6Ly9saW5rcHJvdGVnaWRvLmluZm8vcmVkaXJlY2lvbmFyLz91cmw9aHR0cDovL3llc3MubWUvaXIvaWQvYUhSMGNEb3ZMM0JoYzNSbFltbHVMbU52YlM5elF6aENNMEZqZUE9PS8"}
        expected_response = """[{"dep": 1, "url": "http://yess.me/ir/id/aHR0cDovL3Bhc3RlYmluLmNvbS9zQzhCM0FjeA==/"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "Um9sbGluZyBTdG9uZXMgIEdyZWF0ZXN0IEhpdHN8aHR0cHM6Ly9ob3RmaWxlLmNvbS9kbC8xNzczNjg4NzMvNzdiYTcxYS90aGVyZWJlbHMubmVja2VsNDkucmFyLmh0bWw="}
        expected_response = """[{"dep": 1, "url": "https://hotfile.com/dl/177368873/77ba71a/therebels.neckel49.rar.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_base64_with_pipe_separator(self):
        data = {"data": "http://www.loucosporsoftwares.com/lps/protetor/?url=VGhlIFdhbGtpbmcgRGVhZDogU3Vydml2YWwgSW5zdGluY3QgIFJlbG9hZGVkfGh0dHA6Ly9zaGFyZWZpbGVzLmNvL3ZxMnlqOGl3dHp6by9SRUxUV0RTMS5wYXJ0NC5yYXIuaHRtbA=="}
        expected_response = """[{"dep": 1, "url": "http://sharefiles.co/vq2yj8iwtzzo/RELTWDS1.part4.rar.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data


class desprotetorFetchTestCase(unittest.TestCase):
    def setUp(self):
        desprotetor.app.config['TESTING'] = True
        self.app = desprotetor.app.test_client()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1',
                             'HTTP_REFERER': 'http://desprotetor.com/',
                             'HTTP_USER_AGENT': "Chrome"}

    def tearDown(self):
        # se precisar de algum ajuste no final dos testes
        pass

    # casos com get + captura via regex
    def test_get_result_with_regex_get(self):
        data = {"data": "http://www.centrodedownload.com/2013/02/avenging-angel.html"}
        expected_response = """[{"dep": 1, "url": "http://www.multiupload.nl/9017CUC7AV"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.pqueno.com/?a0kjC"}
        expected_response = """[{"dep": 1, "url": "http://www.gigasize.com/get.php?d=zzdrym6mz8b"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.lockurl.org/YuxW13"}
        expected_response = """[{"dep": 1, "url": "http://oron.com/hc7j185ibssd/AH_Final_Fantasy_VII_Advent_Children_Complete_5BBD_5D.part01.rar.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://link-protector.com/x-88356"}
        expected_response = """[{"dep": 1, "url": "http://rapidshare.com/files/215142479/1996_-_Venus_Isle.rar"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://linkprotegido.info/2s/ID/?a985"}
        expected_response = """[{"dep": 1, "url": "http://depositfiles.com/files/t1xm9vyh2"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        #offline
        #data = {"data": "http://adv.li/5r2"}
        #expected_response = """[{"dep": 1, "url": "http://www.galeria.tesaohq.com/2012/06/celia-iniciacao-sexual-de-uma-ninfeta.html"}]"""
        #result = self.app.post('/', data=data, environ_base=self.environ_base)
        #assert expected_response == result.data

        data = {"data": "http://www.centrodedownload.com/2011/10/assassins-creed-hd.html"}
        expected_response = """[{"dep": 1, "url": "http://www.mediafire.com/?r8umm5qq2xnzzmk"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data
    
    # offline
    #def test_get_result_with_regex_get_base64(self):
    #    data = {"data": "http://assistirfilmesonline.biz/sem-voce-bin-laden-legendado/"}
    #    expected_response = """[{"dep": 1, "url": "http://www.videobb.com/watch_video.php?v=y8lFnRhzOY05"}]"""
    #    result = self.app.post('/', data=data, environ_base=self.environ_base)
    #    assert expected_response == result.data

    def test_get_result_with_regex_rebuild_url(self):
        data = {"data": "http://adf.ly/T5aAc"}
        expected_response = """[{"dep": 1, "url": "http://www.predicta.net"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://adf.ly/RFKCZ"}
        expected_response = """[{"dep": 1, "url": "http://www37.zippyshare.com/v/46543982/file.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data
    
    # offline
    #def test_change_url_get_regex(self):
    #    data = {"data": "http://assistirfilmesonline.net/pub-filme-furia-sobre-rodas-dublado.html"}
    #    expected_response = """[{"dep": 1, "url": "http://videobb.com/e/W42vRjRg57wz"}]"""
    #    result = self.app.post('/', data=data, environ_base=self.environ_base)
    #    assert expected_response == result.data

    # casos especificos
    def test_time_lapse_double_regex_get(self):
        data = {"data": "http://www.link-protegido.com/semprefilmesv2/?link=6HCZL0W01X"}
        expected_response = """[{"dep": 1, "url": "http://uploaded.net/file/dmoy47yu"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.link-protegido.com/semprefilmesv2/?link=CCKIT94P73"}
        expected_response = """[{"dep": 1, "url": "http://bitshare.com/files/650rpa4a/Sev2n.Os.Set5.Cr1m3s.Cap1tai5.Dubl2d-.mkv.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data


class desprotetorSpecialTestCase(unittest.TestCase):
    def setUp(self):
        desprotetor.app.config['TESTING'] = True
        self.app = desprotetor.app.test_client()
        self.environ_base = {'REMOTE_ADDR': '127.0.0.1',
                             'HTTP_REFERER': 'http://desprotetor.com/',
                             'HTTP_USER_AGENT': "Chrome"}

    def tearDown(self):
        # se precisar de algum ajuste no final dos testes
        pass

    def test_decoy_parameter(self):
        data = {"data": "http://36.baixevipdown.net/?test=http://www.incorrect.com&url=http://www.correct.com&?test2=http://www.incorrect.com"}
        expected_response = """[{"dep": 1, "url": "http://www.correct.com"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_cypher_even_odd(self):
        data = {"data": "http://protetor.downloadcdsgratis.com/?url=UhTt3tUpG:N/S/Vw=wdw?./mmeogca.udpalo&t=2"}
        expected_response = """[{"dep": 1, "url": "http://www.megaupload.com/?d=VSNGU3TU"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_base64_rotate(self):   # 23/03/2013
        data = {"data": "http://www.baixandolegal.org/d/index3.php?l=aC9pdi9XdHdsZWZ1dHdlLmllcHdzY2w1Oi5lb2V4L2ZybS9FWA"}
        expected_response = """[{"dep": 1, "url": "http://www.fileserve.com/file/Wue5xEX"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.baixandolegal.org/d/index3.php?l=aHdpbDZkcnVjdC5jZTFvZ2RodGYuLy9sLmkucGljNWJlYm5UOmxvMmFneWhCL2VtMWlhLm9CL3MvMHhsQ0xUd29mMmEubGUud25pNW5vYWUwMi4wNS5ybXZi"}
        expected_response = """[{"dep": 1, "url": "http://www.filesonic.com/file/52102561/baixandolegal.org.by.ClaudinhoLeech.TBBT.02.05.rmvb"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.baixandolegal.org/d/index3.php?l=aGlhZWlMLnV0YmRqZDJMYnRlLmhtLlAucHJjMi9CYXI6dW9pU0RybS9wbTdIUmt2L2wvajNpLmJmbzFiUnBELmh0bWw="}
        expected_response = """[{"dep": 1, "url": "http://fiberupload.com/1ejh2i7jbidm/SH3RL2.BDRip.LPark.Dub.rmvb.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

        data = {"data": "http://www.baixandolegal.org/d/index3.php?l=YUhCakx6UXlZUzVzZEdsdk1pOHdiR0psZEdSdE9FOHdhV0ZuY0hNdk5XWXpkR2xoT21obU0yWXVaWGhzTDJGcE9XbDFYMkV1TDNKc01HTnNkMjV2Y21WbE5HVjBkMlJ5WVM1ek1DNXlkMjluTG5KaGNnPT0="}
        expected_response = """[{"dep": 1, "url": "http://rapidshare.com/files/285390404/Office.2003.ultralite_www.baixandolegal.org.rar"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_dirty_hex_hopping(self):    # found by 70074074068 string
        data = {"data": "http://www.sitesmundo.net/baixar/linkBV/index1.php?link=4142434445464748494A4B4C4F4D4E4F5051525354555758595A&location=06c06d07406802e05304105204204f04104904e05507707707705f02d05f06507006d06104305f06106907204605f06e06906b05302f06d03305107006b06206d06802f06506c06906602f06d06f06302e06406507206106807303402e07707707702f02f03a070074074068"}
        expected_response = """[{"dep": 1, "url": "http://www.4shared.com/file/hmbkpQ3m/Skin_Fria_Campe_-_wwwUNIAOBRAS.html"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_even_cycle_cypher(self):
        data = {"data": "http://protetor.download-jogo.com/v2/?url=kjhUhTt3tUpG:N/S/Vw=wdw?./mmeogca.udpalokjh&t=2"}
        expected_response = """[{"dep": 1, "url": "http://www.megaupload.com/?d=VSNGU3TU"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data

    def test_simple_substitute_cypher(self):
        data = {"data": "http://www.protetor.org/baixar.php?h=m4479uu-j7x.n4pnaj.g0xtupnaj.u08ph_6/aa"}
        expected_response = """[{"dep": 1, "url": "http://depositfiles.com/files/cwfxkrzll"}]"""
        result = self.app.post('/', data=data, environ_base=self.environ_base)
        assert expected_response == result.data


if __name__ == '__main__':
    unittest.main(verbosity=5)
