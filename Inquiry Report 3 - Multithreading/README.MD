# Problem #
We want to be able to multithread our applications to increase performance and output rate.

# Questions #
1. How's multithreading supported in Python?
2. What is threading vs multiprocessing?
3. When should we use each?

# Resources #
1. [Python Multithreading Tutorial]
2. [Parallelising Python with Threading and Multiprocessing]
3. [Parallelising Python with Threading and Multiprocessing]

### Mini-abstract and relevance of [Python Multithreading Tutorial] ###

This tutorial page will explain, in brief, the basics of using threading in Python.

Initially this could be done by spawning a new thread Object from the thread module, like so.

```python

    thread.start_new_thread ( function, args[, kwargs] )
```

Where "function" would be the function executed by the thread and "kwargs" would be the parameters passed to that function. This is now quite limited compared to the newer threading module.

The threading module contains a few basic methods that makes multithreading easy and powerful.
>**threading.activeCount():** Returns the number of thread objects that are active.
>
>**threading.currentThread():** Returns the number of thread objects in the caller's thread control.
>
>**threading.enumerate():** Returns a list of all thread objects that are currently active.
>
>In addition to the methods, the threading module has the Thread class that implements threading. The methods provided by the Thread class are as follows:
>
>**run():** The run() method is the entry point for a thread.
>
>**start():** The start() method starts a thread by calling the run method.
>
>**join([time]):** The join() waits for threads to terminate.
>
>**isAlive():** The isAlive() method checks whether a thread is still executing.
>
>**getName():** The getName() method returns the name of a thread.
>
>**setName():** The setName() method sets the name of a thread.

To create your own thread class you simply need to:

>Define a new subclass of the Thread class.
>
>Override the __init__(self [,args]) method to add additional arguments.
>
>Then, override the run(self [,args]) method to implement what the thread should do when started.

Once you've created your Thread class you simply need to call start() on it, which will in turn call the run() method.

I have included a threading_example.py script which demonstrates the concepts I just highlighted. It will print messages at different intervals from two separate threads. At the moment Thread 1 will print 7 messages at a rate of a message per 3 seconds, and Thread 2 will produce 3 messages at a rate of a message per 7 seconds.

The output and proof of concept is reproduced here.

>C:\Users\Brycon\Anaconda\python.exe "C:/Users/Brycon/PycharmProjects/CS3535/Inquiry Report 3 - Multithreading/threading_example.py"
>Printing from Thread 1
>Waiting 3 seconds
>Printing from Thread 2
>
>Waiting 7 seconds
>Printing from Thread 1
>Waiting 3 seconds
>Printing from Thread 1
>Waiting 3 seconds
>Printing from Thread 2
>Waiting 7 seconds
>Printing from Thread 1
>Waiting 3 seconds
>Printing from Thread 1
>Waiting 3 seconds
>Printing from Thread 2
>Thread 2 finished execution.
>Printing from Thread 1
>Waiting 3 seconds
>Printing from Thread 1
>Thread 1 finished execution.
>Process finished with exit code 0

More information about threading can be found in the [Python API - threading module]

### Mini-abstract and relevance of [Parallelising Python with Threading and Multiprocessing] ###

There are actually two forms of parallel processing in Python: threading and multiprocessing. So what are the differences and when should I use each?

A common misconception is that threading should make use of multiple processing cores. This is not true because of a process known as the Global Interpreter Lock (GIL). Because the Python interpreter itself
is not *thread safe*, the GIL permits only a single thread to access a Python Object at a time. However, multiple cores are accessible, if you use the mulitprocessing library.

The multiprocessing library, though it appears similar to the threading library, works in a fundamentally different way. It actually spawns multiple operating system *processes* for each parallel task. This gets around
the GIL because it gives each process a copy of the Python interpreter.

### When to use each ###

**Use threading when data is...**

* network-bound - must be accessed via the Internet
* I/O bound - must be read-in or output from/to somewhere else

**Use multiprocessing when data is...**

* CPU-bound - must be calculated or produced solely by the code




[Python API - threading module]:https://docs.python.org/2/library/threading.html#module-threading
[Python Multithreading Tutorial]:http://www.tutorialspoint.com/python/python_multithreading.htm
[Parallelising Python with Threading and Multiprocessing]:http://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing