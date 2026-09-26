# Developer-only fixture creation; Excel is not a generator dependency.
$ErrorActionPreference = 'Stop'
$fixtureDir = Join-Path $PSScriptRoot 'fixtures'
New-Item -ItemType Directory -Force -Path $fixtureDir | Out-Null
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    $book = $excel.Workbooks.Add()
    $sheet = $book.Worksheets.Item(1)
    $sheet.Name = 'Process'
    $headers = @('task_id','section','task','department','annual_frequency','next_task_id')
    for ($i=0; $i -lt 6; $i++) { $sheet.Cells.Item(1,$i+1).Value2 = $headers[$i] }
    $sheet.Cells.Item(2,1).Formula = '=TEXT(1,"000")'
    $sheet.Cells.Item(2,2).Formula = '="Area"'
    $sheet.Cells.Item(2,3).Formula = '="Formula task"'
    $sheet.Cells.Item(2,4).Formula = '="Department"'
    $sheet.Cells.Item(2,5).Formula = '=1/2'
    $sheet.Cells.Item(2,6).Value2 = 'PR-01'
    $sheet.Cells.Item(3,1).Value2 = 'PR-01'
    $sheet.Cells.Item(3,2).Value2 = 'Area'
    $sheet.Cells.Item(3,3).Value2 = 'Finish'
    $sheet.Cells.Item(3,4).Value2 = 'Department'
    $excel.CalculateFullRebuild()
    $book.SaveAs((Join-Path $fixtureDir 'excel_saved_formulas.xlsx'),51)
    Write-Output ('Fixture saved with Excel ' + $excel.Version)
    $book.Close($false)
} finally {
    $excel.Quit()
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($excel)
}
