

## Introduction

This tutorial is a step-by-step guide to understanding and writing the sorts of pipelines that we regularly use. It is aimed at people who have been in the lab for maybe a little longer than a month.

  

### What is a pipeline?

A pipeline is a program that takes a set of input files, runs a series of predefined tasks on them and produces output. A pipeline is useful because:

1.  Instead of typing:   
    
        $ program1 input1 > output1  
        $ program2 output1 > output2  
        $ program3 output2 > output3 
    
    Everything is run in a single command.
2.  This process is automatically run on a whole bunch of input files without having to bother doing it to each file individually. Results from multiple files can be merged or collated, compared etc.
3.  If something goes wrong halfway through, or you need to add another file to an already completed pipeline, the pipeline will work out which bits it needs to run and which bits are still fine.

We have a large number of pipelines already written for carrying out many processes. You may also want to write your own.

  

### Prerequisites

It is expected that you will have the following knowldge:

-   Basic knowledge of writing things at the linux command line (bash)
-   Basic knowledge of python syntax

-   Importing pacakges
-   Assigning variables
-   Writing and calling functions.

If these are things that you haven't picked up yet, you might like to look at a basic python and a basic bash course on the [Tutorials and Learning Resources](https://sites.google.com/a/sheffield.ac.uk/sudlab_internal/home/tutorials-and-learning-resources) page.

  

We will also be using git to obtain the files, but these commands will be full spelt out.

  

Finally, we are also going to assume that your computational environment is fully set up on iceberg/sharc. If it isn't you might like to ask someone to make sure it is.

  

## Lession 1: Running external commands from python with P.run(statement)

  

The first job is to get the files required for the tutorial. We do this by cloning the github that contains the files. Find a good place on your iceberg/sharc home directory and enter the following:

  

    $ git clone git@github.com:sudlab/pipeline_tutorial.git

  

You should now have a directory called pipeline_tutorial containing a lessons directory and a solutions directory:

    $ ls pipeline_tutorial
    lessons README.md solutions

Enter the `pipeline_tutorial/lessons` directory. Write a single line that will tell you how many lines are present in the `test1.fastq.gz` file. The solution is on the line below (highlight the line to find the answer), but try to do it yourself first.

    $ cd pipeline_tutorial/lessons/
    $ ls
    test1.fastq.gz test2.fastq.gz test3.fastq.gz test4.fastq.gz
      
    $ zcat test1.fastq.gz | wc -l
    40

  

Now rewrite your line so that it saves it to a file called test1.nlines. Again, the answer is below (highlight the missing line), but try to get it yourself first.

    $ zcat test1.fastq.gz | wc -l > test1.nlines
    $ cat test1.nlines
    40

Now we would like to automate this with a python script. Here is where the first facility from the CGATPipelines module comes in useful. Use your favorite text editor to create a python script. The script should start with the following lines.

    # This line just imports the correct module
    import CGATCorePipelines.Pipeline as P
    
    # This line get the configuration. Don't worry about it for now.
    PARAMS=P.get_pParameters()

    # Normally "Jobs" in CGATPiplines are executed on remote computers
    # that are part of the cluster. Setting to_cluster to false
    # makes it run things on your interactive session.
    to_cluster = False

Now add a line to the script that defines a variable called `statement` , which contains the command you used above on the command line to count the lines in `test1.fastq` and outputs to `test1.nlines`, but this time does it with `test2`. Finish off your script with a call to `P.run(statement)`. `P.run(statement)` tells the computer to look for a variable called `statement`, and run the contents of it.

Execute your python script and have a look at the results. For example, if you had called your script `lesson1.py`, you would type:

    $ python lesson1.py
    $ cat test2.nlines
    80

You can see the solution to this by looking at `lesson1.py` in the solutions directory.

  

Here endeth the first lesson.

## Lesson 2: placeholders and parameterisation

  

Okay, so that is now doing what we wanted, but why use 5 lines of python to do what we could do in one line of bash? One reason is that we can make what we've done generalizable: at the moment it is "hard-coded" to work on test2.fastq.gz, but we can write it so that it can be re-used on lots of different files. We can do this by replacing the filenames with placeholders. These placeholders start with `%(` then have a variable name and then finish with `)s`. Thus we can change our statement line to the following:

    statement = "zcat %(infile)s | wc -l > %(outfile)s"

Now when we do P.run(statement), the script will look for variables called infile and outfile and substitute their values into the statement. Thus if we added the following to the script before P.run(statement) is executed:

    infile = "test3.fastq.gz"
    outfile = "test3.nlines"

So that the total script was:

    # This line just imports the correct module`
    import CGATCorePipelines.Pipeline as P
    
    # This line get the configuration. Don't worry about it for now.
    PARAMS=P.get_pParameters()  
    
    # Normally "Jobs" in CGATPiplines are executed on remote computers
    # that are part of the cluster. Setting to_cluster to false
    # makes it run things on your interactive session.
    to_cluster = False
    statement =` `"zcat %(infile)s | wc -l > %(outfile)s"   
    infile = "test3.fastq.gz"
    outfile = "test3.nlines" 
    
    P.run(statement)

The line that was run would be equivalent to typing:

    $ zcat test3.fastq.gz | wc -l > test3.nlines

This becomes useful when, instead of manually defining infile and outfile, they are defined as inputs to a function. See if you can complete the following script by defining a function called count_lines that will mean the following script counts the lines in test3.fastq.gz, test4.fastq.gz and test5.fastq.gz and puts the results in test3.nlines, test4.nlines and test5.nlines

    # This line just imports the correct module
    import CGATCorePipelines.Pipeline as P

    # This line gets the configuration. Don't worry about it for now.
    PARAMS=P.get_pParameters()
   
    #### Your function def line here #####
    
    #run locatally
    to_cluster = False
      
    # Finish the function
    
    count_lines("test3.fastq.gz", "test3.nlines")
    count_lines("test4.fastq.gz", "test4.nlines")
    count_lines("test5.fastq.gz", "test5.nlines")

  
Once again, the solution is stored in the solutions directory in the file lesson2.py

  

## Lesson 3: Run on ALL the files - turning your script into a pipeline with ruffus decorators

  

What we would really like to do, though is not to have to write the names of the things we would like to run, but rather to run on all the files automatically without use having to type to much more. This is the job of `ruffus`. `Ruffus` is a pipelining system that provides the base of CGATPipelines and is tightly intergrated with it. What we want to do specifically is what `ruffus` calls a _transform_ operation. We want to _transform_ each of our `.fastq.gz` files into a `.nlines` file.
 

In `ruffus` we do this with something called _decorators_. Decorators _decorate_ functions, modifying them in some way. You call a decorator like you would call a function, but starting with a `@` sign and with a function definition immediately following. Like so:

    @my_decorator()
    def my_function(param1, param2):
    # ...do stuff here

The decorator @transform tells ruffus that the following function is mean to transform one file into another. In its most basic form, it takes 3 parameters:

  _input:_ Specifies how to find the files that we would like to use as input files to our function

  _filter:_ Specifies how we would like to find the "base" of the filename

  _output:_ Specifies what to do with the "base" in order to get the output name

There are several ways in which we can specify the filter and output parameters, but the easiest way is to tell ruffus to remove an extension and add a new one. Thus, if we called transform like so:

    @transform("*.txt", suffix(".txt"), ".csv")

We would be saying we wished to use as inputs each of the files with the extension ".txt", and that to find the output filename, remove ".txt" from the name and add ".csv". So if we had the files `file1.txt, file2.txt` and `file3.txt` we are saying we want to do:

    file1.txt -> file1.csv
    file2.txt -> file2.csv
    file3.txt -> file3.csv

The way this happens is to call the following function with the input and output files. So in the case of the three files above, using

    @transform("*.txt", suffix(".txt"), ".csv")
    def my_func(infile, outfile):
    print "called with the following files:"
    print infile, outfile
  
Is the same as calling my_func 3 times with each of the files:

    def my_func(infile, outfile):
           print "called with the following files:"
           print infile, outfile
    
    my_func("file1.txt", "file1.csv")
    my_func("file2.txt", "file2.csv")
    my_func("file3.txt", "file3.csv")

Look at your python file from the last lesson. Delete the three calls to count_lines and replace with `P.main()`. At the start you will also need to add `from ruffus import transform, suffix`. Now add a `transform` decorator to your definition of `count_lines`. As usual the answer is in `solution/lesson3.py`, but try to get it yourself first.  
  
To run your results you will need to change the way you are calling the file. We need to tell the pipeline which function we are interested in and what we want to do with it. First clear out all the `nlines` files that we have already made with

    $ rm *nlines

Now we can ask the pipeline what it thinks it needs to do. If you have saved your pipeline as `lesson3.py` and written it correctly, you should be able to do the following:

    $ python lesson3.py show count_lines -v5
    
    # output generated by ../solutions/lesson3.py show count_lines -v5
    # job started at Tue Nov 7 18:30:54 2017 on sharc-node003.shef.ac.uk -- 67282ab1-20dc-4624-bc38-b80fa86925cf
    # pid: 93287, system: Linux 3.10.0-693.5.2.el7.x86_64 #1 SMP Fri Oct 20 20:32:50 UTC 2017 x86_64
    # cluster_memory_default : None
    # cluster_memory_resource : None 
    # cluster_num_jobs : None
    # cluster_options : None
    # cluster_parallel_environment : None
    # cluster_priority : None
    # cluster_queue : None
    # cluster_queue_manager : None
    # debug : False
    # dry_run : False
    # exceptions_terminate_immediately : False
    # force : False
    # input_validation : False
    # is_test : False
    # log_exceptions : False
    # logfile : pipeline.log
    # loglevel : 5
    # multiprocess : 40
    # pipeline_action : None
    # pipeline_format : svg
    # pipeline_targets : []
    # rabbitmq_exchange : ruffus_pipelines
    # rabbitmq_host : saruman
    # random_seed : None
    # ruffus_checksums_level : 0
    # short_help : None
    # stderr : <open file '<stderr>', mode 'w' at 0x2b239ab861e0>
    # stdin : <open file '<stdin>', mode 'r' at 0x2b239ab860c0>
    # stdlog : <open file '<stdout>', mode 'w' at 0x2b239ab86150>
    # stdout : <open file '<stdout>', mode 'w' at 0x2b239ab86150>
    # terminate : None
    # timeit_file : None
    # timeit_header : None
    # timeit_name : all
    # variables_to_set : []
    # without_cluster : None
    ## 2017-11-07 18:30:54,402 INFO Started in: /home/mb1ims/devel/pipeline_tutorial/lessons
    ________________________________________
    
    Tasks which will be run:
     
    Task = 'count_lines'
    Job = [test1.fastq.gz
        -> test1.nlines]
    Job needs update: ...
    Missing file [test1.nlines]
    Job = [test2.fastq.gz
    -> test2.nlines]
    
    Job needs update: ...
       Missing file [test2.nlines]
     Job = [test3.fastq.gz
         -> test3.nlines]
   
    Job needs update: ... 
    Missing file [test3.nlines]
    Job = [test4.fastq.gz
    -> test4.nlines]
    
    Job needs update: ...
    Missing file [test4.nlines]  
    Job = [test5.fastq.gz  
    -> test5.nlines]   
    Job needs update: ..   
    Missing file [test5.nlines
    ________________________________________
    
    # job finished in 0 seconds at Tue Nov 7 18:30:54 2017 -- 1.05 0.56 0.00 0.01 -- 67282ab1-20dc-4624-bc38-b80fa86925cf`

The first part with all the # is logging information. It says what was run, when, on where and with what parameters. Then after that it tells you which files it needs to convert into others. To do this we run the following command

    $ python lesson3.py make count_lines -p1 --no-cluster

The `-p1` here tells it to only do one thing at once. This is important because sharc will kick you off if you try to do too many things at once. We will talk about doing lots of things at once using the cluster later.

Now if we look in our directory, we will see that all of our files have been converted to nlines files.

    $ ls
    
    pipeline.log test1.fastq.gz test1.nlines test2.fastq.gz test2.nlines test3.fastq.gz test3.nlines test4.fastq.gz test4.nlines test5.fastq.gz test5.nlines
 

There is also a log file which contains a record of everything that you've done with your pipeline in this directory.

  

## Lesson 4: Chaining tasks together

  

So far what we have is a convenient way to run a script on many different files. But there are other, possibly easier ways to do this. The real power comes when we can do several things in order. In our example we have counted how many lines there are in each of our fastq files. But what we probably really want to know is how many _reads_ there are in each one. Since each read is 4 lines long we need to divide the total number of lines by four.

  

(As far as I know), there is no unix command line that will divide a number stored in a file by 4 (I could be wrong). But this doesn't matter, we can run whatever python code we want in a task, not just code to run a statement.

  

Use the following template to add a function to your python program after the count_lines function, but before the `P.main()` call. It should:

-   Loads a file given by the name infile
-   Extracts the number stored in it
-   Divides that number by 4
-   Writes the name of the file, followed by a tab character, followed by the number of reads to a file whose name is stored in outfile.

  

`

    def convert_to_nreads(infile, outfile):
    ''' This function converts the number of lines in a file to a number    
    of reads. It also labels this number with the sample name'''
    
        infile_handle = open(infile)
        outfile_handle = open(outfile, "w")
    
        #
    #
    # Complete the function
        #
    
        outfile_handle.write(sample_name + "\t" + str(nreads))
        outfile_handle.close()

  

The pipeline mode provides a large number of useful functions for doing small but common tasks in pipelines. For example, in the above function, I asked you to output the name of the file into the first column of the output. But that ".nlines" on the end of it is a bit unsightly. What i'd really like is just the sample name - we'd like to remove ".nlines". We can do this with a function called P.snip. If infile contains the input filename "test1.nlines", then if we run the following:

    sample_name = P.snip(infile, ".nlines")

  sample_name will now contain "test1".

  

Use the above so that the output of your function is now a file containing the sample name, followed by a tab followed by the number of reads.

  
Now we need to tell the pipeline that this should be run on every file that was an output of the count_lines function. In lesson3 we used @transform("*.fastq.gz", suffix(".fastq.gz"), ".nlines") to convert all of the files with the extension .fastq.gz to files with the extension .nlines. The *.fastq.gz bit tells the pipeline to look in the directory for all the files ending .fastq.gz. But instead of using a template for filenames, we can use the name of a previous function to tell it to use the output files from that function. For example, here we want to take the output files from count_lines, which all have the extension .nlines, and transform them to files of the same name, but with the extension .nreads. We can do this with:

    @transform(count_lines, suffix(".nlines"), ".nreads")

Decorate your function with this. You can see a solution to the above in `solutions/lesson4.py`

If you check what your pipeline is going to do using `show convert_to_reads`, you should get the following response:

    $ python lesson4.py show convert_to_reads -v5`
    
    # output generated by ../solutions/lesson4.py show convert_to_reads -v5`
    # job started at Thu Nov 9 12:21:50 2017 on sharc-node004.shef.ac.uk -- 827e61cd-b50a-49bd-ba8c-1569b8c825aa`
    # pid: 77792, system: Linux 3.10.0-693.5.2.el7.x86_64 #1 SMP Fri Oct 20 20:32:50 UTC 2017 x86_64`
    # cluster_memory_default : None`
    # cluster_memory_resource : None`
    # cluster_num_jobs : None`
    # cluster_options : None`
    # cluster_parallel_environment : None`
    # cluster_priority : None`
    # cluster_queue : None`
    # cluster_queue_manager : None`
    # debug : False`
    # dry_run : False`
    # exceptions_terminate_immediately : False`
    # force : False`
    # input_validation : False`
    # is_test : False`
    # log_exceptions : False`
    # logfile : pipeline.log`
    # loglevel : 5`
    # multiprocess : 40`
    # pipeline_action : None`
    # pipeline_format : svg`
    # pipeline_targets : []`
    # rabbitmq_exchange : ruffus_pipelines`
    # rabbitmq_host : saruman`
    # random_seed : None`
    # ruffus_checksums_level : 0`
    # short_help : None`
    # stderr : <open file '<stderr>', mode 'w' at 0x2b244fed01e0>`
    # stdin : <open file '<stdin>', mode 'r' at 0x2b244fed00c0>`
    # stdlog : <open file '<stdout>', mode 'w' at 0x2b244fed0150>`
    # stdout : <open file '<stdout>', mode 'w' at 0x2b244fed0150>`
    # terminate : None`
    # timeit_file : None`
    # timeit_header : None`
    # timeit_name : all`
    # variables_to_set : []`
    # without_cluster : None`
    ## 2017-11-09 12:21:50,347 INFO Started in: /home/mb1ims/devel/pipeline_tutorial/lessons`
    ________________________________________

    Tasks which are up-to-date:`
  
    
    Task = 'count_lines' 
    "This function counts the number of lines in its infile"`
    ________________________________________`
    ________________________________________`
    
    Tasks which will be run:`

    Task = 'convert_to_reads'`  
    "This function converts the number of lines in a file to a number of reads. It also labels this`
    number with the sample name"
    
    Job = [test1.nlines`
    -> test1.nreads]
    
    Job needs update: ...
    Missing file [test1.nreads]    
    Job = [test2.nlines
    -> test2.nreads]
    Job needs update: ...`
    Missing file [test2.nreads]  
    Job = [test3.nlines
    -> test3.nreads]
    Job needs update: ...
    Missing file [test3.nreads]
    Job = [test4.nlines
    -> test4.nreads]
    Job needs update: ...
    Missing file [test4.nreads]
    Job = [test5.nlines
    -> test5.nreads]
    Job needs update: ...
    Missing file [test5.nreads]
  
    ________________________________________
    
    # job finished in 0 seconds at Thu Nov 9 12:21:50 2017 -- 1.10 0.66 0.00 0.00 -- 827e61cd-b50a-49bd-ba8c-1569b8c825aa`

  

Why do you think that it says count_lines is 'up-to-date' and doesn't list it under 'tasks that will be run'? What happens if you delete say `test1.nlines`, will the output of show change? How? Try it to see if you were right.

Note that when you do this, the _Task_ 'count_lines' is no longer up-to-date, but only the _Job '_test1.fastq.gz -> test1.nlines 'needs updating, and only this _Job_ will be run, the remaining _Jobs_ that are part of the _Task_ will be left alone.
 

The pipeline figures out weather it needs to run a task by first asking "does the output file exist?". If the output file does not exist, it obviously needs to be created. However, once it has checked if the file exists, it also checks if the date on the output file is more recent than the date on the input file. If it isn't, if the input file is more recent, then the output file needs replacing.

 Now lets consider what happens if an error happens half way through making the output file ... Lets say I forgot to convert what I read out of the input file into an integer before dividing it by 4. That is a had the line:

    nlines = infile_handle.read()
    nreads = nlines/4

This will produce an error and stop the pipeline. The correct code would be:

    nlines = infile_handle.read()
    nreads = int(nlines)/4

So I go back and fix the code. But now when I try to run my pipeline, it tells me the 'convert_to_nreads' task is up-to-date!!! Why is this? This is because the output file was created before the error happened. All the pipeline sees now is that the output file exists and is newer than the input, it doesn't know the last run was a failure, and the file is empty.

Thus, if you have an error while running a pipeline, you need to delete the output files from the task containing the error before continuing.

Run your pipeline with the following command:

    $ python ../solutions/lesson4.py make convert_to_reads -p1 --no-cluster

If there is an error, remember to delete the output flies before fixing it and continuing.

      $ rm *.nreads

Your directory should now look like this:

    $ ls
    pipeline.log test1.fastq.gz test1.nlines test1.nreads test2.fastq.gz test2.nlines test2.nreads test3.fastq.gz test3.nlines test3.nreads test4.fastq.gz test4.nlines test4.nreads test5.fastq.gz test5.nlines test5.nreads

and the contents of test1.nlines like this:

    $ cat test1.nreads
    test1  10

  

## Lesson 5: Merging it all together
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTc0MDMxMTk3Ml19
-->
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA2MzEwNjQxMiwtMjY5NjAxOTU4XX0=
-->