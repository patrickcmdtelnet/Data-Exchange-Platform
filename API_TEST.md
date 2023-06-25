# DATA EXCHANGE PLATFORM API SAMPLE TESTING

Change to the `api` directory.

```sh
cd api
```

### Create sample organizations

Run the interactive django shell

```sh
make shell_plus
```

While in the interactive shell executes the commands. See corresponding screenshot below and remember to exit the shell when done.

```
from core.tests.factories import OrganizationFactory
org1 = OrganizationFactory(name="UN Pulse Labs Kampala", acronym="UNPLK")
org1

org2 = OrganizationFactory(name="Uganda Wild Life Authority", acronym="UWLA")
org2
```

![sample organizations](screenshoots/sample-organizations.png)

### Create superuser/superadmin

Run the command below and follow the prompts. `organization` must an integer number corresponding to the `organization id` in the database

```sh
make createsuperuser
```

See screenshot below

![createsuperuser](screenshoots/createsuperuser.png)


### Start server

```sh
make start-server PORT==8000
```

Browse to the url `http://localhost:8000` and see the api documentation.

![API DOCS](screenshoots/docs-swagger.png)

To test out the rest of the endpoints use an api client like [Postman](https://www.postman.com/downloads/) or you can also use `VSCODE` extension `Thunder client` like what is used in the illustrations below.

### Register user

To register a user, make `POST` request to the endpoint `http://localhost:8000/auth/register` with example request body. You get a response back with an email to verify your email account. For now we are using the `console Email Backend` for testing. This will have to change when using `staging` or `production` environments where you to configure an email server in django settings

```json
{
  "email": "esthernamanda@example.com",
  "username": "esther",
  "first_name": "Esther",
  "last_name": "Namanda",
  "phone_number": "0700101010",
  "organization": 1,
  "password": "passwordtest12343",
  "confirm_password": "passwordtest12343"
}
```

![register user](screenshoots/register-user.png)

### Verify user email account

Copy the link set to your email and make a `GET` request in order to verify your account

`http://localhost:8000/auth/email-verify/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3NzYzMzYxLCJpYXQiOjE2ODc2NzY5NjEsImp0aSI6ImZmNTkyZDEzN2ZmYzQ1ZjJhOWUwM2M1ZmM2ZDIyYjk2IiwidXNlcl9pZCI6N30.TwY6l4GsGECy-pyDU-p6__E5ITN25v1AjMtEEMoC-Hw`

![verify user account](screenshoots/verify-user.png)

### Login user

After verifying a user account you can proceed to login a user. Make a `POST` request to the endpoint `http://localhost:8000/auth/login` using sample request body as below. The response should be user details together with the tokens.

```json
{
  "email": "esthernamanda@example.com",
  "password": "passwordtest12343"
}
```

![login user](screenshoots/login_user.png)

### Try register and login an unverified user

Try registering a user and login before verifying them. You should get an error showing `The user account needs to be verified first before login`

![register user](screenshoots/register-user2.png)

![login unverified user](screenshoots/login_unverified_user.png)

### Logout user

Make a `POST` request to the endpoint `http://localhost:8000/auth/logout` with sample request body in order to logout a user. The `refresh` value show be the `refresh token` that was returned when a user logged in. Also remember to pass an `Authorization Bearer` Header when making this request

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4Nzc2NDI0MiwiaWF0IjoxNjg3Njc3ODQyLCJqdGkiOiJkNDgxYzg2NmU0ZmM0M2ViYTA3NzRlMjMwYjE4YzNiZCIsInVzZXJfaWQiOjZ9.vazF8OvSAOe93h7KbkSRK8kgQMEsZmOpB50SC_Knyg4"
}
```

#### Sample authorization headers

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3NzY0MjQyLCJpYXQiOjE2ODc2Nzc4NDIsImp0aSI6ImQ3NmRmNWI1NDhlYjQyMDliMDY2NzhlNjBiY2QzNTE1IiwidXNlcl9pZCI6Nn0.vTtnPddPlHoYhS-CDu7kJvZ4wjUGsk147DvAf-j64uU
```

![auth header](screenshoots/auth-headers.png)

![logout user](screenshoots/logout-user.png)

### Password reset for user

Make a `POST` request to the endpoint `http://localhost:8000/auth/request-reset-password-email`. Also an email is sent when the reqiest is successful.

```json
{
  "email": "esthernamanda@example.com"
}
```

![password reset](screenshoots/request-password-reset.png)

### Setnew password for user (Reset-password complete)

When request for password is complete. See the link sent to the email e.g `http://localhost:8000/auth/password-reset/Ng/bqcfff-f89d3073005ebe4eb7812425a2512f1f/`.

Make a `PATCH` request to the endpoint `http://localhost:8000/auth/password-reset-complete` in order to complete resetting the password.

```
{
  "password": "newpasswordset123",
  "token": "bqcfff-f89d3073005ebe4eb7812425a2512f1f",
  "uidb64": "Ng"
}
```

![password reset complete](screenshoots/reset-password-complete.png)

### Login to Admin Portal

You can login to the admin portal with the credentials you created for a superuser `http://localhost:8000/admin`

![admin login](screenshoots/super-admin-login.png)


![admin portal](screenshoots/super-admin-portal.png)


![admin user listings](screenshoots/user-listings-admin.png)
