# This line just imports the correct module
import CGATPipelines.Pipeline as P
from ruffus import transform, suffix, pipeline_run

# This line get the configuration. Don't worry about it for now.
PARAMS=P.getParameters()


@transform("*.fastq.gz", suffix(".fastq.gz"), ".nlines")
def count_lines(infile, outfile):
    '''This function counts the number of lines in its infile'''
    
    #run locatally
    to_cluster = False

    statement = '''zcat %(infile)s | wc -l > %(outfile)s'''
    P.run()

@transform(count_lines, suffix(".nlines"), ".nreads")
def convert_to_reads(infile, outfile):
    ''' This function converts the number of lines in a file to a number
    of reads. It also labels this number with the sample name'''
    
    infile_handle = open(infile)
    outfile_handle = open(outfile, "w")

    line = infile_handle.readlines()[0]
    nlines = int(line)
    nreads = nlines/4
    sample_name = P.snip(infile, ".nlines")

    outfile_handle.write(sample_name + "\t" + str(nreads) +"\n")
    outfile_handle.close()

    
P.main()




