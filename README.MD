# WhatsApp-Sender

Automation of WhatsApp message sending with PyWhatKit

## Overview 📖

WhatsApp-Sender is a desktop application designed to automate the sending of WhatsApp messages using Python. It leverages the PyWhatKit library for message automation and the Flet library for its graphical user interface. This tool allows users to send messages automatically from an XLSX database, utilizing PyWhatKit's web navigation capabilities.

## Requirements 📖

- Python 3.6 or higher
- PyWhatKit
- Flet

## Getting Started 🚀

1. Clone the WhatsApp-Sender repository to your local machine.
2. Install the necessary dependencies by running `pip install -r requirements.txt`.
3. Run the application with `python app.py`.

## Usage 🛠️

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


## Contributing  🤝

Contributions are welcome. Please follow the contribution guidelines.

## License

WhatsApp-Sender is licensed under the MIT License. See the `LICENSE` file for more details.
