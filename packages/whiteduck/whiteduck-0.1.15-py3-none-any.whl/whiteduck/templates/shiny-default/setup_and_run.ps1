param(
    [switch]$useDocker = $false
)

# Step 1: Check if the script should run the Docker commands
if ($useDocker) {
    Write-Host "Running Docker commands..."

    # Build the Docker image
    docker build -t whiteduck .

    # Run the Docker container, remove it after execution, and map port 8000
    docker run --rm -p 8000:8000 whiteduck
}
else {# Step 1: Check if Poetry and conda are installed
    # $condaPath = (Get-Command conda -ErrorAction SilentlyContinue).Path
    # if (-not $condaPath) {
    #     Write-Host "Conda is not installed. Latest version of miniconda is getting installed"
    #     curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
    #     Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
    #     del miniconda.exe
    #     Write-Host "Conda was installed. Please restart the terminal for changes to take effect."
    #     exit
    # }
    # else {
    #     Write-Host "Conda is already installed."
    # }

    # Write-Host "Prepare the terminal for conda and poetry..."
    # conda activate base
    # conda init powershell

    $poetryPath = (Get-Command poetry -ErrorAction SilentlyContinue).Path
    if (-not $poetryPath) {
        Write-Host "Poetry is not installed. Poetry getting installed..."
        pip install poetry
    }
    else {
        Write-Host "Poetry is already installed."
    }


    # # Step 2: Check if the Conda environment already exists
    # $envName = "whiteduck"
    # $envExists = conda info --envs | Select-String -Pattern $envName

    # if (-not $envExists) {
    #     Write-Host "Conda environment '$envName' does not exist. Creating the environment..."
    #     conda create -n $envName python=3.10.14 -y
    # }
    # else {
    #     Write-Host "Conda environment '$envName' already exists."
    # }

    # # Step 3: Activate the Conda environment
    # Write-Host "Activating Conda environment '$envName'..."
    # conda activate $envName

    # Step 4: Install project dependencies using Poetry
    Write-Host "Installing project dependencies using Poetry..."
    poetry install --no-root

    # Step 5: Start the app
    Write-Host "Starting App..."
    poetry run shiny run .\app.py

    # Step 6: Keep the script open indefinitely
    Write-Host "Press Enter to exit the script..."
    Read-Host
}