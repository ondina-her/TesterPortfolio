## Project Scope and Objectives
The objective of this project is to verify that the QR scanner web application works correctly across different environments and under varied scanning conditions. The focus is on ensuring functional accuracy, reliable API behavior, and consistent UI performance.

### Functional testing 
covers correct scanning of valid QR codes, handling of invalid or empty QR inputs, and validation of the user interface elements.

### API testing 
includes CRUD operations for Items and Scans, validation of error handling (422 and 404 responses), and negative cases for invalid inputs.

### Automation 
is achieved using Pytest with Selenium for functional and UI tests, and Postman for API tests. JIRA is used for task tracking and alignment with sprint objectives.

### The testing environment 
consists of a camera-based QR scanner running in a QA environment with a local FastAPI server.

### The tools 
used in this project are Postman, Pytest with Selenium, and JIRA.

#### Test Cases

##### STQC‑6 Valid QR test
###### Objective: Verify that a valid QR code is correctly scanned and decoded.

Steps:

- Open app.

- Click scanner button.

- Present valid QR code.

- Verify decoded text appears in result box.

- Expected Result: Result box shows QR text.

##### STQC‑7 Invalid QR test
###### Objective: Verify that invalid QR codes are rejected.

Steps:

- Open app.

- Click scanner button.

- Present invalid QR code.

- Verify result box stays empty or shows “No result.”

- Expected Result: No decoded text appears.


##### STQC‑8 Empty QR test
###### Objective: Verify that blank input does not produce results.

Steps:

- Open app.

- Click scanner button.

- Show blank sheet or cover camera.

- Verify result box stays empty.

- Expected Result: Result box remains empty.



##### STQC‑9 UI validation
###### Objective: Verify that all UI elements are present and functional.

Steps:

- Open app.

- Check page title.

- Verify scanner button, video feed, result placeholders, status box.

- Expected Result: All elements exist and are displayed.



##### API‑1 Create Item
###### Objective: Verify that a new Item can be created.

Steps:

- Send POST /items/ with JSON body.

- Verify response status 201.

- Expected Result: Item created with id, name, description.


##### API‑2 Create Scan
###### Objective: Verify that a Scan links correctly to an Item.

Steps:

- Send POST /scans/ with JSON body.

- Verify response status 201.

- Expected Result: Scan created with item_id and embedded Item.

##### API‑3 Negative – Empty Scan source
###### Objective: Verify that empty source is rejected.

Steps:

- Send POST /scans/ with "source": "".

- Expected Result: Status 422 Unprocessable Entity.


##### API‑4 Negative – Invalid Item ID
###### Objective: Verify that non‑existent Item ID returns error.

Steps:

- Send GET /items/999.

- Expected Result: Status 404 Not Found.