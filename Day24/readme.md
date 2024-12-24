# P24: Santa's here!

## 🧠 The problem

🎅 Santa's coming!

🎄 Santa needs to deliver presents to children all over the world before Christmas morning 🎁.

However, there are some challenges:

Each child has a specific time window when they are available to receive their gift (maybe they're asleep 😴 or out playing 🛝).
Santa's sleighs have a capacity limit 🛷, and given the massive scale of this operation, he must decide how many helpers (sleigh drivers) are needed to complete all the deliveries efficiently.
Here's the catch:

🦌 The reindeers travel at 1000 km/h, and they go in a straight line 🛤️ from one house to another.

🎯 The goal?

Determine how many sleigh drivers Santa needs.
Plan the sequence of deliveries for each driver to ensure every child gets their gift on time! 🕰️
Can you help Santa save Christmas? 🎅✨

Get the important things from the definition (objective function, constraints, decision variables)
Document your journey

Link to the [post](https://www.linkedin.com/posts/borjamenendezmoreno_operationsresearch-activity-7277227758991142913-Hamd?utm_source=share&utm_medium=member_desktop)

At the top of the page... You can check the [leaderboard!](https://orfrom0to1.bmenendez.com/tf/c/eyJ2Ijoie1wiYVwiOjUyODU2NixcImxcIjoxNDEyMTQ5Mzc4NDAwOTI0MjYsXCJyXCI6MTQxNTg2OTM0MDE5MzkzMTA4fSIsInMiOiJjYWJiMGI5MzkwNmFiNTAxIn0)

## Analysis

This is a CVRPTW. I'll try using the OR Tools solver.

Variables: sequence of node visits for each vehicle

Constraints:

- sleigh capacity
- time windows
- all gifts are delivered

## Results

Solution after 5 mins with Tabu Search heuristic:

```
Sleigh 1: Load 12420
Santa's depot 0: Time 420
Child 174: Time 482 [420, 1080] Demand 4710
Child 164: Time 720 [720, 750] Demand 1770
Child 144: Time 761 [420, 1080] Demand 3990
Child 132: Time 825 [420, 1080] Demand 1950

Sleigh 2: Load 12090
Santa's depot 0: Time 420
Child 68: Time 720 [720, 765] Demand 3760
Child 20: Time 783 [420, 1080] Demand 2390
Child 13: Time 808 [420, 1080] Demand 1710
Child 110: Time 851 [420, 1080] Demand 4230

Sleigh 3: Load 12280
Santa's depot 0: Time 420
Child 1: Time 539 [420, 1080] Demand 2290
Child 5: Time 559 [420, 1080] Demand 4990
Child 59: Time 780 [780, 810] Demand 1810
Child 75: Time 855 [855, 900] Demand 2110
Child 194: Time 956 [930, 990] Demand 1080

Sleigh 5: Load 11860
Santa's depot 0: Time 420
Child 188: Time 915 [915, 975] Demand 2950
Child 60: Time 1013 [420, 1080] Demand 4570
Child 119: Time 1077 [420, 1080] Demand 4340

Sleigh 10: Load 12410
Santa's depot 0: Time 420
Child 99: Time 512 [420, 1080] Demand 1840
Child 52: Time 600 [600, 645] Demand 4750
Child 14: Time 720 [720, 780] Demand 1420
Child 25: Time 810 [810, 870] Demand 4400

Sleigh 11: Load 12000
Santa's depot 0: Time 420
Child 49: Time 735 [735, 765] Demand 3220
Child 32: Time 870 [870, 915] Demand 4490
Child 18: Time 905 [420, 1080] Demand 4290

Sleigh 12: Load 12340
Santa's depot 0: Time 420
Child 118: Time 615 [615, 675] Demand 3070
Child 117: Time 750 [750, 780] Demand 4070
Child 113: Time 789 [420, 1080] Demand 2970
Child 139: Time 820 [420, 1080] Demand 2230

Sleigh 13: Load 9380
Santa's depot 0: Time 420
Child 186: Time 468 [420, 1080] Demand 4050
Child 190: Time 525 [525, 570] Demand 1950
Child 192: Time 552 [420, 1080] Demand 3380

Sleigh 14: Load 12370
Santa's depot 0: Time 420
Child 56: Time 855 [855, 885] Demand 4740
Child 55: Time 903 [420, 1080] Demand 3240
Child 34: Time 958 [420, 1080] Demand 4390

Sleigh 15: Load 12540
Santa's depot 0: Time 420
Child 48: Time 528 [510, 570] Demand 1390
Child 3: Time 573 [420, 1080] Demand 2030
Child 6: Time 600 [420, 1080] Demand 2770
Child 35: Time 765 [765, 810] Demand 1850
Child 74: Time 800 [420, 1080] Demand 4500

Sleigh 16: Load 12560
Santa's depot 0: Time 420
Child 107: Time 675 [675, 705] Demand 1200
Child 62: Time 736 [420, 1080] Demand 3260
Child 69: Time 840 [840, 900] Demand 4910
Child 88: Time 876 [870, 900] Demand 1000
Child 80: Time 899 [420, 1080] Demand 2190

Sleigh 17: Load 11980
Santa's depot 0: Time 420
Child 66: Time 524 [510, 540] Demand 3400
Child 41: Time 585 [585, 630] Demand 4510
Child 71: Time 750 [750, 810] Demand 4070

Sleigh 18: Load 11900
Santa's depot 0: Time 420
Child 112: Time 509 [420, 1080] Demand 2610
Child 94: Time 555 [555, 585] Demand 2120
Child 57: Time 598 [420, 1080] Demand 4360
Child 70: Time 632 [420, 1080] Demand 1750
Child 147: Time 701 [675, 735] Demand 1060

Sleigh 19: Load 12500
Santa's depot 0: Time 420
Child 77: Time 795 [795, 840] Demand 2800
Child 28: Time 855 [855, 900] Demand 3900
Child 11: Time 893 [420, 1080] Demand 3740
Child 8: Time 942 [420, 1080] Demand 2060

Sleigh 20: Load 12310
Santa's depot 0: Time 420
Child 78: Time 810 [810, 840] Demand 4220
Child 39: Time 871 [420, 1080] Demand 1290
Child 23: Time 900 [420, 1080] Demand 3030
Child 12: Time 940 [420, 1080] Demand 3770

Sleigh 21: Load 11980
Santa's depot 0: Time 420
Child 114: Time 508 [420, 1080] Demand 1780
Child 91: Time 825 [825, 855] Demand 2530
Child 58: Time 861 [420, 1080] Demand 2660
Child 43: Time 889 [420, 1080] Demand 2480
Child 90: Time 922 [420, 1080] Demand 2530

Sleigh 22: Load 11990
Santa's depot 0: Time 420
Child 82: Time 645 [645, 705] Demand 3650
Child 63: Time 780 [780, 810] Demand 2250
Child 65: Time 885 [885, 915] Demand 4190
Child 141: Time 948 [420, 1080] Demand 1900

Sleigh 23: Load 10520
Santa's depot 0: Time 420
Child 187: Time 468 [420, 1080] Demand 3180
Child 179: Time 900 [900, 945] Demand 1440
Child 172: Time 939 [420, 1080] Demand 3300
Child 182: Time 984 [420, 1080] Demand 2600

Sleigh 24: Load 12300
Santa's depot 0: Time 420
Child 145: Time 499 [465, 525] Demand 4910
Child 143: Time 855 [855, 885] Demand 4400
Child 163: Time 907 [420, 1080] Demand 2990

Sleigh 25: Load 12410
Santa's depot 0: Time 420
Child 115: Time 615 [615, 675] Demand 1980
Child 10: Time 659 [420, 1080] Demand 4960
Child 2: Time 704 [675, 735] Demand 1250
Child 24: Time 735 [420, 1080] Demand 2450
Child 47: Time 840 [840, 885] Demand 1770

Sleigh 26: Load 12600
Santa's depot 0: Time 420
Child 92: Time 517 [420, 1080] Demand 2180
Child 76: Time 825 [825, 885] Demand 3790
Child 42: Time 866 [420, 1080] Demand 2580
Child 67: Time 899 [420, 1080] Demand 3020
Child 104: Time 953 [420, 1080] Demand 1030

Sleigh 27: Load 12180
Santa's depot 0: Time 420
Child 33: Time 765 [765, 795] Demand 2720
Child 31: Time 813 [765, 825] Demand 3730
Child 64: Time 870 [840, 885] Demand 3700
Child 123: Time 936 [420, 1080] Demand 2030

Sleigh 28: Load 12560
Santa's depot 0: Time 420
Child 61: Time 840 [840, 900] Demand 3830
Child 51: Time 879 [420, 1080] Demand 3740
Child 26: Time 935 [420, 1080] Demand 1760
Child 4: Time 961 [420, 1080] Demand 1600
Child 44: Time 1022 [420, 1080] Demand 1630

Sleigh 29: Load 11700
Santa's depot 0: Time 420
Child 146: Time 540 [540, 585] Demand 2450
Child 22: Time 589 [420, 1080] Demand 4690
Child 45: Time 840 [840, 885] Demand 4560

Sleigh 30: Load 12570
Santa's depot 0: Time 420
Child 37: Time 570 [570, 630] Demand 3880
Child 54: Time 615 [615, 660] Demand 4970
Child 46: Time 780 [780, 825] Demand 2100
Child 101: Time 819 [420, 1080] Demand 1620

Sleigh 31: Load 11170
Santa's depot 0: Time 420
Child 86: Time 840 [840, 900] Demand 4260
Child 79: Time 861 [420, 1080] Demand 4880
Child 95: Time 894 [885, 915] Demand 2030

Sleigh 32: Load 12240
Santa's depot 0: Time 420
Child 158: Time 495 [420, 1080] Demand 2240
Child 89: Time 541 [540, 600] Demand 1140
Child 40: Time 750 [750, 780] Demand 2100
Child 7: Time 805 [420, 1080] Demand 3440
Child 36: Time 849 [420, 1080] Demand 1930
Child 38: Time 900 [900, 930] Demand 1390

Sleigh 33: Load 12070
Santa's depot 0: Time 420
Child 111: Time 510 [420, 1080] Demand 3800
Child 98: Time 615 [615, 645] Demand 4250
Child 97: Time 810 [810, 870] Demand 2090
Child 167: Time 915 [915, 960] Demand 1930

Sleigh 34: Load 12410
Santa's depot 0: Time 420
Child 124: Time 504 [420, 1080] Demand 2910
Child 102: Time 557 [420, 1080] Demand 3650
Child 116: Time 825 [825, 870] Demand 1280
Child 127: Time 873 [420, 1080] Demand 4570

Sleigh 35: Load 12490
Santa's depot 0: Time 420
Child 152: Time 498 [420, 1080] Demand 2550
Child 30: Time 578 [420, 1080] Demand 3870
Child 27: Time 765 [765, 810] Demand 1640
Child 50: Time 870 [870, 915] Demand 4430

Sleigh 36: Load 12280
Santa's depot 0: Time 420
Child 191: Time 464 [420, 1080] Demand 1950
Child 178: Time 555 [555, 615] Demand 4890
Child 181: Time 735 [735, 795] Demand 3430
Child 199: Time 885 [885, 915] Demand 2010

Sleigh 37: Load 12230
Santa's depot 0: Time 420
Child 151: Time 855 [855, 915] Demand 4760
Child 159: Time 889 [420, 1080] Demand 1970
Child 161: Time 913 [870, 930] Demand 4280
Child 198: Time 971 [945, 990] Demand 1220

Sleigh 38: Load 11990
Santa's depot 0: Time 420
Child 21: Time 780 [780, 840] Demand 1310
Child 15: Time 835 [810, 870] Demand 1920
Child 17: Time 861 [840, 870] Demand 4300
Child 53: Time 914 [420, 1080] Demand 4460

Sleigh 39: Load 11430
Santa's depot 0: Time 420
Child 142: Time 585 [585, 645] Demand 2210
Child 125: Time 870 [870, 915] Demand 3070
Child 109: Time 900 [900, 930] Demand 1420
Child 105: Time 951 [420, 1080] Demand 4730

Sleigh 40: Load 9900
Santa's depot 0: Time 420
Child 121: Time 505 [420, 1080] Demand 4590
Child 122: Time 549 [420, 1080] Demand 3890
Child 126: Time 855 [855, 900] Demand 1420

Sleigh 41: Load 12240
Santa's depot 0: Time 420
Child 138: Time 885 [885, 945] Demand 4890
Child 135: Time 915 [420, 1080] Demand 3020
Child 129: Time 956 [420, 1080] Demand 4330

Sleigh 42: Load 12300
Santa's depot 0: Time 420
Child 154: Time 615 [615, 675] Demand 2760
Child 100: Time 690 [690, 750] Demand 1300
Child 96: Time 840 [840, 900] Demand 3340
Child 93: Time 885 [885, 945] Demand 4900

Sleigh 43: Load 11870
Santa's depot 0: Time 420
Child 156: Time 885 [885, 945] Demand 4410
Child 133: Time 930 [930, 960] Demand 1950
Child 136: Time 954 [420, 1080] Demand 3670
Child 140: Time 971 [420, 1080] Demand 1840

Sleigh 44: Load 11860
Santa's depot 0: Time 420
Child 165: Time 750 [750, 795] Demand 2920
Child 150: Time 808 [795, 855] Demand 1430
Child 155: Time 861 [855, 915] Demand 4380
Child 176: Time 945 [945, 975] Demand 3130

Sleigh 45: Load 11410
Santa's depot 0: Time 420
Child 175: Time 482 [420, 1080] Demand 1630
Child 171: Time 523 [420, 1080] Demand 4000
Child 168: Time 569 [420, 1080] Demand 3220
Child 183: Time 825 [825, 870] Demand 2560

Sleigh 48: Load 10170
Santa's depot 0: Time 420
Child 108: Time 645 [645, 690] Demand 4300
Child 103: Time 665 [420, 1080] Demand 4570
Child 170: Time 885 [885, 915] Demand 1300

Sleigh 50: Load 11970
Santa's depot 0: Time 420
Child 149: Time 498 [420, 1080] Demand 3250
Child 73: Time 690 [690, 750] Demand 3880
Child 85: Time 855 [855, 885] Demand 1460
Child 106: Time 910 [900, 930] Demand 3380

Sleigh 51: Load 12380
Santa's depot 0: Time 420
Child 148: Time 498 [420, 1080] Demand 3040
Child 153: Time 780 [780, 825] Demand 4330
Child 157: Time 813 [420, 1080] Demand 3030
Child 185: Time 866 [420, 1080] Demand 1980

Sleigh 52: Load 10880
Santa's depot 0: Time 420
Child 166: Time 489 [420, 1080] Demand 4450
Child 120: Time 529 [420, 1080] Demand 3420
Child 137: Time 915 [915, 945] Demand 1100
Child 160: Time 987 [420, 1080] Demand 1910

Sleigh 53: Load 12250
Santa's depot 0: Time 420
Child 180: Time 540 [540, 585] Demand 2390
Child 162: Time 595 [420, 1080] Demand 1840
Child 169: Time 635 [420, 1080] Demand 4000
Child 177: Time 945 [945, 975] Demand 4020

Sleigh 54: Load 11540
Santa's depot 0: Time 420
Child 87: Time 518 [420, 1080] Demand 1180
Child 19: Time 795 [795, 825] Demand 1680
Child 72: Time 855 [855, 885] Demand 2980
Child 81: Time 900 [420, 1080] Demand 1250
Child 83: Time 942 [420, 1080] Demand 4450

Sleigh 55: Load 12160
Santa's depot 0: Time 420
Child 197: Time 460 [420, 1080] Demand 2830
Child 184: Time 750 [750, 810] Demand 4220
Child 189: Time 780 [420, 1080] Demand 3580
Child 196: Time 840 [840, 870] Demand 1530

Sleigh 56: Load 12020
Santa's depot 0: Time 420
Child 173: Time 483 [420, 1080] Demand 2390
Child 130: Time 554 [420, 1080] Demand 4510
Child 134: Time 750 [750, 780] Demand 1840
Child 131: Time 870 [870, 900] Demand 3280

Sleigh 57: Load 11660
Santa's depot 0: Time 420
Child 84: Time 675 [675, 720] Demand 2040
Child 29: Time 704 [420, 1080] Demand 2730
Child 16: Time 750 [420, 1080] Demand 2190
Child 9: Time 825 [825, 870] Demand 2020
Child 128: Time 912 [420, 1080] Demand 2680

Summary:
Active sleighs: 50
Total time: 10800 minutes
Total load: 595320
Total demand: 595320

```
