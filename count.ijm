var IMG_NAME = "j2_cropped"
var IMG_PATH = "images/" + IMG_NAME + ".png"

// Absolute path required for some reason
var OUT_PATH = "/Users/damon/Documents/coding/repos/cis4720/jumbles/";
var OUT_FILE = "data/" + IMG_NAME + ".xls"

var delta = 9.9;
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



