import string
import json
import urllib
import urllib2
from time import sleep
class fmgApi5:
        """ FortiManager Class allowing to perform methods calls to the FortiManager device thru JSON"""
        _httpheaders=None
        _url=None
        _myadom=None
        def __init__(self, fmgip, secure=0):
                _url='http://'
                if secure:
                    _url='https://'
                self._url=_url+fmgip+'/jsonrpc'
                self._httpheaders={"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}

        def _pack_obj_request(self, obj): #creating json objects
                req='{'
                for o in obj:
                        req=req+o+','
                req=req[:len(req)-1] #remove last ','
                req=req+'}'
                return req

        def _pack_lst_request(self, lst): # creating json Arrays
                req='['
                for l in lst:
                        req=req+l+','
                req=req[:len(req)-1]#remove last ','
                req=req+']'
                return req

        def _pack_key_val(self, key, val): # creating name:value pairs
                str1=''
                if val==None:
                        str1='"'+key+'" : null'
                        return str1

                if isinstance(val, int) or isinstance(val, long):#cast value to type string
                        val=str(val)
                        str1='"'+key+'" : '+ val
                        return str1

                str1='"'+key+'" : "'+val+'"'
                return str1

        def _concat_param(self, l1, l2):
                str1=''
                str1='"'+l1+ '" : '+ l2
                return str1

        def _login(self, usrname, passwd, sid, url='sys/login/user'):
                par1=self._pack_key_val('url', url)
                u1=self._pack_key_val('user', usrname)
                u2=self._pack_key_val('passwd', passwd)
                u3=u1+','+u2
                d1=self._pack_obj_request((u3,))
                d2=self._pack_lst_request((d1,))
                d3=self._concat_param('data', d2)
                par1=par1+','+d3
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'exec')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                msg=self._pack_obj_request((line1, line2, line3))
                #print msg
                #print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                obj=json.loads(res)
                if obj['result']['status']['code'] == 0 and obj['result']['status']['message'] == 'OK':
                    return obj['session']
                else:
                    return None

        def _logout(self, sid, session, url='sys/logout'):
                par1=self._pack_key_val('url', url)
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'exec')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                #print msg
                print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                #print res
                print
                obj=json.loads(res)
                if obj['result']['status']['code'] == 0 and obj['result']['status']['message'] == 'OK':
                        return 1
                else:
                        return 0


        def _read(self, url, sid, session, additional):
                par1=self._pack_key_val('url', url)
                if additional != None:
                    par1=par1+','+additional
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'get')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
#                print "below are JSON request"+"\n"
#                print msg
#                print 

                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
#                print "below are JSON response"+"\n"
#                print res
#                print "End of response"+"\n"
#                print

                obj=json.loads(res)

                return obj


        def _multiread(self, url1, url2, sid, session):
                par1=self._pack_key_val('url', url1)
                par2=self._pack_obj_request((par1,))
                bar1=self._pack_key_val('url', url2)
                bar2=self._pack_obj_request((bar1,))
                par3=self._pack_lst_request((par2, bar2))
                line1=self._pack_key_val('method', 'get')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print
                obj=json.loads(res)
                return obj

        def _write(self, url, sid, session, data):
                par1=self._pack_key_val('url', url)
                par_d=self._concat_param('data', data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'set')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print

                obj=json.loads(res)
                return obj

        def _devwrite(self, url, sid, session, data):
                par1=self._pack_key_val('url', url)
                par_d=self._concat_param('data', data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'exec')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print

                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print
                obj=json.loads(res)
                return obj

        def _add(self, url, sid, session, data):
                par1=self._pack_key_val('url', url)
                par_d=self._concat_param('data', data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'add')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print

                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print

                obj=json.loads(res)
                return obj

        def _update(self, url, sid, session, data):
                par1=self._pack_key_val('url', url)
                par_d=self._concat_param('data', data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'update')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
#                print msg
#                print

                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
#                print res
#                print
                obj=json.loads(res)
                return obj

        def _delete(self, url, sid, session, additional):
                par1=self._pack_key_val('url', url)
                if additional != None:
                    par1=par1+','+additional
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'delete')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print
                obj=json.loads(res)
                return obj

        def _pkg_read(self, url, sid, session, additional):
                par1=self._pack_key_val('url', url)
                if additional != None:
                        par1=par1+','+additional
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'get')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print
                obj=json.loads(res)
                print obj
                return obj


        def _pkg_write(self, url, sid, session, children, name):
                par1=self._pack_key_val('url', url)
                if name != None:
                        n1=self._pack_key_val('name', name)
                        par1=par1+','+n1
                par_d=self._concat_param('children', children)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method', 'set')
                line2=self._concat_param('params', par3)
                line3=self._pack_key_val('id', sid)
                line4=self._pack_key_val('session', session)
                msg=self._pack_obj_request((line1, line2, line3, line4))
                print msg
                print
                myreq=urllib2.Request(self._url, msg, self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''
                res= handler.read()
                print res
                print
                obj=json.loads(res)
                return obj

        def execute(self, data):
                if data['method']=='get':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        if data.has_key('additional'):
                           additional=data['additional']
                        else:
                           additional=None;
                        obj=self._read(prefix+url, int(sid), additional)
                        if str(obj['id']) == sid:
                           for element in obj['result']:
                              if element['url'] == url:
                                 if element.has_key('data'):
                                     if element['data'] != None:
                                          return element['data']

                if data['method']=='set':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        dat=data['data']
                        obj=self._write(prefix+url, int(sid), dat)
                        if str(obj['id']) == sid:
                           for element in obj['result']:
                              if element['url'] == url:
                                 if element.has_key('status'):
                                     if element['status'] != None:
                                          return element['status']

                if data['method']=='delete':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        if data.has_key('additional'):
                           additional=data['additional']
                        else:
                           additional=None;
                        obj=self._delete(prefix+url, int(sid), additional)
                        if str(obj['id']) == sid:
                           for element in obj['result']:
                              if element['url'] == url:
                                 if element.has_key('status'):
                                     if element['status'] != None:
                                          return element['status']


#########################################################################
# below are writen by James Cheng For FortiAnalyzer test                #
#########################################################################

        def _parse_language_cmd(self,obj):
                lan_list=[]
                try:
                    for e in obj['result'][0]['data']:
                        lan_list.append(e['name'])
                except:
                    pass
                return lan_list

        def _parse_dataset_cmd(self,obj):
                dataset={}
                i=0
                try:
                    for e in obj['result'][0]['data']:
                        dataset[e['name']]=e['query']
                       
                except:
                    pass
                return dataset

        def _parse_chart_cmd(self,obj):
                chart={}
                chart_type_list=[]
                try:
                    for e in obj['result'][0]['data']:
                        chart[e['name']]=e['dataset']

                        chart_type_list.append(e['graph-type'])
                except:
                    pass
                return chart,chart_type_list

        def _parse_layout_cmd(self,obj):
                layout_name_list=[]
                try:
                    for e in obj['result'][0]['data']:
                        layout_name_list.append(e['title'])
                except:
                    pass
                return layout_name_list

        def _parse_schedule_cmd(self,obj):
                schedule_name_list=[]
                i=0
                try:
                    for e in obj['result'][0]['data']:
                        schedule_name_list.append(e['name'])
                except:
                    pass
                return schedule_name_list

        def _parse_output_cmd(self,obj):
                output_list=[]
                i=0
                try:
                    for e in obj['result'][0]['data']:
                        output_list.append(e['name'])
                except:
                    pass
                return output_list

        def _add_language(self,session,name):
            url="config/global/sql-report/language";
            data="[{\"name\":"+"\""+ name+ "\""+","+" \"description\": \"test Language\", \"protected\": 1}]"
            try:
                result_obj=self._write(url, '', session, data)
                if result_obj['result'][0]['status']['code'] == 0 and result_obj['result'][0]['status']['message'] == 'OK':
                        print "config sucess!"
                        return 0
                else:
                        print "config fail"
                        return -1
            except :
                pass

         # This fuction will
         # 1. Retrieve all the charts in the system and put into a chartlist;
         # 2. Build a jason request payload (data)
         # 3. Put the payload request data, than use write function to construct final jason api package.
        def _create_all_charts_template(self,session,num):
            #1. Retrieve all the charts in the system and put into a chartlist;
            obj=self._read("config/adom/"+self._myadom+"/sql-report/chart", '', session, '')
            chartList,obj2,obj3=self._parse_chart_cmd(obj)
            num_of_charts=len(chartList)
            #2. Build a jason request payload (data)
            data="[{\"title\": \"All_charts_template\", \"component\":["
            i=1
            for ch in range(num):
                chartObj="{"+"\"component-id\""+":"  + str(i)  +  ","  +  " \"chart\""+":" + "\""+chartList[ch%num_of_charts]+ "\"" + "}"
                data=data+chartObj
                if i<num:
                    data=data+","
                i=i+1
            data=data+"]}]"
            #print "data="+data
           # 3. Put the payload request data, than use write function to construct final jason api package.             #3
            try:
                result_obj=self._write("config/adom/"+self._myadom+"/sql-report/layout", '', session, data)
                if result_obj['result'][0]['status']['code'] == 0 and result_obj['result'][0]['status']['message'] == 'OK':
                        print "config sucess!"
                        return 0
                else:
                        print "config fail"
                        return -1
            except :
                pass

         # This fuction will
         # 1. Retrieve all the charts in the system and put into a chartlist;
         # 2. Build a jason request payload (data)
         # 3. Put the payload request data, than use write function to construct final jason api package.
        def _create_template(self,session,num):
            #1. Retrieve all the charts in the system and put into a chartlist;
            obj=self._read("config/adom/"+self._myadom+"/sql-report/chart", '', session, '')
            chartList,obj2,obj3=self._parse_chart_cmd(obj)
            chart_num=len(chartList)
            #2. Build a jason request payload (data)

            total_template=range(num)
            for ch in total_template:
                
                data="[{\"title\": \"template"+str(ch) 
                if chart_num!=0:
                    data=data+"\","+"\"component\":["
                    chartObj="{"+"\"component-id\""+":"  + "1"  +  ","  +  " \"chart\""+":" + "\""+chartList[ch%chart_num]+ "\"" + "}"
                    data=data+chartObj
                    data=data+"]}]"
                else:
                    print "Chart is empty, now creating empty template since no chart availabe."
                    data=data+"\""+"}]"
                print "data="+data
                try:
                    result_obj=self._write("config/adom/"+self._myadom+"/sql-report/layout", '', session, data)
                    if result_obj['result'][0]['status']['code'] == 0 and result_obj['result'][0]['status']['message'] == 'OK':
                            print "config sucess!"
                    else:
                            print "config fail"
                            return -1
                except :
                    pass
                sleep(0.02)

        def _delete_template(self,session,num):
            layout_url="config/adom/"+self._myadom+"/sql-report/layout"
            total=range(num)
            try:
                for i in total:
                    self._delete(layout_url+'/'+str(i), str(i), session, '')
            except:
                pass
        def _delete_schedule(self,session,num):
            url="config/adom/"+self._myadom+"/sql-report/schedule"
            total=range(num)
            try:
               for i in total:
                 self._delete(url+'/'+'schedule'+str(i), str(i), session, '')
            except:
               pass
        def _create_schedule(self,session,num,type,timeframe):
#          type:
#                 "on-demand":    0,
#                "every-n-hours": 1,
#                "every-n-days":  2,
#                "every-n-weeks": 3,
#                "every-n-months":4
            total_num=range(num)
            for ch in total_num:
                data="{\"name\": \"schedule"+str(ch) +"\"," + "\"schedule-type\":"+str(type)+"," + "\"schedule-valid-start\":"+"[\"00:00\", \"2011/08/01\"]"+","+ "\"time-period\":"+str(timeframe)+","+ "\"output-format\":"+"3"+","

                layoutSubObj="\"report-layout\":["+"{"+"\"layout-id\""+":"  + str(ch+1)  + "}"+"]"
                devicesSubObj="\"devices\":["+"{"+"\"devices-name\""+":"  + "\"All_FortiGates\""  + "}"+"]"
                #["00:00", "2011/08/01"]
                data=data+layoutSubObj+","
                data=data+devicesSubObj
                data=data+"}"
                print "data="+data
                try:
                    result_obj=self._add("config/adom/"+self._myadom+"/sql-report/schedule", 1, session, data)
                    print result_obj
                    if result_obj['result'][0]['status']['code'] == 0 and result_obj['result'][0]['status']['message'] == 'OK':
                            print "config sucess!"
                    else:
                            print "config fail"
                            return -1
                except :
                    pass
                sleep(0.02)

        def _create_dataset(self,session,name,query,logtype,num):
            # Build a jason request payload (data)

            total_template=range(num)
            for ch in total_template:
                if (num==1):
                    data="[{\"name\": "+"\""+name+"\","+"\"query\":"+"\""+query +"\","+"\"log-type\":"+logtype +","
                else:
                    data="[{\"name\": "+name+str(ch)+"\","+"\"query\":"+query +"\","               
                #data="[{\"name\": \"dataset"+str,"+"\"query\":"+"\"select * from table_ref"
                data=data+"\"variable\":["
                varObj="{"+"\"var\""+":"  + "\"user\""  +  ","  +  " \"var-name\""+":" + "\"user\"" +  ","+ " \"var-expression\""+":" + "\"user\""+  ","+  " \"var-type\""+":" + "\"string\""+ "}"
                data=data+varObj
                data=data+"]}]"
                
                print "data="+data
                try:
                    result_obj=self._write("config/adom/"+self._myadom+"/sql-report/dataset", '', session, data)
                    if result_obj['result'][0]['status']['code'] == 0 and result_obj['result'][0]['status']['message'] == 'OK':
                            print "config sucess!"
                    else:
                            print "config fail"
                            return -1
                except :
                    pass
                sleep(0.02)

        def _delete_dataset(self,session,name,num):
            layout_url="config/adom/"+self._myadom+"/sql-report/dataset"         
            
            total=range(num)
            try:
                for i in total:
                    if i==1:
                        self._delete(layout_url+'/'+name, str(i), session, '')
                    else:
                        self._delete(layout_url+'/'+'dataset'+str(i), str(i), session, '')
                    #self._delete(layout_url+'/'+'utm-Top-Allowed-Web-Sites-By-Request modify', str(i), session, '')
            except:
                pass

        def _create_chart(self,session,num):
            # Build a jason request payload (data)
            total_template=range(num)
            for ch in total_template:
                
                data="[{\"name\": \"chart"+str(ch)+"\","+"\"category\":"+"\"traffic"+"\","+"\"description\":"+"\"chart"+str(ch)+"\","+"\"dataset\":"+"\"dataset"+str(ch) +"\"," +"\"resolve-hostname\":"+"0" +","+"\"favorite\":"+"0" +"," +"\"graph-type\":"+"\"table" +"\"," +"\"table-subtype\":"+"\"basic" +"\"," +"\"line-subtype\":"+"\"basic" +"\","+"\"graph-columns\":"+"\"one-column" +"\"," +"\"order-by\":"+"\"yourfield" +"\","+"\"show-table\":"+"0" +"," +"\"x-axis-label\":"+"\"your-x-lablel"+"\","+"\"x-axis-data-binding\":"+"\"field1"+"\"," +"\"x-axis-data-top\":"+"10"+","+"\"y-axis-label\":"+"\"your-y-lablel"+"\","  +"\"y-axis-data-binding\":"+"\"field2"+"\"," +"\"y2-axis-label\":"+"\"your-y2-lablel"+"\","  +"\"y2-axis-data-binding\":"+"\"field2"+"\","+"\"y-axis-group\":"+"0"+"," +"\"y-axis-group-by\":"+"\"field2"+"\"," +"\"y-axis-data-top\":"+"10"+","+"\"scale\":"+"1"+"," +"\"protected\":"+"0 "                                                                
                data=data+","+"\"drill-down-table\":["
                drillDownObj1="{"+"\"table-id\""+":"  + "1"  +  ","  +  " \"chart\""+":" + "\"chart0\"" +"}"
                data=data+drillDownObj1
                data=data+"]"
                data=data+","+"\"table-columns\":["
                tableColumnObj1="{"+"\"id\""+":" + "1"  +  ","  +  " \"data-type\""+":" + "0"+"," +" \"data-binding\":"+"\"field1\""+"," +" \"column-num\""+":" + "10"+","+ " \"data-top\""+":" + "10"+","+ " \"column-attr\""+":" + "0"+","+ " \"column-icon\""+":" + "0"+"}"
                tableColumnObj2="{"+"\"id\""+":" + "2"  +  ","  +  " \"data-type\""+":" + "0" +","+" \"data-binding\":"+"\"field2\""+"," +" \"column-num\""+":" + "10"+","+ " \"data-top\""+":" + "10"+","+ " \"column-attr\""+":" + "0"+","+ " \"column-icon\""+":" + "0"+"}"
                data=data+tableColumnObj1+","
                data=data+tableColumnObj2
                data=data+"]"
                data=data+"}]"
                
                print "data="+data
                try:
                    result_obj=self._write("config/adom/"+self._myadom+"/sql-report/chart", '', session, data)
                    if result_obj['result'][0]['status']['code'] == 0 and result_obj['result'][0]['status']['message'] == 'OK':
                            print "config sucess!"
                    else:
                            print "config fail"
                            return -1
                except :
                    pass
                sleep(0.02)

        def _delete_chart(self,session,num):
            layout_url="config/adom/"+self._myadom+"/sql-report/chart"
            total=range(num)
            try:
                for i in total:
                    self._delete(layout_url+'/'+'chart'+str(i), str(i), session, '')
            except:
                pass