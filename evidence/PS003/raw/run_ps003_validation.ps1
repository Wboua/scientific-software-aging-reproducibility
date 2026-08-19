# PS-003-ENV-01 - Reinforced JVM Validation

$ErrorActionPreference = "Continue"

$jdks = [ordered]@{
    "17" = "C:\Program Files\Eclipse Adoptium\jdk-17.0.20.8-hotspot\bin\java.exe"
    "21" = "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot\bin\java.exe"
    "25" = "C:\Program Files\Eclipse Adoptium\jdk-25.0.4.7-hotspot\bin\java.exe"
}

$benchmarkRegex = "org\.scijava\.ops\.benchmarks\.Benchmarks\.(noOps|sjOps|ijOps)"

$warmupIterations = 5
$warmupTime = "5s"
$measurementIterations = 10
$measurementTime = "5s"
$forks = 3
$independentRuns = 3

$outDir = Join-Path (Get-Location) "ps003-validation"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# Verify JDK installations
$metadata = @()

foreach ($version in $jdks.Keys) {

    $java = $jdks[$version]

    if (-not (Test-Path $java)) {
        throw "Java executable not found for JDK ${version}: ${java}"
    }

    Write-Host "Checking JDK $version"
    & $java -version

   $metadata += [pscustomobject]@{
    jdk  = $version
    java = $java
    }
}

$metadata |
    ConvertTo-Json -Depth 4 |
    Out-File (Join-Path $outDir "environment.json") -Encoding utf8


# Run experiments
for ($run = 1; $run -le $independentRuns; $run++) {

    foreach ($version in $jdks.Keys) {

        $java = $jdks[$version]

        $json = Join-Path $outDir ("jdk{0}-run{1}.json" -f $version, $run)
        $txt  = Join-Path $outDir ("jdk{0}-run{1}.txt" -f $version, $run)

        Write-Host ""
        Write-Host "===================================================="
        Write-Host "PS-003 - JDK $version - Independent run $run"
        Write-Host "===================================================="


$oldErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"

        & $java `
            -cp "target\classes;target\dependency\*" `
            --add-opens=java.base/java.io=ALL-UNNAMED `
            org.openjdk.jmh.Main `
            $benchmarkRegex `
            -wi $warmupIterations `
            -w $warmupTime `
            -i $measurementIterations `
            -r $measurementTime `
            -f $forks `
            -rf json `
            -rff $json `
            2>&1 | Tee-Object -FilePath $txt

        if ($LASTEXITCODE -ne 0) {
            throw "JMH failed for JDK ${version}, run ${run}"
        }
    }
}



$ErrorActionPreference = $oldErrorActionPreference

Write-Host ""
Write-Host "===================================================="
Write-Host "PS-003 VALIDATION COMPLETED"
Write-Host "===================================================="
Write-Host ""
Write-Host "Results saved in:"
Write-Host $outDir