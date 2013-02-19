import string
import json
import urllib
import urllib2
import suds
import datetime
import base64
import time
from mode import SendCmd

if __name__ == '__main__':
    print "Version 1.0.5   Release notes: Add in webservice feature\r\n "
    faz_ip = raw_input("Enter FortiAnalyzer IP Address:\r\n")
    adom = raw_input("Enter Adom name,if no input,default will be 'root':\r\n")
    if adom == '':
        adom = 'root'
   
    # faz_ip=faz_ip[:-1] #remove return
    print faz_ip
    test = SendCmd.fmgApi5(faz_ip)
    session = test._login('admin', '', 1)
    if session == None:
        print "Log in fail."
        exit
    else:
        print "session =" + session
    data0 = '''[{
            "name": "Japan123",
            "description": "Japane123 Language",
            "protected": 1
         }]'''
    test._myadom = adom
    print "adom=" + test._myadom
    url = "https://" + faz_ip + ":8080"
    print "Connecting to "+url+".........."
    # connect to webservice using suds
    try:
        client = suds.client.Client(url)
    except:
        print "Connect webservice error,  check your ip address and make sure the webservice is enabled on FortiAnalyzer, can only use Json feature now."
        pass
    print "Connected. \r\n"
    # create servicePass
    try:
        sp = client.factory.create('servicePass')
        sp.userID = 'admin'
        sp.password = ''
    except :
        print "Webservice not connected, test JSON only test case 1~5 only."
        pass
    # below data is used to add in more component.
    # data='''[{"title": "test1", "component":[{"component-id": 1, "chart": "Top-User-By-Sessions",},{"component-id": 2, "chart": "Top-User-By-Sessions"}]}]'''
    # test._create_all_charts_template(session)
    # test._create_template(session,1000)
    # test._create_schedule(session, 2)
    # test._delete_schedule(session,1000)
    # obj=test._write("config/adom/root/sql-report/layout/9/component", '', session, data)
    # run dataset query:
    #       newtest=dataset_test.DatasetQuery(faz_ip)
    #       newtest.start(dataset)
    
    # 3 test the chart:
    #       obj=test._read("config/adom/root/sql-report/chart", '', session, '')
    #       obj1,obj2,obj3=test._parse_chart_cmd(obj)
    while(1):
        testcase = int(raw_input('''Enter testcase id: \r\n1-template\r\n2-schedule\r\n3-datasets\r\n4-charts\r\n5-language\r\n6-Logs\r\n7-Reports\r\n8-Config\r\n9-Archives\r\n0-exit\r\n'''))
        if testcase == 1:
            while(1):
                tc = int(raw_input('''1-Read templates\r\n2-Add template\r\n3-Del template\r\n4-Build a multi-charts template\r\n0-Back to Main Menu\r\n'''))
                if tc == 1:
                    obj = test._read("config/adom/" + adom + "/sql-report/layout", '', session, '')
                    print "Template list are:"
                    obj1 = test._parse_layout_cmd(obj)
                    i = 1
                    for c in obj1:
                        print str(i) + " " + c
                        i = i + 1
                    print
                    print "Menu:"
                    continue
                elif tc == 2:
                    num = int(raw_input("input number of templates you wants to add, name begins from template0 \r\n"))
                    test._create_template(session, num)
                    print
                    print "Menu:"
                    continue
                elif tc == 3:
                    num = int(raw_input("input number of templates you wants to del,e.g if input 10, it will delete template0~10 \r\n"))
                    test._delete_template(session, num)
                    print
                    print "Menu:"
                    continue
                elif tc == 4:
                    num = int(raw_input("input number of charts you wants to put in to the template \"more_charts_template\" \r\n"))
                    test._create_all_charts_template(session, num)
                    print
                    print "Menu:"
                    continue
                else:
                    break
    
    
        elif testcase == 2:
            while(1):
                tc = int(raw_input("1-Read schedule\r\n2-Add schedule\r\n3-Del schedule\r\n0-exit\r\n"))
                if tc == 1:
                    obj = test._read("config/adom/" + adom + "/sql-report/schedule", '', session, '')
                    print "schedule list are:"
                    obj1 = test._parse_schedule_cmd(obj)
                    i = 1
                    for c in obj1:
                        print str(i) + " " + c
                        i = i + 1
                    print
                    print "Menu:"
                    continue
    
                elif tc == 2:
                    num = int(raw_input("input number of schedules you wants to add, name begins from schedule0 \r\n"))
                    stype = int(raw_input('''input type:
                 on-demand:    0,
                 every-1-hours: 1,
                 every-1-days:  2,
                 every-1-weeks: 3,
                 every-1-months:4'
                 \r\n'''))
                    timeframe = int(raw_input('''input time period:
                 "today":         0,
                 "yesterday":     1,
                 "last-n-hours":  2,
                 "this-week":     3,
                 "last-week":     4,
                 "last-7-days":   5,
                 "last-n-days":   6,
                 "last-2-weeks":  7,
                 "last-14-days":  8,
                 "this-month":    9,
                 "last-month":    10,
                 "last-30-days":  11,
                 "last-n-weeks":  12,
                 "this-quarter":  13,
                 "last-quarter":  14,
                 "this-year":     15,
                 "other":         16
                 \r\n'''))                       
                    test._create_schedule(session, num, stype, timeframe)
                    print
                    print "Menu:"
                    continue
                elif tc == 3:
                    num = int(raw_input("input number of schedules you wants to del \r\n"))
                    test._delete_schedule(session, num)
                    print
                    print "Menu:"
                    continue
                else:
                    break
    
        elif testcase == 3:
            while(1):
                tc = int(raw_input("1-read dataset\r\n2-create dataset\r\n3-delete dataset\r\n0-exit\r\n"))
                if tc == 1:
                    obj = test._read("config/adom/" + adom + "/sql-report/dataset", '', session, '')
                    dataset_dict = test._parse_dataset_cmd(obj)
                    i = 1
                    for k, v in dataset_dict.iteritems():
 #                       if (k.find("default") != -1 ) or (k.find("wireless") != -1):
                        print str(i) +" "+ k+"\n"+"query: "+v+"\n"
                        i = i + 1
                
                elif tc == 2:
                    #num = int(raw_input("input number of datasets you wants to add, name begins from dataset0 \r\n"))
                    name=raw_input("Input dataset name:")
                    query=raw_input("Input dataset query:")
                    logtype=raw_input("Input dataset log-type:\r\n  \
    APPCTRL:        0, \r\n  \
    ATTACK:         1, \r\n  \
    CONTENT:        2,\r\n  \
    DLP:            3,\r\n  \
    EMAILFILTER:    4,\r\n  \
    EVENT:          5,\r\n  \
    HISTORY:        7,\r\n  \
    SNIFFER:        9,\r\n  \
    TRAFFIC:        10,\r\n  \
    VIRUS:          11,\r\n  \
    WEBFILTER:      13,\r\n  \
    NETSCAN:        14,\r\n ")
                    num=raw_input("Input number of datasets to create:")
                    test._create_dataset(session, name,query,logtype,num)
                elif tc == 3:
                    #num = int(raw_input("input number of datasets you wants to delete, name begins from dataset0 \r\n"))
                    name=raw_input("Input dataset name:")
                    num=raw_input("Input number of datasets to delete:")
                    test._delete_dataset(session, name,num)                       
                else:
                    break
    
        elif testcase == 4:
            while(1):
                tc = int(raw_input("1-read chart\r\n2-create chart\r\n3-delete chart\r\n0-exit\r\n"))
                if tc == 1:
                    obj = test._read("config/adom/" + adom + "/sql-report/chart", '', session, '')
                    chart_dict, obj2 = test._parse_chart_cmd(obj)
                    i = 1
                    for k, v in chart_dict.iteritems():
 #                       if (k.find("default-")!=-1 or k.find("wireless")!=-1) :
                        print str(i) + " "+k+"\n"+"dataset: "+v+"\n"
                        i = i + 1
                    print
                    print "Menu:"
                    continue
                elif tc == 2:
                    num = int(raw_input("input number of charts you wants to add, name begins from chart0 \r\n"))
                    test._create_chart(session, num)
                elif tc == 3:
                    num = int(raw_input("input number of charts you wants to delete, name begins from chart0 \r\n"))
                    test._delete_chart(session, num)  
                    
                else:
                    break
    
        elif testcase == 5:
            while(1):
                tc = int(raw_input("1-read language\r\n2-add language\r\n0-exit\r\n"))
                if tc == 1:
                    obj = test._read("config/global/sql-report/language", '', session, '')
                    obj1 = test._parse_language_cmd(obj)
                    i = 1
                    for c in obj1:
                        print str(i) + c
                        i = i + 1
                    # go back to language or main menu:
                    print
                    print "Menu:"
                    continue
                
                elif tc == 2:
                    name = raw_input("input language name, e.g. test_lan1\r\n")
                    test._add_language(session, name)
                    print
                    print "Menu:"
                    continue
                else:
                    # back to main menu:
                    break
        elif testcase == 6:
            while(1):
                tc = int(raw_input('''1-Search Logs\r\n0-Back to Main Menu\r\n'''))
                if tc == 1:                       
                    current_dev = (raw_input("Enter Device Name:  default is 'FG200B0000000001'\r\n") or 'FG200B0000000001')
                    log_content = (raw_input("Enter log content: 0 Logs; 1 ContentLogs 2 LocalLogs; default is 0\r\n") or '0')
                    log_format = (raw_input("Enter log format: 0 raw; 1 csv; default is 0\r\n") or '0')
                    log_type = (raw_input("Enter log type:\r\n0 event;\r\n1 traffic;\r\n2 attack;\r\n3 antiVirus;\r\n4 webLogs;\r\n \
                     5 IM;\r\n6 email;\r\n7 content;\r\n8 history;\r\n9 generic;\r\n10 voIP;\r\n11 DLP;\r\n12 appCtrl;\r\n13 netScan;\r\n default is '1'\r\n ") or '1')
                    searchCriteria = (raw_input("Enter search Criteria: like \"srcip=10.0.0.1\"   default is 'vd=root'\r\n ") or "vd=root")
                    max_match = (raw_input("Enter maxium matched logs: like 100;  default is 10\r\n") or '10')
                    start_index = (raw_input("Enter starting index. like 1;  default is '1'\r\n") or '1')
                    print 'current value :'
                    print "current_dev =" + current_dev
                    print "log_content=" + log_content
                    print "log_format=" + log_format
                    print "log_type=" + log_type
                    print "searchCriteria=" + searchCriteria
                    print "max_match=" + max_match
                    print "start_index=" + start_index       
                    try:
                        print client.service.searchFazLog(sp, adom, int(log_content) , int(log_format), current_dev, int(log_type), searchCriteria, int(max_match), int(start_index), 0, 1, 1)
                    except :
                        print "error"
                        
                    # print client.service.searchFazLog(sp, adom,0 , 0, "FG200B-1", 0,"srcip=10.0.0.1",10, int(start_index), 0, 1, 1 )
                    print
                    print "Menu:"
                    continue
    
                else:
                    break
        #Report comand
        elif testcase == 7:
            while(1):
                tc = int(raw_input('''1-List Reports\r\n2-Get Report\r\n3-Run Report\r\n0-Back to Main Menu\r\n'''))
                if tc == 1:
                    date1=(raw_input("Enter report date, format:YYYY-MM-DD HH:MM:SS  default is '2011-01-01 00:00:00' \r\n") or '2011-01-01 00:00:00')
                    date2=(raw_input("Enter report date, format:YYYY-MM-DD HH:MM:SS  default is '2015-01-01 00:00:00'\r\n") or '2015-01-01 00:00:00')
                    
                    print "searching historical report from "+date1+"to"+date2
                    date1=date1.replace(' ','T')
                    date2=date2.replace(' ','T')
                   
                    try:
                        print client.service.listFazGeneratedReports(sp, adom, date1,date2 )
                    except:
                        print "error"
                    continue
                if tc == 2:                       
                    report_date = raw_input("Enter report date, format:YYYY_MM_DD :\r\n (Tips: You can get report time and name from List Reports.)\r\n")
                    report_name = (raw_input("Enter report name.\r\n(Tips: You can get report time and name from List Reports.)\r\n") or '')
                    compression_type = (raw_input("Enter compression type: 0 tar; 1 gzip, default is 'tar'\r\n") or '0')
                    
                    print 'current value:'
                    print "report_date =" + report_date
                    print "report_name=" + report_name
                    print "compression_type=" + compression_type
    
                    try:
                        reportData = client.service.getFazGeneratedReport(sp, adom, report_date, report_name, int(compression_type)).fazReportData.reportContent
                    # print str(reportData)
                    except :
                        print "error"
                        
                    try:
                        original_data = base64.decodestring(str(reportData))
                    except:
                        print "decode error"
                    # print original_data
                    # store it to a file:
                    try:
                        if int(compression_type)==0:
                            file_ext="tar"
                        elif int(compression_type)==1:
                            file_ext="gzip"
                        else:
                            file_ext="gzip"
                        filename = '../downloads/report_file' + time.asctime(time.localtime(time.time())) + '.'+file_ext
                        filename = filename.replace(' ', '_')
                        filename = filename.replace(':', '-')
                        output_file = open(filename, 'wb+',-1)
                        output_file.write(original_data)
                        print filename.strip('../downloads/')+" saved in downloads folder." 
                    except:
                        print "Can not open file"
                        pass
#                    try:
#                        output_file = open("report_file.gzip", "wb+", -1)
#                        output_file.write(original_data)
#                    except:
#                        print "file open error"
#                        pass
                   
                    output_file.close()
                    print
                    print "Menu:"
                    continue
                if tc == 3:                       
                    schedule_name = (raw_input("Enter schedule name, default is 'schedule-utm-reports'") or 'schedule-utm-reports')
                    
                    print 'current value:'
                    print "schedule_name =" + schedule_name
    
                    try:
                        print "Running report  "+schedule_name+"............................."
                        client.service.runFazReport(sp,adom, schedule_name)
                    # print str(reportData)
                    except:
                        print "error"
    
                    print "Menu:"
                    continue
                else:
                    break               
        #Config commands
        elif testcase==8:
            while(1):
                tc = int(raw_input('''1-Get System Status\r\n2-Get Config\r\n3-Set Config\r\n0-Back to Main Menu\r\n'''))
                if tc == 1:                       
                    try:
                        print client.service.getSystemStatus(sp,adom)
                    # print str(reportData)
                    except :
                        print "error"
    
                    print "Menu:"
                    continue
                
                if tc == 2:                       
                    try:
                        print client.service.getFazConfig(sp ).config
                    # print str(reportData)
                    except :
                        print "error"
    
                    print "Menu:"
                    continue
                
                if tc == 3:
                    print('Please input your piece of config to newconfig.txt file fistly   ')   
                    
                    try:
                        newCfgFile=open("newconfig.txt","rU")
                    except:
                        print " new config file open error"
                        break                
                    newconfig=newCfgFile.read()
                    print "newconfig"+ newconfig              
                    try:
                        print client.service.setFazConfig(sp, 'root', newconfig)
                    # print str(reportData)
                    except :
                        print "error"
                    newCfgFile.close()
                    print "Menu:"
                    continue
                else:
                    break    
        #Archive commands
        elif testcase==9:
            while(1):
                tc = int(raw_input('''1-Get Archive File\r\n2-Remove Archive File\r\n0-Back to Main Menu\r\n'''))
                if tc == 1:                 
                    current_dev = (raw_input("Enter Device Name:  default is 'FG200B0000000001'\r\n") or 'FG200B0000000001')  
                    archive_type=   (raw_input("Enter Archive type: - 0: web, 1:email,2:ftp,3:IM,4:MMS,5:quarantine,6:IPS, default is 'IPS'\r\n") or 'IPS')  
                    archive_name=(raw_input("Enter Archive name. Default is '50005:0'\r\n") or '50005:0')  
                    #compression_type = (raw_input("Enter compression type: 0 tar; 1 gzip, default is 'tar'\r\n") or '0')
                    print 'current value:'
                    print "current_dev =" + current_dev
                    print "archive_type =" + archive_type
                    print "archive_name =" + archive_name
                    print "adom =" + adom
                    try:
                        print "Retrieving......"
                        reportData= client.service.getFazArchive(sp, adom, current_dev, archive_type, archive_name, '', '',0 ).fileList[0].data
                        print reportData
                    except :
                        print "error"
                    original_data = base64.decodestring(str(reportData))
                    print "original_data:"
                    print original_data
                    # store it to a file:
                    archive_output_file=archive_type+"_"+archive_name+"archive"
                    archive_output_file=archive_output_file.replace(':','_')
                    try:
                        output_file = open(archive_output_file, "wb+", -1)
                        output_file.write(original_data)
                    except:
                        print "file open error"
                        pass
                    output_file.close()
                    print "archive file:"+archive_output_file+" has been saved to local path"
                    print "Menu:"
                    continue
                
                if tc == 2:   
                      
                    current_dev = (raw_input("Enter Device Name:  default is 'FG200B0000000001'\r\n") or 'FG200B0000000001')  
                    archive_type=   (raw_input("Enter Archive type: - 0: web, 1:email,2:ftp,3:IM,4:MMS,5:quarantine,6:IPS, default is 'IPS'\r\n") or 'IPS')  
                    archive_name=(raw_input("Enter Archive name. Default is '50005:0'\r\n") or '50005:0')  
                    #compression_type = (raw_input("Enter compression type: 0 tar; 1 gzip, default is 'tar'\r\n") or '0')
                    print 'current value:'
                    print "current_dev =" + current_dev
                    print "archive_type =" + archive_type
                    print "archive_name =" + archive_name
                    print "adom =" + adom
                    try:
                        print "Retrieving......"
                        reportData= client.service.removeFazArchive(sp,adom, current_dev, archive_type,archive_name, '' )
                        print reportData
                    except :
                        print "error"
                    print "Menu:"
                    continue
                
                else:
                    break        
        else:
            break
    
    
    # test template:
    # test schedule
    test._logout(1, session)
