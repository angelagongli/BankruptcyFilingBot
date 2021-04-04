Sub ClearTransactionData(TransactionDataSheetName)
    Sheets(TransactionDataSheetName).Cells.Clear
End Sub

Sub ClearSavepointData()
    Sheets("SavepointData").Cells.Clear
End Sub

Sub ClearSavepointDataAll()
    Sheets("SavepointData").Delete
End Sub
