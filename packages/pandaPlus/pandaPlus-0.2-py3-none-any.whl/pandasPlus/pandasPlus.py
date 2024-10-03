'''
Function to write dataframe to excel without Pandas bold formatting.
'''
import xlsxwriter
import os
import pandas as pd

def clearFormatXlsx(df, path = r'/Users/' + os.getlogin() + '/Downloads/', fileName = 'Data', sheet = 1, sheetName = 'Sheet' + sheet, idx = False):

    #Save the columns
    columns = df.columns

    #Output to excel
    writer = pd.ExcelWriter(path + fileName + '.xlsx', engine = 'xlsxwriter')

    #Write with no header
    df.to_excel(writer, sheetName, startrow = sheet, header = False, index = idx)

    # Get workbook and worksheet
    workbook  = writer.book
    worksheet = writer.sheets[sheetName]

    #Add the columns back in
    for i, val in enumerate(columns):
        worksheet.write(0, i, val)

    writer.close()
