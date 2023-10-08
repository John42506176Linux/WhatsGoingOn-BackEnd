# WhatsGoingOn App Backend

This is the backend for an app that allows people to search for current cool events in their area. The backend is built using Python and FastAPI, and provides an API for the frontend to interact with.

## Getting Started

To get started with the backend, you will need to have Python and pip installed on your system. You can install them by following the instructions on the [official Python website](https://www.python.org/downloads/).

Once you have Python and pip installed, you can install the required dependencies by running the following command in the project directory:
```
pip install -r requirements.txt
```
This will install all the required dependencies listed in the `requirements.txt` file.

To start the backend server, you can run the following command:
```
python3 -m uvicorn main:app --reload --port 80002
```
This will start the server on port 8002 by default. You can then make requests to the API endpoints using a tool like curl or a web browser.

## API Endpoints

The backend provides the following API endpoints:

- **POST /api/search**
  - This endpoint allows users to search for events by location. The request body should be in JSON format and have the following structure:
  ```json
  {
    "location": "..."
  }
  ```

## Contributing

If you would like to contribute to the project, you can fork the repository and submit a pull request with your changes. Please make sure to follow the existing code style and include tests for any new functionality.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
```

You can copy and paste the above markdown content into your `readme.md` file.