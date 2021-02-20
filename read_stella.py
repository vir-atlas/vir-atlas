# @author Marisa Loraas
# 2/20/2021
# @brief: reads in files that have the same output format as STELLA and makes a StellaPoint object, which can
# access all possible attributes of stella given in the excel column header file (besides the "mark" objects)


import StellaPoint as SP


def make_stella_points(file):
    points = list()

    # check if the length of each list in points is correct
    for line in file:
        points.append(line.rstrip().split(', '))

    for point in list(points):
        if len(point) != 57:
            print("Error in Format of file, please check again")
            return
        for part in point:
            if part.find('_') != -1 or part.find('hh.hhhh') != -1:
                point.remove(part)
            if part.isnumeric():
                point[point.index(part)] = int(part)
            try:
                point[point.index(part)] = float(part)
            except ValueError:
                continue
    stella_points = list()
    for point in list(points):
        stella = SP.StellaPoint(point[0], point[1], point[2], point[3], point[4], point[5], point[6], point[7], point[8],
                                point[9], point[10], point[11], point[12], point[13], point[14], point[15], point[16],
                                point[17], point[18], point[19], point[20], point[21], point[22], point[23], point[24],
                                point[25], point[26], point[27], point[28], point[29], point[30], point[31], point[32],
                                point[33], point[34], point[35], point[36], point[37], point[38], point[39], point[40],
                                point[41], point[42], point[43], point[44], point[45], point[46], point[47], point[48])
        stella_points.append(stella)
    return stella_points


def main():
    try:
        # the way we read this file will probably change
        stella_output = open('data.txt', 'r')
    except FileNotFoundError as no_file:
        print("Error in reading stella input file", no_file)
    else:
        file = stella_output.readlines()
        stella_points = make_stella_points(file)
        #  stella_points: list of all StellaPoint objects in the order given by the file
        stella_output.close()


if __name__ == '__main__':
    main()
