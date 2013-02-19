#'''
#Created on Aug 16, 2011

#@author: JamesCheng
#'''
import telnetlib
import time
class DatasetQuery:
        """ FortiManager Class allowing to perform methods calls to the FortiManager device thru JSON"""
        _ip=None

        def __init__(self, faz_ip):
                self._ip=faz_ip

        # Func testDataset execute each dataset in FAZ to get result
        def testDataset(self, dataset, time_start, time_end):
            try:
                filename = 'Report_Dataset_TestResult' + time.asctime(time.localtime(time.time())) + '.txt'
                filename = filename.replace(' ', '_')
                filename = filename.replace(':', '-')
                TestResult = open(filename, 'w+')
                QueryResult = open("QueryResult", 'w+')
            except:
                print "Can not open file"
            for i, tmpds in enumerate(dataset) :
                if tmpds.find("fwb") != -1:
                    deviceType = 'All_FortiWebs'
                elif tmpds.find("fct") != -1:
                    deviceType = 'All_FortiClients'
                elif tmpds.find("fml") != -1:
                    deviceType = 'All_FortiMails'
                else :
                    deviceType = 'All_FortiGates'
        #        if i < int(startPoint):
        #            continue
                TestResult.writelines(str(i) + ' ')
                try:
                    tn = telnetlib.Telnet(self._ip)
                except:
                    print '\n******************************************************************'
                    print "Can not open host,Pls make sure you can telnet the FA used your PC"
                    print '******************************************************************\n'

                tn.read_until("login:", 10)
                tn.write('admin' + "\n")
                tn.read_until("Password:", 5)
                tn.write('' + "\n\n")
                Device_name = tn.expect(['#'])[2]
                print Device_name
                tn.read_until("#", 5)
                cmd = 'execute  sql-query-dataset  ' + tmpds + ' ' + deviceType + ' ' + ' dev ' + '"' + time_start + '"' + ' ' + '"' + time_end + '"'
                tn.write(cmd + "\n\n")
                print 'cmd=' + cmd
                tn.write("exit\n")
                rs = tn.read_all()


                QueryResult.writelines(rs)
                print rs
                if (rs.find("No data returns") != -1):
                    print str(i) + tmpds[:-1] + "---no data"
                    TestResult.writelines(tmpds[:-1] + "---no data" + "\n")
                elif (rs.find("doesn't exist") != -1):
                    print str(i) + tmpds[:-1] + "---Dataset doesn't exit"
                    TestResult.writelines(tmpds[:-1] + "---Dataset doesn't exit" + "\n")
                elif (rs.find(" syntax error") != -1):
                    print str(i) + tmpds[:-1] + "---syntax error or command fail"
                    TestResult.writelines(tmpds[:-1] + "---syntax error or command fail" + "\n")
                    TestResult.writelines(rs)
                elif (rs.find("Command fail") != -1) or (rs.find("command parse error") != -1):
                    print "---syntax error or command fail"
                    TestResult.writelines(tmpds[:-1] + "---syntax error or command fail" + "\n")
                    TestResult.writelines(rs)
                else :
                    print str(i) + tmpds[:-1] + "---syntax test pass"
                    TestResult.writelines(tmpds[:-1] + "---syntax test pass" + "\n")

            TestResult.close()
            QueryResult.close()

        def start(self,dataset):
            #print time.asctime(time.localtime(time.time()))
            faz_ip = raw_input("Enter FortiAnalyzer IP Address:\r\n")
            dev_type = int(raw_input("Enter Device Type: 1:FortiGate,2:FortiClient,3:FortiWeb,4:FortiMail\r\n"))
            time_start = raw_input("Enter start time,  yyyy-mm-dd hh:mm:ss   :\r\n ")
            time_end = raw_input("Enter end time, yyyy-mm-dd hh:mm:ss   :\r\n ")
            #startPoint = raw_input("Enter start number 0... 517 :\r\n ")
            #dataset = readInDataset(dev_type)
            self.testDataset(dataset, time_start, time_end)


