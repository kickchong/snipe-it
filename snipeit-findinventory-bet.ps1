#$uri = "https://develop.snipeitapp.com/api/v1/hardware"

$headers = @{
    'accept' = 'application/json'
    'authorization' = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImVmMGVhY2Y4MjAyYzgwZWI2M2JkNmIwZDc0OGYwY2FkYzU2Y2ZlMzgyNzY4ODY0N2EwNmU4ZTBlNmYwZDgwODNjZmMyMzI2YWYyYTZlMTFkIn0.eyJhdWQiOiIxIiwianRpIjoiZWYwZWFjZjgyMDJjODBlYjYzYmQ2YjBkNzQ4ZjBjYWRjNTZjZmUzODI3Njg4NjQ3YTA2ZThlMGU2ZjBkODA4M2NmYzIzMjZhZjJhNmUxMWQiLCJpYXQiOjE0OTMzMzI2MjgsIm5iZiI6MTQ5MzMzMjYyOCwiZXhwIjoxODA4ODY1NDI4LCJzdWIiOiIyIiwic2NvcGVzIjpbXX0.NU7ZRIt-d4b0o8uv9ipo1vSWcg1svbmPp47kHErafm9iuK4FjygKd2_4Hp73HKAmjiYcEn3r39pwNh2t9BMFnTXv0KeDGC8zfZ9z7OJN_a59LPoarWBFzCsYETyAm-CeeFnfdj9Cr0ZeGOnnaPuWPYxicwKFeqJI4Hn8nCymcamDGE0u4WOO95ihGOAen4_fqpj-kkBDsvsGhB-cQxeuKdlbvO1yOsKmgQv-kQuxiFMn1zgU7P02mC6XXrbw6jTm7JOaBSbvqSwNtsrSKZkim1jxLsQ4dm36lFmeMkU6hZvNSUnxg8JwbmoxQ_3tZlG3IJh3Sc9ZUi-AEAQ4bbGzi_xNS9fenIdzLDaSiv_esYyNOYXqOuSBk8Yr-720N9OcVjGLnPrV3RtmPisV1aLFgKWLImtlyQgUq3d5LA3QXz8Q_8isvO9Am1u8ri2plbHGJLJ6GRW_mYcBEYMwUozaeXTUe_FUSSO8gpGtO9Hpa5SbERY272_tojyVXpYPaPdUYYmS9CP332jBNESPT8wGwpOM-iddeVo_n82w3dHmDEdp1Brbs3_vKk0AcgvDLsAbd4dZZO-UqddVx6SDb3HLw1Pmw1wGGYHA6w8wWQAiS9kg2xMcz5i75HOULaN3miqYvcPCvHpI2CBfuvdplI8QNm_XzFPmoQRu_5kR8knzla4'
    'content-type' = 'application/json'
}

$maca = "b8-08-cf-30-dd-b8"

for($x=1380;$x-gt1; $x=$x-1) {
    $uri = 'https://develop.snipeitapp.com/api/v1/hardware/'+$x
    $cf = (Invoke-RestMethod -Uri $uri -Method Get -Headers $headers).custom_fields."MAC Address".value 
    echo $cf
    if ($cf -eq $maca) {
        (Invoke-RestMethod -Uri $uri -Method Get -Headers $headers).id
    }
    else {
        echo "false"
    }
}
#$cf = (Invoke-RestMethod -Uri $uri -Method Get -Headers $headers).custom_fields."MAC Address".value 

#$cf = (Invoke-RestMethod -Uri $uri -Method Get -Headers $headers).rows.custom_fields."MAC Address".value 
#echo $uri 


$a = Invoke-RestMethod -Uri $uri -Method Get -Headers $headers | ConvertTo-Json 

#echo $a > .\a.txt
#echo $a

$b = Get-Content .\a.txt | Where-Object { $_.Contains($maca) }

if ($cf -eq $null) {
    (Invoke-RestMethod -Uri $uri -Method Get -Headers $headers).rows.id 
}

if ($b -eq $null) {
    echo "false"
} 
else {
    echo "true"
}

$c = $a | Select-String -Pattern $maca
#echo $c

if ($c -eq $null) {
    echo "false"
}
else {
    echo "true"
}