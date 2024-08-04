# BankingLLM with Graph DB


## Getting Started

1. Clone the repository:
    ```
    git clone git@github.com:piyushcse29/BankingLLM.git
    ```

2. Navigate to the project directory:
    ```
    cd BankingLLM
    ```

3. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

## Running the Docker File

1. Build the Docker image. 
    ```
    docker build -t bankingllm .
    ```

2. Run the Docker container.
    ```
    docker run -p 7860:7860 bankingllm
    ```

The application should now be running at `http://localhost:7860`.