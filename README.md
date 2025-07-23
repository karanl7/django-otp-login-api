# Django OTP Login API 🔐

A secure user login system using Email and OTP built with Django, JWT, and Docker.

## 🔧 Features
- Register with email
- OTP sent to email (mock print)
- Verify OTP
- Login with JWT token
- Docker support

## 🚀 Run Locally

```bash
docker build -t otp-api .
docker run -p 8000:8000 otp-api
