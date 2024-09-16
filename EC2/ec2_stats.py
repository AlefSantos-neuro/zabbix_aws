#!/usr/bin/python
import datetime
import sys
from optparse import OptionParser
import boto.ec2.cloudwatch

### Arguments
parser = OptionParser()
parser.add_option("-i", "--instance-id", dest="instance_id",
                help="InstanceIdentifier")
parser.add_option("-a", "--access-key", dest="access_key",
                help="AWS Access Key")
parser.add_option("-k", "--secret-key", dest="secret_key",
                help="AWS Secret Access Key")
parser.add_option("-m", "--metric", dest="metric",
                help="RDS cloudwatch metric")
parser.add_option("-r", "--region", dest="region",
                help="RDS region")

(options, args) = parser.parse_args()

if (options.instance_id == None):
    parser.error("-i InstanceIdentifier is required")
if (options.access_key == None):
    parser.error("-a AWS Access Key is required")
if (options.secret_key == None):
    parser.error("-k AWS Secret Key is required")
if (options.metric == None):
    parser.error("-m RDS cloudwatch metric is required")
###

### Real code
metrics = {"CPUCreditBalance":{"type":"float", "value":None},
	"CPUCreditUsage":{"type":"float", "value":None},
	"StatusCheckFailed":{"type":"int", "value":None}}

end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)

#get the region
if (options.region == None):
    options.region = 'sa-east-1'
    
for r in boto.ec2.cloudwatch.regions():
   if (r.name == options.region):
      region = r
      break

conn = boto.ec2.cloudwatch.CloudWatchConnection(options.access_key, options.secret_key,region=region)
#print conn

for k,vh in metrics.items():

    if (k == options.metric):
        try:
#		print k

                res = conn.get_metric_statistics(60, start, end, k, "AWS/EC2", "Average", {"InstanceId": options.instance_id})
#		print res
	
        except Exception, e:
                print "status err Error running rds_stats: {}".format(e.errno, e.strerror)
                sys.exit(1)
        average = res[-1]["Average"] # last item in result set
        if (k == "FreeStorageSpace" or k == "FreeableMemory"):
                average = average / 1024.0**3.0
        if vh["type"] == "float":
                metrics[k]["value"] = "{}".format(average)
        if vh["type"] == "int":
                metrics[k]["value"] = "{}".format(average)

        #print "metric %s %s %s" % (k, vh["type"], vh["value"])
        #print "%s" % (vh["value"])
	#nova = (float(res[-1]["Average"]))
	print vh['value']
	break
