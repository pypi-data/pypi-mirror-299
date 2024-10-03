# Bilkent Trafficæß

![Bilkent Traffic Gif](./assets/example_gif.gif)
![YouTube](https://www.youtube.com/watch?v=iOVfomqV2Dw)

`bilkent_traffic` is a command-line tool designed to simplify reporting traffic violations at Bilkent University by sending an email through Bilkent's email system. The script allows users to select default or custom templates for reporting.

## Features
- Choose between English and Turkish templates.
- Report car model, color, location, and reason for the traffic report.
- Customize email templates for different reports.
- Automatically sends email to `traffic@bilkent.edu.tr` using Bilkent email credentials.

## Installation

### Using `pip`

- To install the latest version of `bilkent_traffic`, use `pip`:

```bash
pip install bilkent_traffic
```

### Requirements

- Python 3.x

- pyfiglet and pillow modules are automatically installed.

## Usage

- After installing, you can use the bilkent_traffic command directly from your terminal:

```bash
bilkent_traffic
```

### Command-line Steps:

1. Enter your Bilkent email address.
2. Enter your email password.
3. Enter the email subject.
4. Choose between a default template or a custom one.
5. If using the default template, you'll be asked to provide:
    - Car model
    - Car color
    - Location of the incident
    - Reason for the report
    - Time when the incident occurred
6. If using a custom template, provide the path to your custom template file.

### Development

- To contribute to the project or run it locally:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bilkent_traffic.git
```

2. Navigate to the project directory:

```bash
cd bilkent_traffic
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## License
- This project is licensed under the MIT License - see the LICENSE file for details.

