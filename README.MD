# WhatsApp-Sender

Automation of WhatsApp message sending with PyWhatKit

## Overview 🌐

WhatsApp-Sender is a desktop application designed to automate the sending of WhatsApp messages using Python. It leverages the PyWhatKit library for message automation and the Flet library for its graphical user interface. This tool allows users to send messages automatically from an XLSX database, utilizing PyWhatKit's web navigation capabilities.

## Requirements 🛠️

- Python 3.6 or higher
- PyWhatKit
- Flet

## Getting Started 🚀

1. Clone the WhatsApp-Sender repository to your local machine.
2. Install the necessary dependencies by running 
```bash 
pip install -r requirements.txt
```
3. Run the application with 
```bash 
`python app.py
````

## Usage 💡

Before using WhatsApp-Sender, it's crucial to log in to WhatsApp Web. This step is essential for the application to function correctly.

1. **Load the XLSX database**: Use the graphical user interface to load your XLSX database.
2. **Select the templates**: Choose the template for the message and modify its variables if necessary. The variables are enclosed in curly braces (e.g., `{nombre}`, `{empresa}`, `{direccion}`) and will be replaced by each row's data from the XLSX database.
3. **Send the messages**: The application will automatically send the messages to the recipients in the database.
4. **Preview**: The application provides a preview feature that renders the first record of the database with the selected template.


## Features 🌟

- **Instant message sending**: Messages are sent instantly without scheduling.
- **Template management**: Allows saving, updating, and deleting templates.
- **Variable substitution**: Variables in templates are replaced with data from the XLSX database.
- **Preview functionality**: Renders the first record of the database with the selected template for preview.

## Screenshots 📸
Include screenshots of the application here to provide a visual guide on how to use it.
![img.png](src%2Fscreenshots%2Fimg.png)

![img_1.png](src%2Fscreenshots%2Fimg_1.png)

![img_2.png](src%2Fscreenshots%2Fimg_2.png)

![img_3.png](src%2Fscreenshots%2Fimg_3.png)

## Packaging the Application 📦

To package the application for distribution, follow these steps:

1. Open a command prompt or terminal window.
2. Navigate to the root directory of your project.
3. Run the following command:

```bash 
flet pack app.py --icon src\assets\logo.png --add-data "src\sample.xlsx;."
```


This command will create a distributable package of your application, including the `sample.xlsx` file in the root directory of the package.

### Troubleshooting

If the `--add-data` option does not work as expected and the `sample.xlsx` file is not included in the `dist` folder, you can manually copy the file to the `dist` folder. Here's how to do it on Windows:

1. Open File Explorer.
2. Navigate to the `src` directory within your project.
3. Find the `sample.xlsx` file.
4. Copy the file.
5. Navigate to the `dist` directory within your project.
6. Paste the `sample.xlsx` file into the `dist` directory.

By following these steps, you ensure that the `sample.xlsx` file is included in the distributable package of your application.


flet pack main.py --icon src\assets\logo.png --add-data "src\sample.xlsx;."

## Contributing  🤝

Contributions are welcome. Please follow the contribution guidelines.

## License 📄

WhatsApp-Sender is licensed under the MIT License. See the `LICENSE` file for more details.
