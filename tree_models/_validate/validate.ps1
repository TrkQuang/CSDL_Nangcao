param(
    [string]$DatabaseName = 'de17_tv2_validation',
    [switch]$ResetDatabase
)

$ErrorActionPreference = 'Stop'
$psql = 'C:\Program Files\PostgreSQL\18\bin\psql.exe'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$out = Join-Path $PSScriptRoot 'validation_result.txt'

if (-not (Test-Path $psql)) {
    throw "Không tìm thấy psql tại '$psql'. Hãy cập nhật đường dẫn trong script."
}
if ($DatabaseName -notmatch '^de17_tv2_validation(?:_[A-Za-z0-9_]+)?$') {
    throw "Chỉ được dùng database kiểm thử có tên de17_tv2_validation hoặc tiền tố đó kèm hậu tố."
}

function Invoke-Psql {
    param([string[]]$Arguments)

    & $psql -X -U postgres -h localhost -w @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "psql thất bại (exit code $LASTEXITCODE). Kiểm tra kết nối và thông tin đăng nhập PostgreSQL."
    }
}

$exists = [string](& $psql -X -U postgres -h localhost -w -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$DatabaseName'")
if ($LASTEXITCODE -ne 0) {
    throw "Không kết nối được PostgreSQL. Hãy cấu hình pgpass.conf hoặc biến môi trường PGPASSWORD bên ngoài repo."
}

if ($exists.Trim() -eq '1') {
    if (-not $ResetDatabase) {
        throw "Database '$DatabaseName' đã tồn tại. Không có dữ liệu nào bị xóa. Dùng -ResetDatabase chỉ khi chắc chắn muốn tạo lại database kiểm thử này."
    }
    Invoke-Psql @('-d', 'postgres', '-c', "DROP DATABASE $DatabaseName")
}

Invoke-Psql @('-d', 'postgres', '-c', "CREATE DATABASE $DatabaseName")
Invoke-Psql @('-d', $DatabaseName, '-v', 'ON_ERROR_STOP=1', '-f', (Join-Path $repo 'database\schema.sql'))
Invoke-Psql @('-d', $DatabaseName, '-v', 'ON_ERROR_STOP=1', '-f', (Join-Path $repo 'database\seed_test.sql'))

foreach ($model in 'adjacency_list', 'closure_table', 'nested_set', 'path_enumeration') {
    Invoke-Psql @('-d', $DatabaseName, '-v', 'ON_ERROR_STOP=1', '-f', (Join-Path $repo "tree_models\$model\schema.sql"))
}

$results = @("=== VALIDATION TV2 tree_models  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===")
foreach ($model in 'adjacency_list', 'closure_table', 'nested_set', 'path_enumeration') {
    Invoke-Psql @('-d', $DatabaseName, '-v', 'ON_ERROR_STOP=1', '-f', (Join-Path $repo "tree_models\$model\queries_q1_q10.sql"))
    Invoke-Psql @('-d', $DatabaseName, '-v', 'ON_ERROR_STOP=1', '-f', (Join-Path $repo "tree_models\$model\crud.sql"))
    $results += "$model  queries=OK  crud=OK"
    Write-Host "$model queries=OK crud=OK"
}

$results += "Database retained for inspection: $DatabaseName"
$results | Set-Content $out -Encoding utf8
Write-Host "Validation complete. Database retained: $DatabaseName"
Write-Host "Report: $out"
