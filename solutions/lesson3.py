# This line just imports the correct module
import CGATCore.Pipeline as P
from ruffus import transform, suffix, pipeline_run

# This line get the configuration. Don't worry about it for now.
PARAMS=P.get_parameters()


@transform("*.fastq.gz", suffix(".fastq.gz"), ".nlines")
def count_lines(infile, outfile):

    #run locat
    to_cluster = False

    statement = '''zcat %(infile)s | wc -l > %(outfile)s'''
    P.run(statement)


P.main()





