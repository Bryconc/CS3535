# Problem #
We want to be able to have a means to compare songs.

# Question #
1. What potential ways do we have to compare music?
2. What features does Echonest provide that could help us?
3. Are there any 3rd Party Libraries that could help?

# Resources #
1. [Comparison of Medieval, Renaissance & Baroque Musical Styles]
2. [Echonest Developer Forums]
    a. [Song2Song Documentation]
3. [musicg - Java Library]

### 1. Mini-abstract and relevance of [Comparison of Medieval, Renaissance & Baroque Musical Styles]

There are many channels across which music can be compared. We must find it important to specify the attributes we find important in our comparisons. Given the abstract nature of the term "comparison" (i.e. what are we specifically trying to compare about these multiple items) and the broad spectrum of attributes applicable to music, comparison in a generic form would be almost impossible to generalize. The resource mentions specifically looks at multiple time periods (Medieval, Renaissance & Baroque) and compares their overall musical styles. For this analysis, theauthor chose to focus on specific musical qualities: tone color, texture, harmony, rhythm, melody, and form. By defining these specific traits, the author firmly gave grounds for comparison. Youcan also see [Tristan's Compartive Description Forum Post] where he describes in brief what goes into comparing songs.

### 2. Mini-abstract and relevance of [Echonest Developer Forums] and [Song2Song Documentation] ###

While the concepts of comparisons are subject to pre-defined qualities, Echonest details a feature that it names "Song2Song". While it looks like a feature that is only available to commercial partners, this feature boasts to be a replacement for conventional collaborative filtering techniques. The engine seeks to be a "partial or total recommendation engine". Its uniqueness stems from its capabilities to include both cultural context and acoustic similarity. Cultural context is achieved through countless amounts of data acquired through web crawling. Acoustic similarity would be calculated using Echonest's public API featured, so long as you have an idea of what qualities you want to consider.

### 3. Mini-abstract and relevance of [musicg - Java Library] ###

A variety of free 3rd party libraries may help us in determining music comparisons. An example of this would be the musicg library. Written in Java, this library seeks to provide both high and low-level audio analysis. I found an interesting example of computing similarity through [FingerprintRecognition]. Following the code through to [FingerprintSimilarity] and [Wave], you eventually can read how they compute Fingerprint Similarity in [FingerprintSimilarityComputer].


[Comparison of Medieval, Renaissance & Baroque Musical Styles]: http://people.emich.edu/dpierce/Med_Ren_table.html
[Tristan's Compartive Description Forum Post]: http://developer.echonest.com/forums/thread/1687#post5601
[Echonest Developer Forums]: http://developer.echonest.com/forums/thread/334
[Song2Song Documentation]: https://docs.google.com/viewer?url=https%3A%2F%2Fechonest-corp.s3.amazonaws.com%2Fdocs%2Fwhitepapers%2FSong2Song-1_0.pdf
[musicg - Java Library]: https://code.google.com/p/musicg/
[FingerprintRecognition]: https://code.google.com/p/musicg/source/browse/src/com/musicg/main/demo/FingerprintRecognitionDemo.java?r=f2fbf166a1d95059650274d6ee668ec08fec03cf
[FingerprintSimilarity]: https://code.google.com/p/musicg/source/browse/src/com/musicg/fingerprint/FingerprintSimilarity.java?r=f2fbf166a1d95059650274d6ee668ec08fec03cf
[Wave]: https://code.google.com/p/musicg/source/browse/src/com/musicg/wave/Wave.java?r=f2fbf166a1d95059650274d6ee668ec08fec03cf
[FingerSimilarityComputer]: https://code.google.com/p/musicg/source/browse/src/com/musicg/fingerprint/FingerprintSimilarityComputer.java