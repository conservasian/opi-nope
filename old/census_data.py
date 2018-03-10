import matplotlib.pyplot as plt

from xlrd import open_workbook

def main():
    # Get column header information.
    mastdata_filename = 'data/census/Mastdata.xls'
    mastdata = read_mastdata(mastdata_filename)

    # Read a census data spreadsheet.
    health_data_filename = ['data/census/HEA01.xls',
        'data/census/HEA02.xls']
    health_data = dict()
    for filename in health_data_filename:
        health_data = read_census_sheet(filename, health_data)


    for stcou, county_data in health_data.items():
        fig = plt.figure()
        ax = fig.add_subplot(111)

        if stcou == '00000':
            continue

        for header, value in county_data.items():
            if header == 'name':
                print(value)
                continue

            print(mastdata[header])
            print(parse_header(header))
            header_dict = parse_header(header)

            if header_dict['series'] == '270':
                ax.plot(header_dict['year'], value, 'k.')
                title = '{} {}'.format(county_data['name'],
                    mastdata[header]['description'])
                ax.set_title(title)




        plt.show()

    return


def read_census_sheet(filename, census_data=None):
    if census_data is None:
        census_data = dict()

    census_book = open_workbook(filename)
    for i in range(census_book.nsheets):
        census_sheet = census_book.sheet_by_index(i)

        # Go through all rows.
        for j in range(1, census_sheet.nrows):
            stcou = census_sheet.cell_value(rowx=j, colx=1)

            if stcou in census_data.keys():
                county_data = census_data[stcou]
            else:
                county_data = dict()

            county_data['name'] = census_sheet.cell_value(rowx=j, colx=0)

            # Find column indices that correspond to actual data.
            for k in range(2, census_sheet.ncols):
                header_name = census_sheet.cell_value(rowx=0, colx=k)
                if header_name.endswith('D'):
                    county_data[header_name] = census_sheet.cell_value(rowx=j,
                        colx=k)

            census_data[stcou] = county_data

    return census_data


def read_mastdata(filename):
    '''
    Read MASTDATA file, which includes information about what each column header
    represents within each of the census data spreadsheets.
    '''
    # Open workbook + get first (and only) sheet.
    mastdata_book = open_workbook(filename)
    mastdata_sheet = mastdata_book.sheet_by_index(0)

    mastdata = dict()

    for i in range(1, mastdata_sheet.nrows):
        # Get info about each item and store it in a dictionary.
        item_dict = dict()

        # Short description of what the item ID represents.
        item_dict['description'] = mastdata_sheet.cell_value(rowx=i, colx=1)

        # Units (dollars, percentage, number, etc.)
        item_dict['units'] = mastdata_sheet.cell_value(rowx=i, colx=2)

        # Gives the location of the decimal place. '0' means you don't have to
        # do anything. '1' means you need to divide by 10, etc.
        item_dict['decimal'] = mastdata_sheet.cell_value(rowx=i, colx=3)

        # Overall total in the United States.
        item_dict['us_total'] = mastdata_sheet.cell_value(rowx=i, colx=4)

        # Add item_dict to the overall dictionary.
        item_id = mastdata_sheet.cell_value(rowx=i, colx=0)

        mastdata[item_id] = item_dict

    return mastdata


def parse_header(header):
    header_data = dict()
    header_data['group'] = header[:3]
    header_data['series'] = header[3:6]
    year = header[6:9]
    if year.startswith('1'):
        header_data['year'] = int('19' + year[1:])
    else:
        header_data['year'] = int('20' + year[1:])

    return header_data

if __name__ == '__main__':
    main()
