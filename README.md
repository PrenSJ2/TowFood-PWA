
# Django-Tailwind Food Inventory System (TowFood)

This project is my final project for the School of Computing at the University of Buckingham.



## Environment Setup

To run this project, you will need to create a python virtual environment inside your project directory:

```bash
python -m venv env
```

start the environment:

```bash
source env/bin/activate
```

next install all project requirements:

```bash
pip install -r requirements.txt
```


## Install dependencies

navigate to the theme/static_src
```bash
cd theme/static_src
```

```bash
npm install
```

## Run Locally

Inside of your newly created environment run:

```bash
python manage.py runserver
```
And or If you have made changes to the styling you will need to open another terminal inside of the environment and run:
```bash
python manage.py tailwind start
```

## Production

To create a production build of your theme, run:
```bash
python manage.py tailwind build
```

## Documentation

[Project Report](https://pdfhost.io/v/b7hB7oiAU_TowFood_PWA)

[Deployment to AWS Report](https://pdfhost.io/v/hfFf~NRtN_Launching_TowFood_Django_App_on_AWS_Elastic_Beanstalk)


## Database

You can either use SQLite or Postgres.

I would recommend Postgres if you wish to deploy to AWS.

## Demo

Hosted with Postgresql on AWS elasticbeanstalk

http://towfood2-env.eba-hriwjts6.eu-west-2.elasticbeanstalk.com/

## User Interface:

![User Interface](https://i.ibb.co/pjFrtPV/Screenshot-2022-11-13-at-10-13-39-PM.png)
Performing a Collection (Stock In):
![Performing a Collection (Stock In)](https://i.ibb.co/h2zJ6BV/Screenshot-2022-11-13-at-10-13-50-PM.png)
Performing a Pickup (Stock Out):
![Performing a Pickup (Stock Out)](https://i.ibb.co/NV30QVm/Screenshot-2022-11-13-at-10-14-05-PM.png)
Report Generation:
![Report Generation](https://i.ibb.co/QMw4WQc/Screenshot-2022-11-13-at-10-14-16-PM.png)


## Useful Resources:

 - [Django Tailwind Docs](https://django-tailwind.readthedocs.io/en/latest/index.html)
 - [DaisyUI Components](https://daisyui.com/components/)

## Acknowledgements

 - [Open Food Facts](https://world.openfoodfacts.org/)
 - [Project Supervisor - Hongbo Du](https://www.buckingham.ac.uk/directory/mr-hongbo-du/)
 - [University of Buckingham, School of Computing](https://www.buckingham.ac.uk/computing)


## Author

- [@PrenSJ2 - Github](https://www.github.com/PrenSJ2)
- [Sebastian Prentice - LinkedIn](https://www.linkedin.com/in/sebastianprentice/)
