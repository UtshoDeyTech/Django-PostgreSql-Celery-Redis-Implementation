# Wait for PostgreSQL to be ready
$maxRetries = 30
$retryCount = 0
$retryIntervalSeconds = 2

Write-Host "Waiting for PostgreSQL to be ready..."
while ($retryCount -lt $maxRetries) {
    try {
        $env:PGPASSWORD = $env:DATABASE_PASSWORD
        $checkConnection = & pg_isready -h $env:DATABASE_HOST -p $env:DATABASE_PORT -U $env:DATABASE_USER
        
        if ($checkConnection -match "accepting connections") {
            Write-Host "PostgreSQL is ready!"
            break
        }
    }
    catch {
        Write-Host "PostgreSQL not ready yet. Waiting..."
    }
    
    $retryCount++
    Start-Sleep -Seconds $retryIntervalSeconds
}

if ($retryCount -ge $maxRetries) {
    Write-Host "Error: Could not connect to PostgreSQL after multiple attempts."
    exit 1
}

# Make migrations first to ensure all models are properly registered
Write-Host "Creating migrations..."
python manage.py makemigrations

# Run migrations
Write-Host "Running migrations..."
python manage.py migrate

# Create superuser if specified in environment variables
if ($env:DJANGO_SUPERUSER_USERNAME -and $env:DJANGO_SUPERUSER_EMAIL -and $env:DJANGO_SUPERUSER_PASSWORD) {
    Write-Host "Creating superuser..."
    python manage.py createsuperuser --noinput
}

# Execute the command passed as arguments
Write-Host "Starting application with command: $args"
& $args[0] $args[1..($args.Length-1)]