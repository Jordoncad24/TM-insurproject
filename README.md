
# TM-InsurProject

An exercise to create a Python web service using AWS services that interact with a database hosted on MongoDB Atlas.

This guide provides instructions on how to utilize the **TM-InsurProject** web application, which was built using Flask. The application comprises several components, and this documentation will guide you through each one.

## Table of Contents

- [Web Application](#web-application)
  - [Running the Application Locally](#running-the-application-locally)
  - [Main Page Features](#main-page-features)
  - [Endpoints](#endpoints)
- [MongoDB Database](#mongodb-database)
- [Cloud Deployment and Access](#cloud-deployment-and-access)
- [Testing](#testing)
- [Further Improvements](#further-improvements)

## Web Application

### Running the Application Locally

The main file for the application is `insuranceapi.py`. To run the web application locally, execute the following command in your terminal:

```bash
python insuranceapi.py
```

This will start the web application locally. Once running, you can access the main page of the web application through your web browser.

### Main Page Features

On the main page, you should see:

- **Search Bar:** Allows you to search for specific policy numbers.
- **Policy Numbers List:** Displays all the policy numbers stored in the MongoDB database.
- **"View All Policies" Button:** When clicked, it displays all documents in the database in JSON format.

**Note:** If the policies do not appear on the main page, you may need to run the `populatedb.py` file located in the `scripts` folder to populate the database.

### Endpoints

The application provides endpoints to view either specific policies or all policies in the database.

#### Retrieve a Specific Policy

To access a particular policy, use the following endpoint:

```
/api/policies/<policy_number>
```

You can also reach this endpoint by entering the desired policy number in the search bar on the main page.

#### Retrieve All Policies

To retrieve all policies in the database, use the following endpoint:

```
/api/policies
```

This endpoint returns a list of all policies in JSON format. Additionally, you can access it by clicking the **"View All Policies"** button on the web application.

## MongoDB Database

The MongoDB database is hosted on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and managed through AWS. Policies are stored in BSON format, which includes the essential details of each policy.

## Cloud Deployment and Access

The web application has been deployed to **AWS ECS Fargate** and is accessible via the public IP address provided by AWS.

### Deployment Steps

1. **Containerization:** The application was containerized using Docker.
2. **AWS ECR:** The Docker container was uploaded to the **AWS Elastic Container Registry (ECR)**.
3. **ECS Cluster:** AWS ECS accessed the container from ECR and deployed it to a cluster.
4. **Task Definition:** A task definition was created for the container before running it.

### Accessing the Deployed Application

1. Navigate to the ECS services page:
   [AWS ECS Services](https://eu-west-1.console.aws.amazon.com/ecs/v2/clusters/Insurance_TM/services?region=eu-west-1)

2. **Run the Task:**
   - Update the service by setting the desired number of tasks to `1`.
   - Start the service.

3. **Access the Application:**
   - Once the service is running, access the web application via `http://<publicIP>:5000`.
   - The Flask application listens on port `5000`.

**Note:** Replace `<publicIP>` with the actual public IP address provided by AWS.

## Testing

For testing, mocking was implemented to simulate a connection to the MongoDB database. Mocking was chosen to prevent interference with the real data stored in the database, avoiding potential issues during testing.

### Testing Coverage

The tests are designed to:

- Cover all aspects of the application code.
- Test various cases, including error handling scenarios.

### Running Tests

To execute the tests, navigate to the main project folder and run:

```bash
python tests/testinsuranceapi.py
```

## Further Improvements

Given more time, the following improvements could be made to enhance the application:

1. **Robust Testing and Test-Driven Development (TDD):**
   - Implement more comprehensive tests.
   - Adopt TDD practices to ensure tests are specifically designed for the application, ensuring accurate pass and fail conditions.
   - Fully integrate and implement existing tests.

2. **CI/CD Pipeline:**
   - Establish a Continuous Integration/Continuous Deployment (CI/CD) pipeline.
   - Automate the deployment process to enable faster updates and immediate reflection of changes in the application.

3. **Enhanced Security:**
   - Secure the connection to the MongoDB database by using environment variables for connection strings.
   - Ensure that database access is restricted to authorized users only.

4. **Improved User Interface (UI):**
   - Enhance the UI for better clarity and professionalism.
   - Improve navigation and overall user experience.

5. **Scalability and Performance Optimization:**
   - Optimize the application for better performance and scalability.
   - Implement caching strategies and load balancing as needed.

6. **Comprehensive Documentation:**
   - Expand the documentation to include more detailed instructions, troubleshooting tips, and feature explanations.

By addressing these areas, the application can achieve higher reliability, security, and user satisfaction.
