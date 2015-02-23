## Pitch Quantifier ##

The application visualizes the recurrence of the 12 chromatic pitches at the segment level in a song/songs.

**Process**

The application receives a list of songs to quantify via command line. Then for each segment in said song/songs the application compiles a list of the summation of all pitch vectors. Finally, the application produces a bar graph, visualizing which pitches are more frequently found then others.

**Dependencies**

To use pitch_quantifier.py, you will need:

      - numpy
      - echonest.remix
      - matplotlib

**Example**

Execute pitch_quantifier.py with a song/songs to be visualized. For our example we will take the two songs Let It Go and For the First Time in Forever.

```
    python pitch_quantifier.py Let_It_Go.mp3 For_The_First_Time_In_Forever.mp3
```

The program will execute and produce the following image
<img src="https://github.com/Bryconc/CS3535/blob/master/Research%20Module%201/Pitch%20Frenquency%20Count%20for%20Let_It_Go.mp3,%20and%20For_The_First_Time_In_Forever.mp3.png?raw=true" alt="Pitch Quantified Graph Example" width="400" height="400">

If the program had been run on each song individually it would produce these two separate graphs
<img src="https://github.com/Bryconc/CS3535/blob/master/Research%20Module%201/Pitch%20Frenquency%20Count%20for%20For_The_First_Time_In_Forever.mp3.png?raw=true" alt="Pitch Quantified Graph Example - First Time" width="400" height="400">
<img src="https://github.com/Bryconc/CS3535/blob/master/Research%20Module%201/Pitch%20Frenquency%20Count%20for%20Let_It_Go.mp3.png?raw=true" alt="Pitch Quantified Graph Example - Let It Go" width="400" height="400">

**Code Explanation**

As a preliminary me must have a pitch vector set up to store the recurrence values. We will accumulate the data in said vector.

```python

    pitches = [0] * 12
```

Firstly, we must perform an audio analysis on every song provided as an argument. Furthermore, we are only interested in looking at pitches on the segment level. With each segment, we will send its pitch vector to accounted for.

```python

    try:
        audiofile = audio.LocalAudioFile(input_file)
        segments = audiofile.analysis.segments
        for segment in segments.pitches:
            add_to_vector(segment)

    except Exception as e:
        print("File specified not found.")
```

Let's take advantage of a feature of numpy: its add method (which can add vectors!).

```python

    def add_to_vector(pitch_vect):
        global pitches
        pitches = np.add(pitches, pitch_vect)
```
By taking advantage of the global keyword, we acknowledge that we're referring to the global pitch vector and not a local overshadowing variable. Now we can simply call the numpy's add method, passing it in the global pitch vector and the specific one we're adding in and assign the result to be the new global pitch vector.

Once we've accumulated all the data about pitch recurrence, it's time to graph our resulting data, courtesy of matplotlib's pyplot. But first there's some preliminary setup we need to take care of.

```python

    pitch_values = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    width = 0.75
    ind = np.arange(12)
```

The first statement creates a list of the 12 chromatic pitches we will use as labels for our graph. According to the [Analyzer Documentation],

>pitch content is given by a “chroma” vector, corresponding to the 12 pitch classes C, C#, D to B, with values ranging
from 0 to 1 that describe the relative dominance of every pitch in the chromatic scale.

Therefore, my list matches the indices specified in the pitch vector. The width value specifed will be the width of the bars in our graph. And the "ind" variable just represents the indices where the bars will placed on the x axis. numpy's arange method just generates an array of numbers ranging from 0-n.

Now we need to label the axes.
```python

    fig, ax = plot.subplots()
    ax.bar(ind, pitches)
    ax.set_xlabel('Pitches')
    ax.set_ylabel('Recurrence Values')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(pitch_values)
```

First we must be able to reference the axes of the plot. We get this via the secondary return of the subplots() method. We provide the plot with information on the bar graph: the indices of the bar and the values of each bar (the pitch vector).We can set the labels of the graph via their respective set_*label method. Then we have to position the "ticks" which are the smaller labels showing what each bar represents. We want to position these at the midpoint of the bar (ind + width / 2). Finally, we tell the graph what its tick labels will be (remember our pitch values from earlier?).

Now we've got our graph labeled appropriately and ready to go. For convenience's sake, we'll also have the program save the figure as a local file.

```python

    plot.title(title)
    plot.savefig(title + ".png")
    plot.show()
```


**Resources**
    1. [Analyzer Documentation]
    2. [pyploy Documentation]
    3. [numpy Documentation]


[Analyzer Documentation]: http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation.pdf
[pyploy Documentation]: http://matplotlib.org/api/pyplot_api.html
[numpy Documentation]: http://docs.scipy.org/doc/
