'''This is a custom layout for the RPi InfoScreen wordclock screen.

    Custom layouts can be created for the screen by creating a new file in the
    "layouts" folder.

    Each layout must have the following variables:
        LAYOUT:   The grid layout. Must be a single string.
        MAP:      The mapping required for various times (see notes below)
        COLS:     The number of columns required for the grid layout
        SIZE:     The size of the individual box containing your letter.
                  Tuple in (x, y) format.
        FONTSIZE: Font size for the letter
'''

# Layout is a single string variable which will be looped over by the parser.
LAYOUT = ("ITQISHCUBMWLRPI"
          "AOQUARTERFDHALF"
          "TWENTYSFIVEGTEN"
          "TOXPASTNYTWELVE"
          "ONESIXTHREENINE"
          "SEVENTWOXELEVEN"
          "EIGHTENFOURFIVE"
          "RPIO'CLOCKHAMPM")

# Map instructions:
# The clock works by rounding the time to the nearest 5 minutes.
# This means that you need to have settngs for each five minute interval "m00"
# "m00", "m05".
# The clock also works on a 12 hour basis rather than 24 hour:
# "h00", "h01" etc.
# There are three optional parameters:
#   "all": Anything that is always shown regardless of the time e.g. "It is..."
#   "am":  Wording/symbol to indicate morning.
#   "pm":  Wording/symbol to indicate afternoon/evening
MAP = {
       "all": [0, 1, 3, 4],
       "m00": [108, 109, 110, 111, 112, 113, 114],
       "m05": [37,38, 39, 40, 48, 49, 50, 51],
       "m10": [42, 43, 44, 48, 49, 50, 51],
       "m15": [15, 17, 18, 19, 20, 21, 22, 23, 48, 49, 50, 51],
       "m20": [30, 31, 32, 33, 34, 35, 48, 49, 50, 51],
       "m25": [30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 48, 49, 50, 51],
       "m30": [26, 27, 28, 29, 48, 49, 50, 51],
       "m35": [30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 45, 46],
       "m40": [30, 31, 32, 33, 34, 35, 45, 46],
       "m45": [15, 17, 18, 19, 20, 21, 22, 23, 45, 46],
       "m50": [42, 43, 44, 45, 46],
       "m55": [37, 38, 39, 40, 45, 46],
       "h01": [60, 61, 62],
       "h02": [80, 81, 82],
       "h03": [66, 67, 68, 69, 70],
       "h04": [97, 98, 99, 100],
       "h05": [101, 102, 103, 104],
       "h06": [63, 64, 65],
       "h07": [75, 76, 77, 78, 79],
       "h08": [90, 91, 92, 93, 94],
       "h09": [71, 72, 73, 74],
       "h10": [94, 95, 96],
       "h11": [84, 85, 86, 87, 88, 89],
       "h12": [54, 55, 56, 57, 58, 59],
       "am": [116, 117],
       "pm": [118, 119]
  }

# Number of columns in grid layout
COLS = 15

# Size of letter in grid (x, y)
SIZE = (53, 60)

# Font size of letter
FONTSIZE = 40
