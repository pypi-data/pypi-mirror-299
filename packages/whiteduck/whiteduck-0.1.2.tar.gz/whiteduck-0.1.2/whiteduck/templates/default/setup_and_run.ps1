# Step 1: Check if Poetry and conda are installed
$poetryPath = (Get-Command poetry -ErrorAction SilentlyContinue).Path
if (-not $poetryPath) {
    Write-Host "Poetry is not installed. Poetry getting installed..."
    curl -sSL https://install.python-poetry.org | python3 -
}
else {
    Write-Host "Poetry is already installed."
}

$condaPath = (Get-Command conda -ErrorAction SilentlyContinue).Path
if (-not $condaPath) {
    Write-Host "Conda is not installed. Latest version of miniconda is getting installed"
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
    Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
    del miniconda.exe
}
else {
    Write-Host "Conda is already installed."
}

# Step 2: Check if the Conda environment already exists
$envName = "whiteduck"
$envExists = conda info --envs | Select-String -Pattern $envName

if (-not $envExists) {
    Write-Host "Conda environment '$envName' does not exist. Creating the environment..."
    conda create -n $envName python=3.10.14 -y
}
else {
    Write-Host "Conda environment '$envName' already exists."
}

# Step 3: Activate the Conda environment
Write-Host "Activating Conda environment '$envName'..."
conda activate $envName

# Step 4: Install project dependencies using Poetry
Write-Host "Installing project dependencies using Poetry..."
poetry install --no-root

# Step 5: Start the app
Write-Host "Starting App..."
shiny run .\app.py

# Step 6: Keep the script open indefinitely
Write-Host "Press Enter to exit the script..."
Read-Host
