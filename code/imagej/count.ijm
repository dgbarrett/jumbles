// A macro for perfoming particle analysis on word jumble
// Jumble must be located in the images folder and be a png file
// Place the name of the file in the IMG variable and adjust the delta according to the output of step 1.
//		Deltas can also be found in a text file at data/saved_deltas.txt

var IMG = "j10"
var delta = 7.19;

var IMG_NAME = IMG + "_cropped"
var IMG_PATH = "../../images/" + IMG_NAME + ".png"

// Absolute path required for some reason
var OUT_PATH = "/Users/damon/Documents/coding/repos/cis4720/jumbles/";
var OUT_FILE = "data/particle_data/" + IMG_NAME + ".xls"

var minArea = (delta*delta) * 3.1415;

open(IMG_PATH)

// In case image is not binary already.
run("8-bit");
run("Make Binary");

// Invert to make circles into solid particles.
run("Invert");
// Find circles.
run("Analyze Particles...", "display size=&minArea-Infinity");

// Save results.
selectWindow("Results");
saveAs("results",OUT_PATH + OUT_FILE);

// Cleanup.
close("*");
selectWindow("Results");
run("Close");



