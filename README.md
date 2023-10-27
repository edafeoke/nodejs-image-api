# Server

This API allows users to upload images, store image information in a MongoDB database, and retrieve image data, including location information and public URLs.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Features

- Upload images and associated information (date, location, public URL).
- Store image data in a MongoDB database.
- Retrieve image information and display it as a list.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Node.js and npm installed.
- MongoDB installed and running (Update the connection string accordingly).
- Basic knowledge of using Postman or a similar tool to interact with the API.

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:Asifor/react-native-private-challenge.git
   ```

2. Change into the project directory:

   ```bash
   cd server
   ```

3. Install dependencies:

   ```bash
   npm install
   ```

   or

   ```bash
   yarn
   ```

4. Create an `uploads` directory in the project root to store uploaded images.

5. Update the MongoDB connection string in `index.js` to point to your MongoDB server.

6. Start the server:

   ```bash
   npm start
   ```

or

```bash
   yarn start
   ```

## Usage

To upload images and retrieve image data, you can use a tool like Postman or make HTTP requests to the API endpoints.

## API Endpoints

- **POST /upload**

  Upload an image along with information. The request should contain an image file (`image`) and a JSON body with additional information.

  Example request body:

  ```json
  {
    "date": "2023-10-31",
    "latitude": "123.456",
    "longitude": "78.910",
    "publicUrl": "https://example.com/image.png"
  }
  ```

- **GET /images**

  Retrieve a list of uploaded image information.

  Example response:

  ```json
  [
    {
      "_id": "609c474a39475e193062a4bd",
      "filename": "image-1635623664566.png",
      "date": "2023-10-31",
      "latitude": "123.456",
      "longitude": "78.910",
      "publicUrl": "https://example.com/image.png",
      "__v": 0
    }
  ]
  ```