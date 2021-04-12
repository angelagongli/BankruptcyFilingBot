Sub ClearTransactionData(TransactionDataSheetName)
    Sheets(TransactionDataSheetName).Cells.Clear
End Sub

Sub ClearSavepointData()
    Sheets("SavepointData").Cells.Clear
End Sub

Sub ClearSavepointDataAll()
    Application.DisplayAlerts = False
    Sheets("SavepointData").Delete
    Application.DisplayAlerts = True
End Sub
