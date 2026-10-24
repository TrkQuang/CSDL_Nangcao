param(
    [int]$Clients = 10,
    [int]$TransactionsPerClient = 100,
    [int]$Threads = 2,
    [string]$Database = "detai17_db",
    [string]$DbHost = "localhost",
    [int]$Port = 5432,
    [string]$User = "postgres",
    [string]$Password = "",
    [string]$PgbenchPath = "" # Cho phep tu truyen duong dan neu cai o vi tri tuy bien
)

$ErrorActionPreference = "Stop"

# ==============================================================================
# THUAT TOAN TIM PGBENCH THONG MINH (TU DONG THICH UNG VOI MOI MAY):
# 1. Neu truyen tham so -PgbenchPath thi dung ngay.
# 2. Kiem tra bien moi truong PATH (Get-Command pgbench) -> Chay duoc ca tren Windows, Linux, macOS.
# 3. Kiem tra thu muc Program Files dong ($env:ProgramFiles, khong hardcode o C).
# 4. Quet tim tu dong trong cac thu muc cai dat pho bien tren moi o dia.
# ==============================================================================

$pgbench = $null

# Buoc 1: Kiem tra tham so nguoi dung truyen vao
if ($PgbenchPath -and (Test-Path $PgbenchPath)) {
    $pgbench = $PgbenchPath
}

# Buoc 2: Kiem tra bien moi truong he thong (PATH)
if (-not $pgbench) {
    $cmd = Get-Command pgbench -ErrorAction SilentlyContinue
    if ($cmd) {
        $pgbench = $cmd.Source
    }
}

# Buoc 3: Tu dong quet thu muc Program Files theo cac phien ban PostgreSQL (14 den 19)
if (-not $pgbench) {
    $searchDirs = @(
        "$env:ProgramFiles\PostgreSQL",
        "${env:ProgramFiles(x86)}\PostgreSQL",
        "D:\Program Files\PostgreSQL",
        "D:\PostgreSQL",
        "C:\PostgreSQL"
    )

    foreach ($dir in $searchDirs) {
        if (Test-Path $dir) {
            # Tim file pgbench.exe trong cac subfolder bin
            $found = Get-ChildItem -Path $dir -Filter "pgbench.exe" -Recurse -Depth 3 -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $pgbench = $found.FullName
                break
            }
        }
    }
}

# Neu van khong tim thay thi huong dan chi tiet cach xu ly
if (-not $pgbench) {
    Write-Error @"
[KHONG TIM THAY PGBENCH.EXE TRÊN MÁY NÀY!]
Cac cach de khac phuc nhanh:
1. Truyen truc tiep duong dan khi chay script:
   .\run_pgbench.ps1 -PgbenchPath "D:\duong_dan_den\bin\pgbench.exe"
2. Hoac them thu muc bin cua PostgreSQL vao bien moi truong PATH cua Windows.
"@
    exit 1
}

Write-Host ">>> Da tim thay pgbench tai: $pgbench" -ForegroundColor Cyan
Write-Host ">>> Dang chay thu tai: $Clients ket noi dong thoi ($TransactionsPerClient transactions/client)..." -ForegroundColor Yellow

# Thiet lap mat khau linh hoat (uu tien param truyen vao, sau do den env, mac dinh la postgres)
if ($Password) {
    $env:PGPASSWORD = $Password
} elseif (-not $env:PGPASSWORD) {
    $env:PGPASSWORD = "postgres"
}

$scriptPath = Join-Path $PSScriptRoot "transactions\pgbench\add_friend.sql"

& $pgbench -n -h $DbHost -p $Port -U $User -c $Clients -j $Threads -t $TransactionsPerClient -f $scriptPath $Database

if ($LASTEXITCODE -ne 0) {
    throw "pgbench failed with exit code $LASTEXITCODE. Check connection and script output."
}

Write-Host "`n>>> THU TAI PGBENCH HOAN TAT THANH CONG! <<<" -ForegroundColor Green
