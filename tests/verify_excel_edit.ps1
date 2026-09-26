# Verify edits on a disposable copy, leaving the reusable example unchanged.
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
$qa = Join-Path $repo '.qa'
New-Item -ItemType Directory -Force -Path $qa | Out-Null
$source = Join-Path $repo 'examples\purchase_request.xlsx'
$destination = Join-Path $qa 'excel_edited.xlsx'
Copy-Item -LiteralPath $source -Destination $destination
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    $book = $excel.Workbooks.Open($destination)
    $sheet = $book.Worksheets.Item('Process')
    $sheet.Cells.Item(2,3).Value2 = 'Edited in Excel: identify the required supplies'
    $sheet.Cells.Item(13,6).NumberFormat = '@'
    $sheet.Cells.Item(13,6).Value2 = '013'
    $sheet.Cells.Item(14,1).NumberFormat = '@'
    $sheet.Cells.Item(14,6).NumberFormat = '@'
    $sheet.Cells.Item(14,1).Value2 = '013'
    $sheet.Cells.Item(14,2).Value2 = 'Close'
    $sheet.Cells.Item(14,3).Value2 = 'File the completed request'
    $sheet.Cells.Item(14,4).Value2 = 'Purchasing'
    $sheet.Cells.Item(14,5).Value2 = 0.5
    $excel.CalculateFullRebuild()
    $book.Save()
    $book.Close($false)
    Write-Output 'Excel edit/add/save completed on .qa/excel_edited.xlsx'
} finally {
    $excel.Quit()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel)
}
