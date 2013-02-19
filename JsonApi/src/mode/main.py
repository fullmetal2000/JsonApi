
'''
important: need change httplib.py below line to make it works for https site!
 --          #self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)
 ++         self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
'''
import suds
import datetime
import base64

url = "https://172.16.106.254:8080"
client = suds.client.Client(url)

sp=client.factory.create('servicePass')
sp.userID='admin'
sp.password=''

#datetime
date1 = datetime.datetime( 2000, 3, 2)
date2 = datetime.datetime( 2013, 3, 6)
#print date1
#print client


#print client.service.getSystemStatus(sp,"root")
#print client.service.getFazConfig(sp )
#print client.service.setFazConfig(sp, 'root', newconfig)
'''
Get report from other adom maybe not working
'''
reportData= client.service.getFazGeneratedReport(sp, 'root', '2013_01_25', 'S-schedule-utm-reports_t1-2013-01-25-1804/FortiAnalyzer_Report.html', 0 ).fazReportData.reportContent
#print str(reportData)
original_data = base64.decodestring(str(reportData))
print original_data
#.strip('(fazReportData){').strip('}').lstrip('')


    #trim farzReportData and '{','}'
    #call base64 decoding function.
    #call file creation function
#print client.service.runFazReport(sp,'root', '4')
#print client.service.searchFazLog(sp, 'root', 0, 0, 'FG200B-1', 1,'srcip=10.0.0.1',30, 1, 0, 1, 1 )
#print client.service.getFazArchive(sp, 'root', 'FG200B0000000001', 'IPS', '50005:0', '', '', 0 )
#print client.service.removeFazArchive(sp,'root', 'FG200B0000000001', 'IPS','50005:0', '' )


#not working:
#print client.service.listFazGeneratedReports(sp, 'root', date1,date2 )





            
            