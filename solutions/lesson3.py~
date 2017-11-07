# This line just imports the correct module
import CGATPipelines.Pipeline as P

# This line get the configuration. Don't worry about it for now.
PARAMS=P.getParameters()


def count_lines(infile, outfile):

    #run locat
    to_cluster = False

    statement = '''zcat %(infile)s | wc -l > %(outfile)s'''
    P.run()


count_lines("test3.fastq.gz", "test3.nlines")
count_lines("test4.fastq.gz", "test4.nlines")
count_lines("test5.fastq.gz", "test5.nlines")



