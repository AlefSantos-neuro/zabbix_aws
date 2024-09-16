#!/usr/bin/python
import datetime
import sys
from optparse import OptionParser
import boto.ec2.cloudwatch

### Arguments
parser = OptionParser()
parser.add_option("-i", "--client-id", dest="client_id",
                help="ClientID")
parser.add_option("-d", "--domain-name", dest="domain_name",
                help="DomainName")
parser.add_option("-a", "--access-key", dest="access_key",
                help="AWS Access Key")
parser.add_option("-k", "--secret-key", dest="secret_key",
                help="AWS Secret Access Key")
parser.add_option("-m", "--metric", dest="metric",
                help="cloudwatch metric")
parser.add_option("-r", "--region", dest="region",
                help="AWS region")

(options, args) = parser.parse_args()

if (options.client_id == None):
    parser.error("-i ClientID is required")
if (options.domain_name == None):
    parser.error("-d DomainName is required")
if (options.access_key == None):
    parser.error("-a AWS Access Key is required")
if (options.secret_key == None):
    parser.error("-k AWS Secret Key is required")
if (options.metric == None):
    parser.error("-m ELB cloudwatch metric is required")
###

### Real code
metrics = {"CPUUtilization":{"type":"float", "value":None},
	"WriteLatency":{"type":"float", "value":None},
	"ReadIOPS":{"type":"float", "value":None},
	"WriteIOPS":{"type":"float", "value":None}}
end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

#get the region
if (options.region == None):
    options.region = 'us-east-1'
    
for r in boto.ec2.cloudwatch.regions():
   if (r.name == options.region):
      region = r
      break

conn = boto.ec2.cloudwatch.CloudWatchConnection(options.access_key, options.secret_key,region=region)

for k,vh in metrics.items():

    if (k == options.metric):

        try:
                res = conn.get_metric_statistics(60, start, end, k, "AWS/ES", "Average", {"DomainName": options.domain_name,"ClientId": options.client_id})
                #print res               
        except Exception, e:
                print "status err Error running elb_stats: %s" % e.error_message
                sys.exit(1)
        if(len(res)>0):    
            average = res[-1]["Average"] # last item in result set
        else:
            average = 0

        if vh["type"] == "float":
                metrics[k]["value"] = "%.4f" % average
        if vh["type"] == "int":
                metrics[k]["value"] = "%i" % average

        #print "metric %s %s %s" % (k, vh["type"], vh["value"])
        print "%s" % (vh["value"])
        break
