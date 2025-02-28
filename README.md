# SRM LMS Automation Tool

## Overview
The **SRM LMS Automation Tool** is designed to streamline and enhance the user experience of the **SRM Learning Management System (LMS)** by automating repetitive tasks such as assignment submissions. This tool aims to reduce manual effort, improve efficiency, and provide seamless interaction with SRM LMS.

## Features
- **Automated Login**: Secure and quick access to the LMS without repeated manual authentication.

- **Assignment Submission**:
  - **Audio visual learning materials**
  - **Textual Learning Materials**
  - **Additional Reference Links**
  - **Glossary**
  - **FAQs**

    
## Benefits
- **Saves Time**: Eliminates the need for manual interaction with repetitive LMS tasks.
- **Reduces Errors**: Minimizes the chances of missing deadlines or incorrect 


## Installation
- Install Dependencies
  ```shell
    pip install requests
- Install Dependencies
    ```shell
    python main.py

## Code Example
```shell
LMS = srm_lms_dashboard.LMS("US1234", "passWORD")
LMS.Activity(LMS.PYTHON_PROGRAMING).CompleteAllWeeks()
