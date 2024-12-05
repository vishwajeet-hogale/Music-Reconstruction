# Music-Reconstruction With Genetic Algorithms
In this project, we reconstruct music from various components extracted from an input of MIDI files, using genetic algorithms to create better sounding samples.

Authors: [Justin Feldman](https://github.com/jfeldm02), [Garapati Venkata Krishna Rayalu ](https://github.com/VenkataKrishnaGarapati), [Vishwajeet Hogale](https://github.com/vishwajeet-hogale), [Arzoo Jiwani](https://github.com/ArzooMJ), [Annamayya Vennelakanti](https://github.com/Annamayya9), [Jason Zou](https://github.com/zoujas)

# Motivation
As a group of engineers and musicians, we naturally wanted to explore the intersection of AI, mathematics, and music. Our goal is to take existing songs and use genetic algorithms to generate new, euphonious songs from existing samples. In particular, we wanted to see how an artificial intelligence can optimize and find the best sounding songs given elementary building blocks. 

# Built With
[![Python](https://www.python.org/community/logos/python-logo.png)](https://www.python.org/)

[Node.js](https://nodejs.org/en)

# Getting Started

Requirements:

[npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

[Node.js v22.12](https://nodejs.org/en/download/package-manager)

[Python 3.11](https://www.python.org/downloads/release/python-3110/)

[numpy 2.1.3](https://pypi.org/project/numpy/) 

[pretty_midi 0.2.10](https://pypi.org/project/pretty_midi/) 

This project includes a GUI to simplify user interactions. To start:
1) Clone the repository onto your local machine.

2) In the command terminal of your choice, navigate to the directory containing the project. Run the command "npm start" in the terminal.

3) The GUI should launch in a localhost. On the main page of the GUI, there is an option to choose the MIDI files you are working with.

4) After you have uploaded your files, you can start generating a new song using the "Recycle" button, which will perform a set number of iterations of the genetic algorithm on random subsets of the MIDI dataset that you submitted in step 4.

5) You can listen to the current song the algorithm has produced, or press the "Continue Recycling" button to process the song for more generations.

# Contents
The genetic algorithm is executed over the course of multiple files.

feature_extractor.py is a preprocessing file that holds numerous helper functions. These functions separates midi files into separate instruments and establishes their various features, such as velocity, tempo, pitch, and key. 

genetic_algorithm.py contains all of the parts required to successfully conduct a genetic algorithm. The code to generate random populations, mutate individuals, conduct crossover, and evaluating an individual using the fitness function can all be found in this file.

Finally, main.py calls on the functions from genetic_algorithm.py to begin the process.


# Results
After running the genetic algorithm, the user should obtain the final, most fit song in the form of a  MIDI file, which can downloaded from the GUI. Here is a sample of what the best song may sound like:

https://github.com/user-attachments/assets/9ba4728d-c9b2-4209-a190-3d8c79ac211a

Your song may sound radically different, but this sample should show what the user can expect as an output.

We would also like to present these whisker plots to show what the user might expect in terms of the population's fitness score across multiple generations.

The figures below represent an example of our algorithm’s population fitness score’s distributions and their trends over the course of the evolutionary process. The population fitness score distributions shown were sampled at 10 equally incremented generations over the course of 100 generations. The rebuilt populations between fitness scoring were comprised of 20% mutated individuals, 20% crossed over individuals, and 20% best fit individuals from the previous generation’s population, along with 40% randomly generated individuals.

 

While the scatter plot does not reveal any significant change in the maximum and minimum individual values over the generations,  the box-and-whisker plot clearly shows that the upper quartile individual fitness scores improve over the generations. Given that genetic algorithms are intended to improve the fitness of populations towards an objectively desired outcome, the upper quartile’s positive trend conclusively shows the functionality of our algorithm.

![Whisker_100Gen](https://github.com/user-attachments/assets/f4a00640-5570-4091-88a1-0e5b76be6ab9)
![Scatter_100](https://github.com/user-attachments/assets/498a9d73-c76d-480d-a2c1-0d2c10bb08a4)



