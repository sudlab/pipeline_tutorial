# This line just imports the correct module
import CGATPipelines.Pipeline as P

# This line get the configuration. Don't worry about it for now.
PARAMS=P.getParameters()

# Normally "Jobs" in CGATPiplines are executed on remote computers
# that are part of the cluster. Setting to_cluster to false
# makes it run things here.
to_cluster = False

statement = '''zcat test2.fastq.gz | wc -l > test2.nlines'''

P.run()

