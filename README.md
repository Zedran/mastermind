<h1>Mastermind</h1>

<h2>Introduction</h2>
<p style="text-indent:40px">Mastermind game written in Python.Mastermind is a two-player game in which one person sets the code and the other tries to figure it out. In this implementation, the player guesses the code set by the AI.</p>

<h3>Features</h3>
    <ul>
        <li>Customizable theme</li>
        <li>Languages:
            <ul>
                <li>EN - English</li>
                <li>PL - Polish</li>
            </ul>
        </li>
    </ul>

<br>
<h2>Rules</h2>
<ul>
    <li>The code consists of 4 elements with no repetitions</li>
    <li>There are 8 different elements to chose from. They all have a unique color and are numbered for convenience</li>
    <li>Once the code is set, <i>the guesser</i> attempts to solve the code</li>
    <li>Each time <i>the guesser</i> submits the code, <i>the setter</i> evaluates it by inserting proper feedback pins. There is one feedback pin per element. Their order do not match that of the code. Their meaning is as follows:
        <ul>
            <li>Red pin indicates that one of the elements is of correct kind and in correct place</li>
            <li>White pin indicates that one of the elements is of correct kind but in incorrect place</li>
            <li>No feedback pin means that one of the elements does not exist in the code</li>
        </ul>
    </li>
    <li>The game is over once "the guesser" finds the correct code or fails to do so in 12 attempts.</li>
</ul>

<br>
<h2>Resources</h2>
    <ul>
        <li>
            <a href="https://www.pygame.org/">Pygame</a>
        </li>
    </ul>
