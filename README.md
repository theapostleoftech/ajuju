# Ajuju

![Ajuju Logo](theme/static/logo/ajuju_logo.png)



## Introduction

Ajuju is an interactive quiz application that allows users who are teachers called creators to create quizzes for
students who are Whizzers to take.
- **Deployed Site:** [http://ajuju.the10x.tech](http://ajuju.the10x.tech)

## Features

- On-demand package delivery
- Real-time tracking
- Flexible pricing models
- User-friendly interface for both customers and couriers
- Integration with Google Maps for efficient routing
- Secure payment processing

## Technologies Used

- Backend: Django (Python web framework)
- Frontend: HTML, CSS, JavaScript
- CSS Framework: Tailwind CSS
- Database: PostgresSQL
- Version Control: Git
- Cloud Platform: AWS

## Installation

To set up Ajuju locally, follow these steps:

1. Clone the repository:
   git clone https://github.com/theapostleoftech/ajuju.git
   cd ajuju

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate # On Windows, use venv\Scripts\activate

3. Install the required dependencies:
   pip install -r requirements.txt

4. Set up environment variables:
   Create a `.env` file in the root directory and add necessary environment variables (database credentials, API keys,
   etc.)

5. Run database migrations:
   python manage.py migrate

6. Start the development server:
   python manage.py runserver

7. Visit `http://localhost:8000` in your web browser to access the application.

## Usage

1. **For Teachers(Creators):**

- Create an account or log in
- Create Subject
- Create Quiz
- Track Whizzers in realtime as they take the quiz

2. **For Students(Whizzers):**

- Sign up as a whizzer
- Start taking quizzes

## Contributing

We welcome contributions to Ajuju! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to our coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

Chukwunonso Nwankpa - [LinkedIn](https://www.linkedin.com/in/chukwunonsonwankpa/) - chukwunonsonwankpa@gmail.com

Project Link: [https://github.com/theapostleoftech/ajuju](https://github.com/theapostleoftech/ajuju)
