## Users
- userId INT NOT NULL PRIMARY KEY
- OrganizationId INT NOT NULL FOREIGN KEY
- first_name VARCHAR(30) NOT NULL
- last_name VARCHAR(30) NOT NULL
- email VARCHAR(30) NOT NULL
- password VARCHAR(30) NOT NULL
- phone_number VARCHAR(12) NULL
- username VARCHAR(30) NOT NULL
- permission_level VARCHAR(30) NOT NULL

## Organisation
- organizationId INT NOT NULL PRIMARY KEY
- name VARCHAR(100) NOT NULL
- type VARCHAR(30) NOT NULL
- Acronym VARCHAR(30) NULL

## MInistry (Lookup Table)
- minId INT NOT NULL PRIMAMRY KEY
- name VARCHAR(100) NOT NULL

## Private Sector (Lookup Table)
- psID INT NOT NULL PRIMARY KEY
- name VARCHAR(100) NOT NULL

## Public Sector (Lookup Table)
- psID INT NOT NULL PRIMARY KEY
- name VARCHAR(100) NOT NULL

## Academia (Lookup Table)
- acID INT NOT NULL PRIMARY KEY
- name VARCHAR(100)

### Permission Levels/Roles
- Contact Admin
- User
- System Adminit

