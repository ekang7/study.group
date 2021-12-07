


time_to_index = {
                    "12:00am": 0,
                    "12:30am": 1,
                    "1:00am": 2,
                    "1:30am": 3, 
                    "2:00am": 4, 
                    "2:30am": 5,
                    "3:00am": 6, 
                    "3:30am": 7,
                    "4:00am": 8, 
                    "4:30am": 9,
                    "5:00am": 10,
                    "5:30am": 11,
                    "6:00am": 12,
                    "6:30am": 13,
                    "7:00am": 14,
                    "7:30am": 15, 
                    "8:00am": 16,
                    "8:30am": 17,
                    "9:00am": 18,
                    "9:30am": 19,
                    "10:00am": 20,
                    "10:30am": 21,
                    "11:00am": 22,
                    "11:30am": 23,
                    "12:00pm": 24,
                    "12:30pm": 25, 
                    "1:00pm": 26,
                    "1:30pm": 27,
                    "2:00pm": 28,
                    "2:30pm": 29,
                    "3:00pm": 30,
                    "3:30pm": 31,
                    "4:00pm": 32, 
                    "4:30pm": 33,
                    "5:00pm": 34,
                    "5:30pm": 35, 
                    "6:00pm": 36, 
                    "6:30pm": 37, 
                    "7:00pm": 38, 
                    "7:30pm": 39, 
                    "8:00pm": 40, 
                    "8:30pm": 41,
                    "9:00pm": 42,
                    "9:30pm": 43,
                    "10:00pm": 44,
                    "10:30pm": 45, 
                    "11:00pm": 46, 
                    "11:30pm": 47
} 

timelist = ["2:00am", "10:30am", "10:30pm", "1:00am"]
matrix = []
for x in range(0,10):
    row = []

    for x in range(0,10):
        row.append(0)

    matrix.append(row)
stackedTimelines =[[0, 0], [0,0]] 
stackedTimelines = stackedTimelines + stackedTimelines
print(stackedTimelines)
for time in timelist: 
        index = time_to_index[time]
        print(index)
      #  stackedTimelines[index][0] += 1
     #   stackedTimelines[index][1]=time
stackedTimelines[0][0] +=1
print(len(stackedTimelines))
